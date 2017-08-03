#!/usr/bin/env bash

# *** Run pre-push testing ***

#sh* - draft script - replace with a runtests.py (pref. in a test dir)
#If hooks/set-hooks.sh is run - this runs as a pre-push git script
#Once setup can use "git push --no-verify" to push without running
#Note coverage only run with unit tests

# Options for test types (only matters if "true" or anything else)
export RUN_UNIT_TESTS=true    #Recommended for pre-push / CI tests
export RUN_COV_TESTS=true     #Provide coverage report
export RUN_REG_TESTS=true     #Recommended for pre-push / CI tests
export RUN_PEP_TESTS=false     #Code syle conventions
#--------------------------------------------------------------------------
     
# Test Directories 
#export CODE_DIR=code
export CODE_DIR=libensemble
export LIBE_SRC_DIR=$CODE_DIR/src
export UNIT_TEST_SUBDIR=$CODE_DIR/unit_tests
export REG_TEST_SUBDIR=$CODE_DIR/examples

# Regression test options
export REG_TEST_CORE_COUNT=4
export REG_USE_PYTEST=true

#sh - need to automate - should work with tox etc
#   - Only applies when not running pytest
#export PYTHON_MAJ_VER=python3 

#PEP code standards test options
export PYTHON_PEP_STANDARD=pep8

#export PEP_SCOPE=$CODE_DIR
export PEP_SCOPE=$LIBE_SRC_DIR

#--------------------------------------------------------------------------
#get opts - sh - quick test just pass positional parameter
#set -x

script_name=`basename "$0"`

unset RUN_PREFIX
if [ -n "$1" ]; then
  RUN_PREFIX=$1
else
  RUN_PREFIX=$script_name
fi;


#set +x
#--------------------------------------------------------------------------

# Note - pytest exit codes
# Exit code 0:	All tests were collected and passed successfully
# Exit code 1:	Tests were collected and run but some of the tests failed
# Exit code 2:	Test execution was interrupted by the user
# Exit code 3:	Internal error happened while executing tests
# Exit code 4:	pytest command line usage error
# Exit code 5:	No tests were collected

tput bold
#echo -e "\nRunning $RUN_PREFIX libensemble Test-suite .......\n"
echo -e "\n************** Running: Libensemble Test-Suite **************\n"
tput sgr 0
echo -e "Selected:"
[ $RUN_UNIT_TESTS = "true" ] && echo -e "Unit Tests"
[ $RUN_COV_TESTS = "true" ]  && echo -e " - including coverage analysis"
[ $RUN_REG_TESTS = "true" ]  && echo -e "Regression Tests"
[ $RUN_PEP_TESTS = "true" ]  && echo -e "PEP Code Standard Tests (static code test)"


# Using git root dir
root_found=false

ROOT_DIR=$(git rev-parse --show-toplevel) && root_found=true

#To enable running from other dirs
#export PYTHONPATH=${PYTHONPATH}:$ROOT_DIR

#debugging script
#echo -e "python path is $PYTHONPATH"

#set -x


if [ "$root_found" = true ]; then
  

  # Run Unit Tests ---------------------------------------------------
  
  if [ "$RUN_UNIT_TESTS" = true ]; then  
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX: Running unit tests"
    tput sgr 0     
    if [ "RUN_COV_TESTS" = true ]; then
      pytest $ROOT_DIR/$UNIT_TEST_SUBDIR/test_manager_main.py
    else
      pytest  --cov=. --cov-report html:cov_html $ROOT_DIR/$UNIT_TEST_SUBDIR/test_manager_main.py    
      #pytest  --cov=.  $ROOT_DIR/$UNIT_TEST_SUBDIR/test_manager_main.py    
    fi;
    
    code=$?
    if [ "$code" -eq "0" ]; then
    	echo
    	tput bold;tput setaf 2; echo "Unit tests passed. Continuing...";tput sgr 0
    	echo
    else
    	echo
    	put bold;tput setaf 1;echo -e "Abort $RUN_PREFIX: Unit tests failed: $code";tput sgr 0
     	exit $code #return pytest exit code
    fi;  
  fi;


  # Run Regression Tests ---------------------------------------------
  
  if [ "$RUN_REG_TESTS" = true ]; then  
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX: Running regression tests"
    tput sgr 0    
    #sh - For now cd to directories - cannot run from anywhere
    cd $ROOT_DIR/$REG_TEST_SUBDIR #sh - add test/err
        
    #Build dependencies
    cd GKLS_and_uniform_random_sample/GKLS_sim_src #sh - add test/err - input dir names
    make gkls_single #sh Test this also - possible failure mode
    cd ../../
        
    #Run regression tests - mpi - and check result...
    #Before first test set code to zero
    code=0
    
    
    #For Each Test check code is 0 - or skip to test summary
    if [ "$code" -eq "0" ]; then
      RUN_TEST=true
    else
      RUN_TEST=false
    fi
      
    # If output test req. would go here - generally will use assertion within code
      
    if [ "$RUN_TEST" = "true" ]; then        
       #sh - currently manually name tests - future create list/auto
       cd GKLS_and_aposmm/
       
       #sh for pytest - may be better to wrap main test as function.
       if [ "$REG_USE_PYTEST" = true ]; then
         echo -e "Regression testing using pytest"
         mpiexec -np $REG_TEST_CORE_COUNT pytest test_libE_on_GKLS_pytest.py
	 test_code=$?
       else
         #mpiexec -np $REG_TEST_CORE_COUNT $PYTHON_MAJ_VER call_libE_on_GKLS.py
	 echo -e "Regression testing is NOT using pytest"
	 python --version
	 #PYTH_VER=`python --version`
	 #echo -e "Running $PYTH_VER"
         mpiexec -np $REG_TEST_CORE_COUNT python call_libE_on_GKLS.py
	 test_code=$?
       fi              

       if [ "$test_code" -eq "0" ]; then
    	   echo -e " ---Test 1: call_libE_on_GKLS.py ...passed"
	   #continue testing
       else
    	   echo -e " ---Test 1: call_libE_on_GKLS.py ...failed"
    	   code=$test_code #sh - currently stop on failure
       fi;
    fi;


    #All reg tests - summary ----------------------------------------------
    if [ "$code" -eq "0" ]; then
    	echo
    	tput bold;tput setaf 2; echo "Regression tests passed. Continuing...";tput sgr 0
    	echo
    else
    	echo
    	tput bold;tput setaf 1;echo -e "Abort $RUN_PREFIX: Regression tests failed";tput sgr 0
    	exit 1 #shudson - cld return pytest exit code
    fi;  
    

  fi; #$RUN_REG_TESTS


  # Run Code standards Tests -----------------------------------------
  
  if [ "$RUN_PEP_TESTS" = true ]; then
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX: Running PEP tests - All python src below $PEP_SCOPE"
    tput sgr 0
    pytest --$PYTHON_PEP_STANDARD $ROOT_DIR/$PEP_SCOPE
    
    code=$?
    if [ "$code" -eq "0" ]; then
    	echo
    	echo "PEP tests passed. Continuing..."
    	echo
    else
    	echo
    	echo -e "Abort $RUN_PREFIX: PEP tests failed: $code"
     	exit $code #return pytest exit code
    fi;  
  fi;
  



  # ------------------------------------------------------------------ 
  tput bold;tput setaf 2
  echo -e "\n$RUN_PREFIX: All tests passed\n"
  tput sgr 0
  exit 0
else
  tput bold;tput setaf 1
  echo -e "Abort $RUN_PREFIX:  Git repository root not found"
  tput sgr 0
  exit 1
fi
