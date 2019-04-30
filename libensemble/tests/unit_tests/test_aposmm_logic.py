import sys, time, os
import numpy as np

import libensemble.gen_funcs.aposmm as al

import libensemble.tests.unit_tests.setup as setup

n = 2
libE_specs = {'comm':{}}

gen_out = [('x',float,n),
      ('x_on_cube',float,n),
      ('sim_id',int),
      ('priority',float),
      ('local_pt',bool),
      ('known_to_aposmm',bool), # Mark known points so fewer updates are needed
      ('dist_to_unit_bounds',float),
      ('dist_to_better_l',float),
      ('dist_to_better_s',float),
      ('ind_of_better_l',int),
      ('ind_of_better_s',int),
      ('started_run',bool),
      ('num_active_runs',int), # Number of active runs point is involved in
      ('local_min',bool),
      ]

def test_failing_localopt_method():
    hist, sim_specs_0, gen_specs_0, exit_criteria_0, alloc  = setup.hist_setup1()

    hist.H['returned'] = 1

    gen_specs_0['localopt_method'] = 'BADNAME'

    try:
        al.advance_local_run(hist.H, gen_specs_0, 0, 0, {'run_order': {0:[0,1]}})
    except:
        assert 1, "Failed like it should have"
    else:
        assert 0, "Didn't fail like it should have"


def test_exception_raising():
    hist, sim_specs_0, gen_specs_0, exit_criteria_0, alloc  = setup.hist_setup1(n=2)
    hist.H['returned'] = 1

    for method in ['LN_SBPLX','pounders','scipy_COBYLA']:
        gen_specs_0['localopt_method'] = method

        out = al.advance_local_run(hist.H, gen_specs_0,  0, 0, {'run_order': {0:[0,1]}})

        assert out[0]==0, "Failed like it should have"


def test_decide_where_to_start_localopt():
    #sys.path.append(os.path.join(os.path.dirname(__file__), '../regression_tests'))

    #from libensemble.regression_tests.test_branin_aposmm import gen_out
    H = np.zeros(10,dtype=gen_out + [('f',float),('returned',bool)])
    H['x'] = np.random.uniform(0,1,(10,2))
    H['f'] = np.random.uniform(0,1,10)
    H['returned'] = 1

    b = al.decide_where_to_start_localopt(H, 9, 1)
    assert len(b)==0

    b = al.decide_where_to_start_localopt(H, 9, 1, nu=0.01)
    assert len(b)==0


def test_calc_rk():
    rk = al.calc_rk(2,10,1)

    rk = al.calc_rk(2,10,1,10)
    assert np.isinf(rk)


def test_initialize_APOSMM():
    hist, sim_specs_0, gen_specs_0, exit_criteria_0, alloc  = setup.hist_setup1()

    al.initialize_APOSMM(hist.H,gen_specs_0)

def test_declare_opt():
    hist, sim_specs_0, gen_specs_0, exit_criteria_0, alloc  = setup.hist_setup1(n=2)

    try: 
        al.update_history_optimal(hist.H['x_on_cube'][0]+1,hist.H,np.arange(0,10))
    except: 
        assert 1, "Failed because the best point is not in H"
    else: 
        assert 0


    hist.H['x_on_cube'][1] += np.finfo(float).eps
    hist.H['f'][1] -= np.finfo(float).eps

    # Testing case where point near x_opt is slightly better. 
    al.update_history_optimal(hist.H['x_on_cube'][0],hist.H,np.arange(0,10))
    assert np.sum(hist.H['local_min']) == 2




if __name__ == "__main__":
    test_failing_localopt_method()
    print('done')
    test_exception_raising()
    print('done')
    test_decide_where_to_start_localopt()
    print('done')
    test_calc_rk()
    print('done')
    test_initialize_APOSMM()
    print('done')
    test_declare_opt()
    print('done')
