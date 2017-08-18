#!/usr/bin/env bash

# *** Run libensemble testing ***

#Draft script - replace with a runtests.py
#If hooks/set-hooks.sh is run - this runs as a pre-push git script

# Options for test types (only matters if "true" or anything else)
export RUN_UNIT_TESTS=true    #Recommended for pre-push / CI tests
export RUN_COV_TESTS=true     #Provide coverage report
export RUN_REG_TESTS=true     #Recommended for pre-push / CI tests
export RUN_PEP_TESTS=false     #Code syle conventions
#-----------------------------------------------------------------------------------------
     
# Test Directories - all relative to project root dir
export CODE_DIR=code
export LIBE_SRC_DIR=$CODE_DIR/src
export TESTING_DIR=$CODE_DIR/tests
export UNIT_TEST_SUBDIR=$TESTING_DIR/unit_tests
export REG_TEST_SUBDIR=$TESTING_DIR/regression_tests

#Coverage merge and report dir - will need the relevant .coveragerc file present
export COV_MERGE_DIR='' #root dir
#export COV_MERGE_DIR=$TESTING_DIR

# Regression test options
#export REG_TEST_PROCESS_COUNT=4
export REG_TEST_PROCESS_COUNT_LIST='2 4'
export REG_USE_PYTEST=false
export REG_TEST_OUTPUT_EXT=std.out #/dev/null

#Currently test directory within example
  # maybe more than one per dir? - or maybe put in one dir - in reg_test subdir under tests
#export REG_TEST_LIST='GKLS_and_aposmm GKLS_and_aposmm'
#export REG_TEST_LIST='test_libE_on_GKLS_aposmm_1.py test_number2.py' #selected/ordered
export REG_TEST_LIST=test_*.py #unordered

#PEP code standards test options
export PYTHON_PEP_STANDARD=pep8

#export PEP_SCOPE=$CODE_DIR
export PEP_SCOPE=$LIBE_SRC_DIR

#-----------------------------------------------------------------------------------------
#Parse Options
#set -x

unset PYTHON_VER
unset RUN_PREFIX

#Default to script name for run-prefix (name of tests)
script_name=`basename "$0"`
RUN_PREFIX=$script_name

while getopts ":p:n:" opt; do
  case $opt in
    p)
      echo "Parameter supplied for Python version: $OPTARG" >&2
      PYTHON_VER=$OPTARG
      ;;
    n)
      echo "Parameter supplied for Test Name: $OPTARG" >&2
      RUN_PREFIX=$OPTARG
      ;;
    \?)
      echo "Invalid option supplied: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

#If not supplied will go to just python (no number) - eg. with tox/virtual envs
PYTHON_RUN=python$PYTHON_VER
echo -e "Python run: $PYTHON_RUN"


#set +x
#-----------------------------------------------------------------------------------------

# Note - pytest exit codes
# Exit code 0:  All tests were collected and passed successfully
# Exit code 1:  Tests were collected and run but some of the tests failed
# Exit code 2:  Test execution was interrupted by the user
# Exit code 3:  Internal error happened while executing tests
# Exit code 4:  pytest command line usage error
# Exit code 5:  No tests were collected

tput bold
#echo -e "\nRunning $RUN_PREFIX libensemble Test-suite .......\n"
echo -e "\n************** Running: Libensemble Test-Suite **************\n"
tput sgr 0
echo -e "Selected:"
[ $RUN_UNIT_TESTS = "true" ] && echo -e "Unit Tests"
[ $RUN_COV_TESTS = "true" ]  && echo -e " - including coverage analysis"
[ $RUN_REG_TESTS = "true" ]  && echo -e "Regression Tests"
[ $RUN_PEP_TESTS = "true" ]  && echo -e "PEP Code Standard Tests (static code test)"

COV_LINE_SERIAL=''
COV_LINE_PARALLEL=''
if [ $RUN_COV_TESTS = "true" ]; then
   COV_LINE_SERIAL='--cov --cov-report html:cov_unit'
   #COV_LINE_PARALLEL='-m coverage run --parallel-mode --rcfile=../.coveragerc' #running in sub-dirs
   COV_LINE_PARALLEL='-m coverage run --parallel-mode' #running in regression dir itself
   
   #include branch coverage? eg. flags if never jumped a statement block...
   #COV_LINE_PARALLEL='-m coverage run --branch --parallel-mode'
fi;


# Using git root dir
root_found=false

ROOT_DIR=$(git rev-parse --show-toplevel) && root_found=true

#To enable running from other dirs
#export PYTHONPATH=${PYTHONPATH}:$ROOT_DIR

#debugging script
#echo -e "python path is $PYTHONPATH"

#set -x


