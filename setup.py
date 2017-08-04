# S.Hudson - Testing setup.py - search ***update*** for sections to complete.

#Examples:
#python3 setup install --user: - Install inc. setting up dependences
#python3 setup test:           - Run testsuite
#python3 setup tox :           - Run tox - runs test suite for multiple platforms

#pip versions
#pip3 install .: - Install with pip


# from distutils.core import setup

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
#from setuptools.extension import Extension
from setuptools.command.install import install as InstallCommand
#from Cython.Build import cythonize
from setuptools.command.test import test as TestCommand

#Force to use pip rather than easy_install
#class Install(InstallCommand):
#    """ Customized setuptools install command which uses pip. """
#
#    def run(self, *args, **kwargs):
#        import pip
#        pip.main(['install', '.'])
#        InstallCommand.run(self, *args, **kwargs)

class Run_TestSuite(TestCommand):
    def run_tests(self):
      import os
      import sys
      #import pytest
      py_version=sys.version_info[0]
      print('Python version from setup.py is', py_version)
      run_string="./run-tests.sh -p " + str(py_version)
      os.system(run_string)

class ToxTest(TestCommand):
    user_options = []

    def initialize_options(self):
        TestCommand.initialize_options(self)

    def run_tests(self):
        import tox
        tox.cmdline()

setup(
    name='libensemble',
    version='0.1.0',
    
    #ext_modules = cythonize(extensions)    

    description='Library for managing ensemble-like collections of computations',

#    cmdclass={
#        'install': Install,
#     },

    url='https://github.com/shuds13/libensemble',

    # Author: ***update*** - check official authors
    # author='Jeff Larson',
    # author_email='jmlarson@anl.gov',

    license='BSD 2-clause',

    packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. A requirements.txt file also exists for
    # specified versions (for repeatable builds).
    # For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html

    # Min/Max versions are optional - these may be too restrictive
#   install_requires=['Cython>=0.25.2',
#                      'mpi4py>=2.0.0',
#                      'numpy>=1.13.1',
#                      'petsc>=3.7.2',
#                      'petsc4py>=3.7.0',
#                      'scipy>=0.19.1'
#                      ],

#    install_requires=['Cython',
#                      'mpi4py',
#                      'numpy',
#                      'scipy'
#                      ],

#Note some of these are for pure python package - some only needed for examples or tests
#Maybe should be a separation here - for installing just libensemble src...		      
    install_requires=['Cython>=0.25',
                      'mpi4py>=2.0',
                      'numpy>=1.13',
		      'petsc>=3.7.6',
                      'petsc4py>=3.7.0',
                      'scipy>=0.19',
		      'pytest>=3.1',
                      'pytest-cov>=2.5',
		      'pytest-pep8>=1.0'
		      'tox>=2.7'
                      ],

#sh Should include - some are transient deps so pip should install
#                 pytest-cov, coverage, pytest-pep8, pytest-cache
#    setup_requires=['pytest-runner'],

#Note: These do not get permenantly installed when run python3 setup.py tests
#Just uses a temp. egg - so I suggest installing i install_requires/requirements.txt
    tests_require=['pytest',
                   'pytest-cov',
		   'pytest-pep8',
		   'tox>=2.7'
		   ],
		   
#sh pytest-profiling can be used for profiling if nec.

#Enable the fixture explicitly in your tests or conftest.py (not required when using setuptools entry points):
# pytest_plugins = ['pytest_profiling']
# testing & profiling shld be separated with diff commands here

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        #Note: This is for classification.
        #To enforce given Python versions use python_requires keyword.
    ],

    # ***update***
    # To add more attributes see sample setup.py at
    # https://github.com/pypa/sampleproject/blob/master/setup.py

    cmdclass = {'test': Run_TestSuite,
                'tox': ToxTest}
)
