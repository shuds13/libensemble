#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from setuptools.command.install import install as InstallCommand
from setuptools.command.test import test as TestCommand

class Run_TestSuite(TestCommand):
    def run_tests(self):
        import os
        import sys
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
    url='https://github.com/libensemble/libensemble',
    author='Jeff Larson',
    author_email='jmlarson@anl.gov',
    license='BSD 2-clause',
    packages=['libensemble'],
    package_dir={'libensemble'  : 'code/src'},

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
       
    # Enable the fixture explicitly in your tests or conftest.py
    # pytest_plugins = ['pytest_profiling']
        
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

    cmdclass = {'test': Run_TestSuite,
                'tox': ToxTest}
)