if [ "$root_found" = true ]; then

  cd $ROOT_DIR/

  # Run Unit Tests -----------------------------------------------------------------------
  
  if [ "$RUN_UNIT_TESTS" = true ]; then  
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX --$PYTHON_RUN: Running unit tests"
    tput sgr 0    
    
    cd $ROOT_DIR/$UNIT_TEST_SUBDIR
    
    #For coverage run from code dir so can find SRC dir when not installed - cannot find modules above in pytest
    #cd $ROOT_DIR/$CODE_DIR    

    #$PYTHON_RUN -m pytest $COV_LINE_SERIAL $ROOT_DIR/$UNIT_TEST_SUBDIR/test_manager_main.py 
    $PYTHON_RUN -m pytest $COV_LINE_SERIAL 
    code=$?
    if [ "$code" -eq "0" ]; then
      echo
      tput bold;tput setaf 2; echo "Unit tests passed. Continuing...";tput sgr 0
      echo
    else
      echo
      tput bold;tput setaf 1;echo -e "Abort $RUN_PREFIX: Unit tests failed: $code";tput sgr 0
       exit $code #return pytest exit code
    fi;
    
    #Not ideal.... post-process coverage
    #if [ "$RUN_COV_TESTS" = true ]; then
    #  #For coverage run from code dir so can find SRC dir when not installed - cannot find modules above in pytest     
    #  
    #  if [ -e $ROOT_DIR/$UNIT_TEST_SUBDIR/cov_unit ]; then
    #    rm -r $ROOT_DIR/$UNIT_TEST_SUBDIR/cov_unit
    #  fi;
    #  mv .cov_unit_out $ROOT_DIR/$UNIT_TEST_SUBDIR
    #  mv cov_unit $ROOT_DIR/$UNIT_TEST_SUBDIR    
    #fi;
    
      
  fi;  
  cd $ROOT_DIR/

