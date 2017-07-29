# S.Hudson - Testing setup.py - search ***update*** for sections to complete.

# from distutils.core import setup

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
#from setuptools.extension import Extension
from setuptools.command.install import install as InstallCommand
#from Cython.Build import cythonize

#Force to use pip rather than easy_install
#class Install(InstallCommand):
#    """ Customized setuptools install command which uses pip. """
#
#    def run(self, *args, **kwargs):
#        import pip
#        pip.main(['install', '.'])
#        InstallCommand.run(self, *args, **kwargs)

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

    # ***update*** Min/Max versions are optional - these may be too restrictive
    #Note - by default uses easy_install - may be pref. to use pip3 install ...
#   install_requires=['Cython>=0.25.2',
#                      'mpi4py>=2.0.0',
#                      'numpy>=1.13.1',
#                      'petsc>=3.7.2',
#                      'petsc4py>=3.7.0',
#                      'scipy>=0.19.1'
#                      ],

    install_requires=['Cython',
                      'mpi4py',
                      'numpy',
                      'petsc4py',
                      'scipy'
                      ],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        #Note: This is for classification.
        #To enforce given Python versions use python_requires keyword.
    ],

    # ***update***
    # To add more attributes see sample setup.py at
    # https://github.com/pypa/sampleproject/blob/master/setup.py

)
