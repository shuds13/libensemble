#!/usr/bin/env bash

#NOTE: ***PROBLEM NOT SORTED*** - sim_dir_name directory in test_branin_aposmm.py

#Set to exit script on error
set -e

if [[ -z $1 ]]
then
  echo -e "Aborting: No repo supplied"
  echo -e "Usage E.g: ./convert-to-importable.sh libensemble-balsam/"
  echo -e "If in project root dir do ./convert-to-importable.sh ."
  exit
fi

echo -e "\nTime of writing: check sim_dir_name directory in test_branin_aposmm.py"
echo -e "Also remember need packages in setup.py and make sure got __init__.py in test dirs unit/regression"
echo -e "then can do <pip install .> or <pip install --upgrade .> from the project root dir. And try run tests.\n" 

REPO_DIR=$1

export CODE_DIR=code

#Quick and Dirty Convert
#Currently going through existing files - need to generalise to get files by listing dirs - so does new ones.
#So this is files in master branch at time of writing.

convert_import_paths() {
  echo ${PWD}
  sed -i -e 's/^\(\s*\)sys.path.append/\1#sys.path.append/g' *.py 
  sed -i -e 's/^\(\s*\)from libE/\1from libensemble.libE/g' *.py 
  sed -i -e 's/^\(\s*\)from message_numbers/\1from libensemble.message_numbers/g' *.py   
  sed -i -e 's/^\(\s*\)import libE/\1import libensemble.libE/g' *.py 
  sed -i -e 's/^\(\s*\)import message_numbers/\1import libensemble.message_numbers/g' *.py   

  sed -i -e 's/^\(\s*\)from six_hump_camel/\1from libensemble.sim_funcs.six_hump_camel/g' *.py 
  sed -i -e 's/^\(\s*\)from chwirut1/\1from libensemble.sim_funcs.chwirut1/g' *.py 
  sed -i -e 's/^\(\s*\)from helloworld/\1from libensemble.sim_funcs.helloworld/g' *.py 
  sed -i -e 's/^\(\s*\)from branin/\1from libensemble.sim_funcs.branin.branin/g' *.py 
  sed -i -e 's/^\(\s*\)import six_hump_camel/\1import libensemble.sim_funcs.six_hump_camel/g' *.py 
  sed -i -e 's/^\(\s*\)import chwirut1/\1import libensemble.sim_funcs.chwirut1/g' *.py 
  sed -i -e 's/^\(\s*\)import helloworld/\1import libensemble.sim_funcs.helloworld/g' *.py 
  sed -i -e 's/^\(\s*\)import branin/\1import libensemble.sim_funcs.branin.branin/g' *.py 

  sed -i -e 's/^\(\s*\)from uniform_sampling/\1from libensemble.gen_funcs.uniform_sampling/g' *.py 
  sed -i -e 's/^\(\s*\)from aposmm_logic/\1from libensemble.gen_funcs.aposmm_logic/g' *.py 
  sed -i -e 's/^\(\s*\)import uniform_sampling/\1import libensemble.gen_funcs.uniform_sampling/g' *.py 
  sed -i -e 's/^\(\s*\)import aposmm_logic/\1import libensemble.gen_funcs.aposmm_logic/g' *.py 
  sed -i -e 's/^\(\s*\)from uniform_or_localopt/\1from libensemble.gen_funcs.uniform_or_localopt/g' *.py 
  sed -i -e 's/^\(\s*\)import uniform_or_localopt/\1import libensemble.gen_funcs.uniform_or_localopt/g' *.py 
  
  sed -i -e 's/^\(\s*\)from give_sim_work_first/\1from libensemble.alloc_funcs.give_sim_work_first/g' *.py
  sed -i -e 's/^\(\s*\)import give_sim_work_first/\1import libensemble.alloc_funcs.give_sim_work_first/g' *.py  

  sed -i -e 's/^\(\s*\)from start_persistent_local_opt_gens/\1from libensemble.alloc_funcs.start_persistent_local_opt_gens/g' *.py
  sed -i -e 's/^\(\s*\)import start_persistent_local_opt_gens/\1import libensemble.alloc_funcs.start_persistent_local_opt_gens/g' *.py  
  
  #Special kluge - for unit tests accessing regression tests - now i've made unit/reg tests submodules
  #Not sure this is a good idea
  sed -i -e 's/^\(\s*\)from test_branin_aposmm/\1from libensemble.regression_tests.test_branin_aposmm/g' *.py   
}

echo -e "Converting libensemble src dir:"
cd $REPO_DIR

cd code/src
convert_import_paths

echo -e "Converting libensemble examples:"
cd ../examples/

cd calling_scripts
convert_import_paths

cd ../alloc_funcs
convert_import_paths

cd ../sim_funcs
convert_import_paths
cd branin/
convert_import_paths
cd ..

cd ../gen_funcs
convert_import_paths
cd ..

echo -e "Converting libensemble tests:"
cd ../tests/
cd unit_tests
convert_import_paths

cd ../regression_tests
convert_import_paths
