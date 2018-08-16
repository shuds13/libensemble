import sys, time, os
import numpy as np
import numpy.lib.recfunctions

#sys.path.append(os.path.join(os.path.dirname(__file__), '../../src')) 
#sys.path.append(os.path.join(os.path.dirname(__file__), '../../examples/alloc_funcs'))

import libensemble.libE_manager as man
import libensemble.tests.unit_tests.setup as setup
from libensemble.alloc_funcs.give_sim_work_first import give_sim_work_first
from libensemble.history import History

al = {'alloc_f': give_sim_work_first,'out':[]}
libE_specs = {'comm': {}, 'workers':set([1,2])}
H0=[]

def test_decide_work_and_resources():

    sim_specs, gen_specs, exit_criteria = setup.make_criteria_and_specs_1()
    hist = History(al, sim_specs, gen_specs, exit_criteria, H0)

    _, W, _ = man.initialize(hist, sim_specs, gen_specs, al, exit_criteria, libE_specs) 

    # Don't give out work when all workers are active 
    W['active'] = 1
    Work, persis_info = al['alloc_f'](W, hist.H, sim_specs, gen_specs, {})
    assert len(Work) == 0 
    # 

if __name__ == "__main__":
    test_decide_work_and_resources()
