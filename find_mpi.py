import os
import mpi4py

path=mpi4py.__path__[0]
print("mpi4py path found is", path)

configfile=os.path.join(path,"mpi.cfg")

#print(os.path.join(path,"mpi.cfg"))

with open(configfile, 'r') as confile_handle:
    print(confile_handle.read())
