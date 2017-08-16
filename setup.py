# S.Hudson - Testing setup.py - search ***update*** for sections to complete.
# ***update*** On merge - must update shuds13/libensemble to libensemble/libensemble
#Examples:
#python3 setup install --user: - Install inc. setting up dependences
#python3 setup test:           - Run testsuite
#python3 setup tox :           - Run tox - runs test suite for multiple platforms

#pip versions
#pip3 install .: - Install with pip

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand
from setuptools.command.test import test as TestCommand

#from setuptools.extension import Extension
#from Cython.Build import cythonize

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
    description='Library for managing ensemble-like collections of computations',
    url='https://github.com/shuds13/libensemble',
    author='Jeff Larson',
    author_email='jmlarson@anl.gov',
    license='BSD 2-clause',
    packages=['libensemble'],
    package_dir  = {'libensemble'  : 'code/src'},

    install_requires=['Cython>=0.24',
                      'mpi4py>=2.0',
                      'numpy>=1.13',
		      'petsc>=3.7.6',
                      'petsc4py>=3.7.0',
                      'scipy>=0.17',
		      'pytest>=3.1',
                      'pytest-cov>=2.5',
		      'pytest-pep8>=1.0'
		      'tox>=2.7'
                      ],

    tests_require=['pytest',
                   'pytest-cov',
		   'pytest-pep8',
		   'tox>=2.7'
		   ],
		   
    #Enable the fixture explicitly in your tests or conftest.py
    # (not required when using setuptools entry points):
    # pytest_plugins = ['pytest_profiling']
    
    
    #***update*** MUST CHECK
    #             author/author email/classifiers - inc. platforms/status etc...

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English', 	
        'Operating System :: Linux',
        'Operating System :: Unix',	       
	'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: C',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',	
    ],

    # ***update***
    # To add more attributes see sample setup.py at
    # https://github.com/pypa/sampleproject/blob/master/setup.py

    cmdclass = {'test': Run_TestSuite,
                'tox': ToxTest}
)
