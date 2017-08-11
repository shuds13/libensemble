===========
libensemble
===========

.. image::  https://travis-ci.org/shuds13/libensemble.svg?branch=master
   :target: https://travis-ci.org/shuds13/libensemble

.. image:: https://coveralls.io/repos/github/shuds13/libensemble/badge.svg?branch=master
   :target: https://coveralls.io/github/shuds13/libensemble?branch=master
   
.. image::  https://readthedocs.org/projects/libensemble/badge/?version=latest
   :target: https://libensemble.readthedocs.org/en/latest/



Library for managing ensemble-like collections of computations.

Note: shuds13/libensemble is an experimental fork of libensemble/libensemble. NOTHING is guaranteed to work!


Dependencies
------------

* Python_ 2.7, 3.4 or above.

* A functional MPI 1.x/2.x/3.x implementation like `MPICH
  <http://www.mpich.org/>`_ or `Open MPI <http://www.open-mpi.org/>`_
  built with shared/dynamic libraries.
  
The examples and tests require the following non-Python dependencies:

* PETSc_ - This can optionally be installed by pip along with petsc4py
* nlopt_ - Installed with `shared libraries enabled <http://ab-initio.mit.edu/wiki/index.php/NLopt_Installation#Shared_libraries>`_.

The above packages must be built with shared libraries enabled and present in sys.path (eg. via setting the PYTHONPATH environment variable).

Python dependencies can be seen in setup.py and include NumPy_, SciPy_ and mpi4py_. These should install     automatically if accessible when libensemble is installed (see below).

Conda can also be used for simple fast installation. This is probably the fastest approach for a clean installation from scratch as conda can install both the Python and non-Python dependencies - see conda directory for dependent packages/instructions. Note, however, that mpi4py should be configured to point to your systems MPI if that already exists. This can be checked by locating the mpi.cfg file in the mpi4py installation. Note that if PYTHONPATH is set these packages will take precedence over conda installed packages. Travis testing has also be configured to use Conda with the `Miniconda <https://conda.io/docs/install/quick.html>` distribution.

.. _PETSc:  http://www.mcs.anl.gov/petsc
.. _Python: http://www.python.org
.. _nlopt: http://ab-initio.mit.edu/wiki/index.php/NLopt
.. _NumPy:  http://www.numpy.org
.. _SciPy:  http://www.scipy.org
.. _mpi4py:  http://pythonhosted.org/mpi4py

Installation
------------

* If you have pip/pip3 installed, type the following command::

   pip3 install libensemble

- | If you are using Python 2.7 use pip instead of pip3. Depending on your
  | permissions, you might need to use ``pip install --user libensemble`` to install.

* Or you can download the source code from `here <https://github.com/shuds13/libensemble>`_, and then install the package from the top level directory using::

    python setup.py install --user
    
  OR::
    
    pip3 install . --user
    

Testsuite
---------

The testsuite includes both unit and regression tests and is run periodically on

* `Travis CI <https://travis-ci.org/shuds13/libensemble>`_

Developer info:

* The testsuite can be run using the following methods::

    ./run-tests.sh (optionally specify eg. -p 3 for Python3)
  
    python3 setup.py test

    tox - For testing multiple versions within virtual environments (see tox.ini).

* Running hooks/set-hooks.sh from the top-level directory will fire-off the tests on a *git push*. This simply sets a symbolic link to a test wrapper at .git/hooks/pre-push. To remove, simply delete the link. If set, the pre-push hook can be overriden with *git push --no-verify*. Use of this feature is down to developer preference. 

Documentation
-------------
* http://libensemble.readthedocs.org/, For full docs *to be implemented*
  
