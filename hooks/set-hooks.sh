#!/usr/bin/env bash

# Create symbolic links in .git/hooks dir to hook scripts in here

# These can be stored in source control with the project
# while contents of .git/hooks are not stored

# Hook Scripts
# pre-push: Run test-suite on git push - abort on failure

# List scripts here
hk_scripts='pre-push'

#--------------------------------------------------------------------------

# Using git root dir
root_found=false

ROOT_DIR=$(git rev-parse --show-toplevel) && root_found=true

if [ "$root_found" = true ]; then
  for script in $hk_scripts
  do  
    if [ -f "$ROOT_DIR/hooks/$script" ]; then
      ln -s $ROOT_DIR/hooks/$script $ROOT_DIR/.git/hooks/$script 
      if [ $? = 0 ]; then
        echo -e "Sym link set to $ROOT_DIR/hooks/$script"
      else
        echo -e "Error: Sym link failed for $ROOT_DIR/hooks/$script"
      fi
    else
      echo -e "Error: Script $script not found in $ROOT_DIR/hooks/"
    fi    
  done
else
  echo -e "Error: Git repository root not found - aborting"  
fi
