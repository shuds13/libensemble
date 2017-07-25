#!/usr/bin/env bash

# Run pre-push testing

# Options for test types

export RUN_UNIT_TESTS=true
#export RUN_COV_TESTS=false
export RUN_REG_TESTS=false
#export RUN_TOX_TESTS=false
#export RUN_PEP_TESTS=false

#--------------------------------------------------------------------------

# Note - pytest exit codes
# Exit code 0:	All tests were collected and passed successfully
# Exit code 1:	Tests were collected and run but some of the tests failed
# Exit code 2:	Test execution was interrupted by the user
# Exit code 3:	Internal error happened while executing tests
# Exit code 4:	pytest command line usage error
# Exit code 5:	No tests were collected

echo -e "\nRunning pre-push test-suite .......\n"

# Using git root dir
root_found=false

ROOT_DIR=$(git rev-parse --show-toplevel) && root_found=true

#To enable running from other dirs
#export PYTHONPATH=${PYTHONPATH}:$ROOT_DIR

#debugging script
#echo -e "python path is $PYTHONPATH"

#set -x

if [ "$root_found" = true ]; then
  

  # Run Unit Tests -----------------------------------------
  
  if [ "$RUN_UNIT_TESTS" = true ]; then  
    echo -e "\npre-push: Running unit tests"
    pytest $ROOT_DIR/code/unit_tests/test_manager_main.py
    code=$?
    if [ "$code" -eq "0" ]; then
    	echo
    	echo "Unit tests passed. Continuing..."
    	echo
    else
    	echo
    	echo -e "Abort pre-push: Unit tests failed"
    	exit 1 #shudson - cld return pytest exit code
    fi;  
  fi;

  # Get Coverage of Unit Tests -----------------------------

  # Run Regression Tests -----------------------------------
  if [ "$RUN_REG_TESTS" = true ]; then  
    echo -e "\npre-push: Running regression tests"
    #pytest $ROOT_DIR/code/unit_tests/test_manager_main.py
    
    
    
    #Run regression testa - mpi - and check result...
    
    #code=$?
    
    if [ "$code" -eq "0" ]; then
    	echo
    	echo "Regresion tests passed. Continuing..."
    	echo
    else
    	echo
    	echo -e "Abort pre-push: Regresion tests failed"
    	exit 1 #shudson - cld return pytest exit code
    fi;  
  fi;

  # Run multi-platform Tests -------------------------------

  # Run Code standards Tests -------------------------------




  # --------------------------------------------------------
  echo -e "\npre-push: All tests passed\n"
  exit 0
else
  echo -e "Abort pre-push:  Git repository root not found"
  exit 1
fi
