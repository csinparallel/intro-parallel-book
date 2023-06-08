from mpi4py import MPI
import numpy as np 

#array size
N = 2000000


def populateArray(rank, nprocs):

    nElems = N/nprocs #number of elemes to generate
    isTail = N % nprocs

    start = rank*nElems
    end = (rank+1)*nElems
    if rank == (nprocs-1) and isTail > 0:
        end = N

    length = end-start

    local_array = np.empty(length)
    for i in range(length):
        local_array[i] = 1+start+i
    return local_array



def main():
    comm = MPI.COMM_WORLD
    myId = comm.Get_rank()
    numProcesses = comm.Get_size()

    #SPMD pattern 
    local = populateArray(myId, numProcesses) #generate an empty array of size N

    if myId == 0: #initialize global array on master process only
        global_array = np.empty(N)
    else:
        global_array = None

    #gather the local results into global_array
    comm.Gather(local, global_array, root=0) 

    if myId == 0:
        #print out final array
        total = sum(global_array)
        print(total)
        print((N*(N+1)/2))


########## Run the main function
main()
