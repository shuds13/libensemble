#!/usr/bin/env python
"""
Parallel Hello World MPI application. Each MPI process prints its rank, world
size, and host name. Used as a simple test application submitted via the
libEnsemble MPIExecutor in executor hello-world tests.
"""

if __name__ == "__main__":
    import sys

    from mpi4py import MPI

    size = MPI.COMM_WORLD.Get_size()
    rank = MPI.COMM_WORLD.Get_rank()
    name = MPI.Get_processor_name()

    sys.stdout.write("Hello, World! I am process %d of %d on %s.\n" % (rank, size, name))
