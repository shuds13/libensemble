"""
    import IPython; IPython.embed()
    sys.stdout.flush()
    import ipdb; ipdb.set_trace()
libEnsemble manager routines
====================================================


"""

from __future__ import division
from __future__ import absolute_import

from message_numbers import EVAL_TAG # manager tells worker to evaluate the point 
from message_numbers import STOP_TAG # manager tells worker run is over

from mpi4py import MPI
import numpy as np
import scipy as sp
from scipy import spatial

import time,sys

def manager_main(comm, allocation_specs, sim_specs, gen_specs,
        failure_processing, exit_criteria, H0):

    status = MPI.Status()
    
    print("******************WARNING: THIS IS AN EXPERIMENTAL VERSION OF LIBENSEMBLE")
    print("******************WARNING: THIS IS AN EXPERIMENTAL VERSION OF LIBENSEMBLE")
    print("******************WARNING: THIS IS AN EXPERIMENTAL VERSION OF LIBENSEMBLE")

    H, H_ind = initialize_H(sim_specs, gen_specs, exit_criteria['sim_eval_max'], H0)

    idle_w = allocation_specs['worker_ranks'].copy()
    active_w = {'gen':set(), 'sim':set()}

    ### Continue receiving and giving until termination test is satisfied
    while termination_test(H, H_ind, exit_criteria, len(H0)):

        H, H_ind, active_w, idle_w = receive_from_sim_and_gen(comm, active_w, idle_w, H, H_ind)

        update_active_and_queue(active_w, idle_w, H[:H_ind], gen_specs)

        Work = decide_work_and_resources(active_w, idle_w, H, H_ind, sim_specs, gen_specs)

        for w in Work:
            comm.send(obj=Work[w], dest=w, tag=EVAL_TAG)
            active_w[Work[w]['calc_info']['type']].add(w)
            idle_w.remove(w)

    ### Receive from all active workers 
    while len(active_w['gen'].union(active_w['sim'])):
        H, H_ind, active_w, idle_w = receive_from_sim_and_gen(comm, active_w, idle_w, H, H_ind)

    ### Stop all workers 
    for w in allocation_specs['worker_ranks']:
        comm.send(obj=None, dest=w, tag=STOP_TAG)

    return H[:H_ind]


def receive_from_sim_and_gen(comm, active_w, idle_w, H, H_ind):
    status = MPI.Status()

    active_w_copy = active_w.copy()

    while True:
        for w in active_w_copy['sim'].union(active_w_copy['gen']): 
            if comm.Iprobe(source=w, tag=MPI.ANY_TAG):
                D_recv = comm.recv(source=w, tag=MPI.ANY_TAG, status=status)
                idle_w.add(status.Get_source())
                active_w[D_recv['calc_info']['type']].remove(status.Get_source())

                if D_recv['calc_info']['type'] == 'sim':
                    update_history_f(H, D_recv)
                elif D_recv['calc_info']['type'] == 'gen':
                    H, H_ind = update_history_x_in(H, H_ind, D_recv['calc_out'])

        if active_w_copy == active_w:
            break
        else:
            active_w_copy = active_w.copy()

    return H, H_ind, active_w, idle_w

def decide_work_and_resources(active_w, idle_w, H, H_ind, sim_specs, gen_specs):
    """ Decide what should be given to workers 
    """

    Work = {}
    gen_work = 0

    for i in idle_w:
        q_inds = np.where(np.logical_and(~H['given'][:H_ind],~H['paused'][:H_ind]))[0]

        if len(q_inds):
            # Give all points with highest priority
            inds_to_send = q_inds[ np.where(H['priority'][q_inds] == max(H['priority'][q_inds]))[0] ]

            Work[i] = {'calc_f': sim_specs['f'][0], 
                       'calc_params': sim_specs['params'], 
                       'form_subcomm': [], 
                       # 'calc_in': H[sim_specs['in']][inds_to_send],
                       'calc_in': H[inds_to_send][sim_specs['in']],
                       'calc_out': sim_specs['out'],
                       'calc_info': {'type':'sim', 'sim_id': inds_to_send},
                      }

            update_history_x_out(H, inds_to_send, Work[i]['calc_in'], i, sim_specs['params'])

        else:
            # Don't give out any gen instances if in batch mode and any point has not been returned or paused
            if 'batch_mode' in gen_specs and gen_specs['batch_mode'] and any(np.logical_and(~H['returned'][:H_ind],~H['paused'][:H_ind])):
                break

            # Limit number of gen instances if given
            if 'num_inst' in gen_specs and len(active_w['gen']) + gen_work == gen_specs['num_inst']:
                break

            # Give gen work 
            gen_work += 1 

            Work[i] = {'calc_f': gen_specs['f'], 
                       'calc_params': gen_specs['params'], 
                       'form_subcomm': [], 
                       # 'calc_in': H[gen_specs['in']][:H_ind],
                       'calc_in': H[:H_ind][gen_specs['in']],
                       'calc_out': gen_specs['out'],
                       'calc_info': {'type':'gen'},
                       }

            if H_ind + gen_work >= len(H):
                break


    return Work

def update_active_and_queue(active_w, idle_w, H, gen_specs):
    """ Decide if active work should be continued and the queue order

    Parameters
    ----------
    H: numpy structured array
        History array storing rows for each point.
    """
    if 'queue_update_function' in gen_specs:
        gen_specs['queue_update_function'](H,gen_specs)
    
    return

