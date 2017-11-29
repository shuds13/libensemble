from __future__ import division
from __future__ import absolute_import

import numpy as np
from mpi4py import MPI


def uniform_random_sample_obj_components(H,gen_info,gen_specs,libE_info):
    del libE_info # Ignored parameter

    ub = gen_specs['ub']
    lb = gen_specs['lb']

    n = len(lb)
    m = gen_specs['components']
    b = gen_specs['gen_batch_size']

    O = np.zeros(b*m, dtype=gen_specs['out'])
    for i in range(0,b):
        # x = np.random.uniform(lb,ub,(1,n))
        x = gen_info['rand_stream'][MPI.COMM_WORLD.Get_rank()].uniform(lb,ub,(1,n))

        O['x'][i*m:(i+1)*m,:] = np.tile(x,(m,1))
        # O['priority'][i*m:(i+1)*m] = np.random.uniform(0,1,m)
        O['priority'][i*m:(i+1)*m] = gen_info['rand_stream'][MPI.COMM_WORLD.Get_rank()].uniform(0,1,m)
        O['obj_component'][i*m:(i+1)*m] = np.arange(0,m)

        O['pt_id'][i*m:(i+1)*m] = len(H)//m+i

    return O, gen_info

def uniform_random_sample(H,gen_info,gen_specs,libE_info):
    del libE_info # Ignored parameter

    ub = gen_specs['ub']
    lb = gen_specs['lb']

    n = len(lb)
    b = gen_specs['gen_batch_size']

    O = np.zeros(b, dtype=gen_specs['out'])
    for i in range(0,b):
        # x = np.random.uniform(lb,ub,(1,n))
        x = gen_info['rand_stream'][MPI.COMM_WORLD.Get_rank()].uniform(lb,ub,(1,n))

        O['x'][i] = x

    return O, gen_info
