#!/bin/bash -x
##COBALT -A <...project code...>
#COBALT -t 60
#COBALT -O libE_test
#COBALT -n 5 #no. nodes
##COBALT -q default
##COBALT -q debug-flat-quad #For small runs only
##COBALT -o tlib.%j.%N.out
##COBALT -e tlib.%j.%N.error
##COBALT --proccount 
##COBALT --attrs mcdram=cache:numa=quad #Experiment here

# Script to launch libEnsemble using Balsam within Conda. Conda environment must be set up.

# To be run with central job management - Manager and workers run on one node (or more if nec). Workers submit jobs to the rest of the nodes in the pool.

# Constaint: - As set up - only uses one node (up to 63 workers) for libE. To use more, modifiy "balsam job" line to use hyper-threading and/or more than one node.

# Name of calling script
export EXE=libE_calling_script.py

# Number of workers.
export NUM_WORKERS=16

# Wallclock for libE job (supplied to Balsam - make at least several mins smaller than wallclock for this submission to ensure job is launched)
export LIBE_WALLCLOCK=45

# Name of working directory where Balsam places running jobs/output (inside the database directory)
export WORKFLOW_NAME=libe_workflow #sh - todo - may currently be hardcoded to this in libE - allow user to specify

#Tell libE manager to stop workers, dump timing.dat and exit after this time. Script must be set up to receive as argument.
export SCRIPT_ARGS=$(($LIBE_WALLCLOCK-3)) 
# export SCRIPT_ARGS='' #Default No args

# Name of Conda environment (Need to have set up: https://balsam.alcf.anl.gov/quick/quickstart.html)
export CONDA_ENV_NAME=balsam

# Conda location - theta specific
export PATH=/opt/intel/python/2017.0.035/intelpython35/bin:$PATH
export LD_LIBRARY_PATH=~/.conda/envs/balsam/lib:$LD_LIBRARY_PATH

export PYTHONNOUSERSITE=1 #Ensure environment isolated

# Activate conda environment
. activate $CONDA_ENV_NAME

# Unload Theta modules that may interfere with Balsam
module unload trackdeps
module unload darshan
module unload xalt

#Location of sim func script (only required if not in sys.path already)
# export PYTHONPATH=/home/shudson/opal_work/opal/emittance_minimization/code:$PYTHONPATH

#Where you want your Balam database to be
#export BALSAM_DB_PATH=~/database_sqlite
#export BALSAM_DB_PATH=~/database_postgres
export BALSAM_DB_PATH=/projects/CSC250STMS07/libensemble/database_postgres

#Create a new database is not setup.
if [[ ! -d $BALSAM_DB_PATH ]]; then
  echo -e '\nCreating database at $BALSAM_DB_PATH'
  #balsam init $BALSAM_DB_PATH --db-type sqlite3 #small/medium jobs
  balsam init $BALSAM_DB_PATH --db-type postgres #big jobs (many concurrent calcs)
fi;

# Currently need atleast one DB connection per worker (for postgres).
if [[ $NUM_WORKERS -gt 100 ]]
then
   #Add a margin
   echo -e "max_connections=$(($NUM_WORKERS+10)) #Appended by submission script" >> $BALSAM_DB_PATH/balsamdb/postgresql.conf
fi
wait

#Start Balsam database server running
# balsam dbserver --stop #In case running
balsam dbserver --reset $BALSAM_DB_PATH
balsam dbserver --start 
wait
sleep 5

# Make sure no existing apps/jobs
balsam rm apps --all --force
balsam rm jobs --all --force
wait
sleep 5

# Add calling script to Balsam database as app and job.
THIS_DIR=$PWD
SCRIPT_BASENAME=${EXE%.*}
balsam app --name $SCRIPT_BASENAME.app --exec $EXE --desc "Run $SCRIPT_BASENAME"

# Running libE on one node - one manager and upto 63 workers
balsam job --name job_$SCRIPT_BASENAME --workflow $WORKFLOW_NAME --application $SCRIPT_BASENAME.app --args $SCRIPT_ARGS --wall-min $LIBE_WALLCLOCK  --num-nodes 1 --ranks-per-node $((NUM_WORKERS+1)) --url-out="local:/$THIS_DIR" --stage-out-files="*.out *.dat" --url-in="local:/$THIS_DIR" --yes

# Hyper-thread libE (note this will not affect HT status of user calcs - only libE itself)
# Running 255 workers and one manager on one libE node.
# balsam job --name job_$SCRIPT_BASENAME --workflow $WORKFLOW_NAME --application $SCRIPT_BASENAME.app --args $SCRIPT_ARGS --wall-min $LIBE_WALLCLOCK  --num-nodes 1 --ranks-per-node 256 --threads-per-core 4 --url-out="local:/$THIS_DIR" --stage-out-files="*.out *.dat" --url-in="local:/$THIS_DIR" --yes

# Multiple nodes for libE
# Running 127 workers and one manager - launch script on 129 nodes (if one node per worker)
# balsam job --name job_$SCRIPT_BASENAME --workflow $WORKFLOW_NAME --application $SCRIPT_BASENAME.app --args $SCRIPT_ARGS --wall-min $LIBE_WALLCLOCK  --num-nodes 2 --ranks-per-node 64 --url-out="local:/$THIS_DIR" --stage-out-files="*.out *.dat" --url-in="local:/$THIS_DIR" --yes

#Run job
balsam launcher --consume-all

balsam dbserver --stop
