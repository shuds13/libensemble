#!/usr/bin/env bash

# Run pre-push testing

# Options for test types
export RUN_UNIT_TESTS=true
#export RUN_COV_TESTS=false
export RUN_REG_TESTS=true
#export RUN_TOX_TESTS=false
#export RUN_PEP_TESTS=false

# Test Directories 
export UNIT_TEST_SUBDIR=code/unit_tests
export REG_TEST_SUBDIR=code/examples

# Regression test options
export REG_TEST_CORE_COUNT=4
export REG_USE_PYTEST=true

export PYTHON_MAJ_VER=python3

#--------------------------------------------------------------------------
#get opts - sh - quick test just pass positional parameter
unset RUN_PREFIX
if [ -n $1 ]; then
  RUN_PREFIX=$1
fi

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
echo -e "\n************** Running: $RUN_PREFIX Libensemble Test-Suite **************\n"
tput sgr 0

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
    echo -e "\n$RUN_PREFIX: Running unit tests"
    pytest $ROOT_DIR/$UNIT_TEST_SUBDIR/test_manager_main.py
    code=$?
    if [ "$code" -eq "0" ]; then
    	echo
    	echo "Unit tests passed. Continuing..."
    	echo
    else
    	echo
    	echo -e "Abort $RUN_PREFIX: Unit tests failed: $code"
     	exit $code #return pytest exit code
    fi;  
  fi;


  # Get Coverage of Unit Tests ---------------------------------------


  # Run Regression Tests ---------------------------------------------
  if [ "$RUN_REG_TESTS" = true ]; then  
    echo -e "\n$RUN_PREFIX: Running regression tests"
    
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
         mpiexec -np $REG_TEST_CORE_COUNT pytest call_libE_on_GKLS_pytest.py
	 test_code=$?
       else
         mpiexec -np $REG_TEST_CORE_COUNT $PYTHON_MAJ_VER call_libE_on_GKLS.py
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
    	echo "Regresion tests passed. Continuing..."
    	echo
    else
    	echo
    	echo -e "Abort $RUN_PREFIX: Regresion tests failed"
    	exit 1 #shudson - cld return pytest exit code
    fi;  
    

  fi; #$RUN_REG_TESTS


  # Run multi-platform Tests -----------------------------------------

  # Run Code standards Tests -----------------------------------------




  # ------------------------------------------------------------------
  echo -e "\n$RUN_PREFIX: All tests passed\n"
  exit 0
else
  echo -e "Abort $RUN_PREFIX:  Git repository root not found"
  exit 1
fi