#set -x
  # Run Regression Tests -----------------------------------------------------------------
    
  if [ "$RUN_REG_TESTS" = true ]; then  
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX --$PYTHON_RUN: Running regression tests"
    tput sgr 0
    
    #sh - For now cd to directories - cannot run from anywhere
    cd $ROOT_DIR/$REG_TEST_SUBDIR #sh - add test/err
    
    #Running without subdirs - delete any leftover output and coverage data files
    [ -e *.$REG_TEST_OUTPUT_EXT ] && rm *.$REG_TEST_OUTPUT_EXT
    [ -e *.npy ] && rm *.npy
    [ -e .cov_reg_out.* ] && rm .cov_reg_out.*
    [ -e active_runs.txt ] && rm active_runs.txt  
            
    #Build dependencies
    cd common/GKLS_and_uniform_random_sample/GKLS_sim_src #sh - add test/err - input dir names
    make gkls_single #sh Test this also - possible failure mode
    
    #Add further dependencies here .....
    
        
    cd $ROOT_DIR/$REG_TEST_SUBDIR
        
    #Run regression tests - mpi - and check result...
    #Before first test set code to zero
    code=0
    
    #sh for pytest - may be better to wrap main test as function.
    if [ "$REG_USE_PYTEST" = true ]; then
      echo -e "Regression testing using pytest"
      [ $RUN_COV_TESTS = "true" ]  && echo -e "WARNING: Coverage NOT being run for regression tests - not working with pytest\n"   
    else
      echo -e "Regression testing is NOT using pytest"
    fi 
    #tput bold;tput setaf 4; echo -e "***Note***: Duplicating Test libE_on_GKLS\n";  tput sgr 0           
    
    echo -e ""

    # ********* Loop over regression tests ************
    reg_start=$SECONDS
    reg_count=0
    reg_count_runs=0    
    reg_pass=0
    reg_fail=0 
    test_num=0       
    #for TEST_DIR in $REG_TEST_LIST
    for TEST_SCRIPT in $REG_TEST_LIST
    do
      test_num=$((test_num+1))
      #Need proc count here for now - still stop on failure etc.
      for NPROCS in $REG_TEST_PROCESS_COUNT_LIST
      do
      
        #sh Currently stop on failure - make option to carry on later....
        #Before Each Test check code is 0 (passed so far) - or skip to test summary
        if [ "$code" -eq "0" ]; then
          RUN_TEST=true
        else
          RUN_TEST=false
        fi

        # If output test req. would go here - generally will use assertion within code

        if [ "$RUN_TEST" = "true" ]; then        

           #cd $TEST_DIR

           #sh for pytest - may be better to wrap main test as function.
           if [ "$REG_USE_PYTEST" = true ]; then
             mpiexec -np $NPROCS $PYTHON_RUN -m pytest $TEST_SCRIPT >> $TEST_SCRIPT.$REG_TEST_OUTPUT_EXT
             #mpiexec -np $REG_TEST_PROCESS_COUNT $PYTHON_RUN -m pytest $COV_LINE_PARALLEL test_libE_on_GKLS_pytest.py >> $REG_TEST_OUTPUT
             test_code=$?
           else
             mpiexec -np $NPROCS $PYTHON_RUN $COV_LINE_PARALLEL $TEST_SCRIPT >> $TEST_SCRIPT.$NPROCS'procs'.$REG_TEST_OUTPUT_EXT
             test_code=$?   
           fi
           reg_count_runs=$((reg_count_runs+1))

           if [ "$test_code" -eq "0" ]; then
             echo -e " ---Test $test_num: $TEST_SCRIPT on $NPROCS processes ...passed"
             reg_pass=$((reg_pass+1))
             #continue testing
           else
             echo -e " ---Test $test_num: $TEST_SCRIPT on $NPROCS processes ...failed"
             code=$test_code #sh - currently stop on failure
             reg_fail=$((reg_fail+1))     
           fi;

           #Move this test's coverage files to regression dir where they can be merged with other tests
           #[ "$RUN_COV_TESTS" = "true" ] && mv .cov_reg_out.* ../


           #cd $ROOT_DIR/$REG_TEST_SUBDIR

        fi; #if [ "$RUN_TEST" = "true" ];
      
      done #nprocs
      reg_count=$((reg_count+1))
    done #te
    reg_time=$(( SECONDS - start ))
    
    # ********* End Loop over regression tests *********


    #sh - temp. line to make sure in right place - needs updating based on dir layout
    cd $ROOT_DIR/$REG_TEST_SUBDIR


    #Create Coverage Reports
    #Only if passed - else may be misleading!
    #sh assumes names of coverage data files - once working make dot files and put above
    if [ "$code" -eq "0" ]; then
      if [ "$RUN_COV_TESTS" = true ]; then
        
        # Merge MPI coverage data for all ranks from regression tests and create html report in sub-dir
        
        #sh REMEMBER - MUST COMBINE ALL IF IN SEP SUB-DIRS WILL COPY TO DIR ABOVE - BUT WORK OUT WHAT WILL BE DIR STRUCTURE
        coverage combine  .cov_reg_out.* #Name of coverage data file must match that in .coveragerc in reg test dir.
        coverage html

        echo -e "\n..moving output files to output/ dir"
        mv *.$REG_TEST_OUTPUT_EXT output/
        mv *.npy output/
        mv active_runs.txt  output/    
  
                
        if [ "$RUN_UNIT_TESTS" = true ]; then

          #Combine with unit test coverage at top-level
          cd $ROOT_DIR/$COV_MERGE_DIR
          cp $ROOT_DIR/$UNIT_TEST_SUBDIR/.cov_unit_out .
          cp $ROOT_DIR/$REG_TEST_SUBDIR/.cov_reg_out . #sh - IMPORTANT - FIX THIS - Ok this would assume all reg tests in one dir
          
          #coverage combine --rcfile=.coverage_merge.rc .cov_unit_out .cov_reg_out
          coverage combine .cov_unit_out .cov_reg_out #Should create .cov_merge_out - if picks up correct .coveragerc

          #coverage combine .cov_merge_out  $ROOT_DIR/$REG_TEST_SUBDIR/.cov_reg_out
          #coverage html --rcfile=.coverage_merge.rc
          coverage html #Should create cov_merge/ dir
        fi;
        
      fi;    
    fi;


    #All reg tests - summary ----------------------------------------------
    if [ "$code" -eq "0" ]; then
      echo
      #tput bold;tput setaf 2
      
      if [ "$REG_USE_PYTEST" != true ]; then
  #sh - temp formatting similar(ish) to pytest - update in python (as with timing)
  tput bold;tput setaf 4; echo -e "***Note***: temporary formatting/timing ......"
  tput bold;tput setaf 2;echo -e "============================ $reg_pass passed in $reg_time seconds ============================"
      fi;
      
      tput bold;tput setaf 2;echo "Regression tests passed. Continuing..."      
      tput sgr 0
      echo
    else
      echo
      tput bold;tput setaf 1;echo -e "Abort $RUN_PREFIX: Regression tests failed";tput sgr 0
      exit 1 #shudson - cld return pytest exit code
    fi;  
    

  fi; #$RUN_REG_TESTS


  # Run Code standards Tests -----------------------------------------
  cd $ROOT_DIR
  if [ "$RUN_PEP_TESTS" = true ]; then
    tput bold;tput setaf 6
    echo -e "\n$RUN_PREFIX --$PYTHON_RUN: Running PEP tests - All python src below $PEP_SCOPE"
    tput sgr 0
    pytest --$PYTHON_PEP_STANDARD $ROOT_DIR/$PEP_SCOPE
    
    code=$?
    if [ "$code" -eq "0" ]; then
      echo
      tput bold;tput setaf 2; echo "PEP tests passed. Continuing...";tput sgr 0
      echo
    else
      echo
      tput bold;tput setaf 1;echo -e "Abort $RUN_PREFIX: PEP tests failed: $code";tput sgr 0
       exit $code #return pytest exit code
    fi;  
  fi;
  

#set +x

  # ------------------------------------------------------------------ 
  tput bold;tput setaf 2; echo -e "\n$RUN_PREFIX --$PYTHON_RUN: All tests passed\n"; tput sgr 0
  exit 0
else
  tput bold;tput setaf 1; echo -e "Abort $RUN_PREFIX:  Git repository root not found"; tput sgr 0
  exit 1
fi