def update_history_f(H, D): 
    """
    Updates the history (in place) after a point has been evaluated

    Parameters
    ----------
    H: numpy structured array
        History array storing rows for each point.
    """

    new_inds = D['calc_info']['sim_id']
    H_0 = D['calc_out']

    for j,ind in enumerate(new_inds): 
        for field in H_0.dtype.names:
            H[field][ind] = H_0[field][j]

        H['returned'][ind] = True


def update_history_x_in(H, H_ind, O):
    """
    Updates the history (in place) when a new point has been returned from a gen

    Parameters
    ----------
    H: numpy structured array
        History array storing rows for each point.
    H_ind: integer
        The new point
    O: numpy array
        Output from gen_f
    """

    rows_remaining = len(H)-H_ind
    
    if 'sim_id' not in O.dtype.names:
        # gen method must not be adjusting sim_id, just append to H
        num_new = len(O)

        if num_new > rows_remaining:
            H = grow_H(H,num_new-rows_remaining)
            
        update_inds = np.arange(H_ind,H_ind+num_new)
        H['sim_id'][H_ind:H_ind+num_new] = range(H_ind,H_ind+num_new)
    else:
        # gen method is building sim_id. 
        num_new = len(np.setdiff1d(O['sim_id'],H['sim_id']))

        if num_new > rows_remaining:
            H = grow_H(H,num_new-rows_remaining)

        update_inds = O['sim_id']
        
    for field in O.dtype.names:
        H[field][update_inds] = O[field]

    H_ind += num_new

    return H, H_ind

def grow_H(H, k):
    """ LibEnsemble is requesting k rows be added to H because gen_f produced
    more points than rows in H."""
    H_1 = np.zeros(k, dtype=H.dtype)
    H_1['sim_id'] = -1
    H_1['given_time'] = np.inf

    H = np.append(H,H_1)

    return H


def update_history_x_out(H, q_inds, W, lead_rank, sim_f_params):
    """
    Updates the history (in place) when a new point has been given out to be evaluated

    Parameters
    ----------
    H: numpy structured array
        History array storing rows for each point.
    H_ind: integer
        The new point
    W: numpy array
        Work to be evaluated
    lead_rank: int
        lead ranks for the evaluation of x 
    """

    for i,j in zip(q_inds,range(len(W))):
        for field in W.dtype.names:
            H[field][i] = W[field][j]

        H['given'][i] = True
        H['given_time'][i] = time.time()
        H['lead_rank'][i] = lead_rank


def termination_test(H, H_ind, exit_criteria, lenH0):
    """
    Return False if the libEnsemble run should stop 
    """

    if np.sum(H['given']) >= exit_criteria['sim_eval_max'] + lenH0:
        return False
    elif 'stop_val' in exit_criteria and any(H[exit_criteria['stop_val'][0]][:H_ind] <= exit_criteria['stop_val'][1]):
        return False
    elif 'elapsed_clock_time' in exit_criteria and time.time() - H['given_time'][lenH0] > exit_criteria['elapsed_clock_time']:
        return False
    else:
        return True



def initialize_H(sim_specs, gen_specs, feval_max, H0):
    """
    Forms the numpy structured array that records everything from the
    libEnsemble run 

    Returns
    ----------
    H: numpy structured array
        History array storing rows for each point. Field names are below

        | sim_id              : Identifier for each simulation (could be the same "point" just with different parameters) 
        | given               : True if point has been given to a worker
        | given_time          : Time point was given to a worker
        | lead_rank           : lead worker rank point was given to 
        | returned            : True if point has been evaluated by a worker
    """

    libE_fields = [('sim_id','int'),
                   ('given','bool'),       
                   ('given_time','float'), 
                   ('lead_rank','int'),    
                   ('returned','bool'),    
                   ('paused','bool'),    
                   ]

    assert 'priority' in [entry[0] for entry in gen_specs['out']],\
        "'priority' must be an entry in gen_specs['out']"
        

    if ('sim_id','int') in gen_specs['out'] and 'sim_id' in gen_specs['in']:
        print('\n' + 79*'*' + '\n'
               "User generator script will be creating sim_id.\n"\
               "Take care to do this sequentially.\n"\
               "Also, any information given back for existing sim_id values will be overwritten!\n"\
               "So everything in gen_out should be in gen_in!"\
                '\n' + 79*'*' + '\n\n')
        sys.stdout.flush()
        libE_fields = libE_fields[1:] # Must remove 'sim_id' from libE_fields because it's in gen_specs['out']

    H = np.zeros(feval_max + len(H0), dtype=libE_fields + sim_specs['out'] + gen_specs['out']) 


    if len(H0):
        names = H0.dtype.names
        assert set(names).issubset(set(H.dtype.names)), "Can not process H0 since it contains keys not in H"
        if 'returned' in names:
            assert np.all(H['returned']), "Can not use unreturned points from H0 in H, Exiting"

        for name in names:
            H[name][:len(H0)] = H0[name]


    # Prepend H with H0 
    H['sim_id'][:len(H0)] = np.arange(0,len(H0))
    H['given'][:len(H0)] = 1
    H['returned'][:len(H0)] = 1


    H['sim_id'][-feval_max:] = - 1
    H['given_time'][-feval_max:] = np.inf

    return (H, len(H0))
