from __future__ import division
from __future__ import absolute_import

import sys, os
import numpy as np
import scipy as sp
from scipy import spatial
from mpi4py import MPI

from numpy.lib.recfunctions import merge_arrays

from math import log, gamma, pi, sqrt

from petsc4py import PETSc
import nlopt

def aposmm_aaatest():
    """A simple test."""
    pass
