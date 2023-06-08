from mpi4py import MPI
import numpy as np 
import sys

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
    if numProcesses > 1 and numProcesses % 2 == 1:
        if myId == 0:
            print("Number of processes must be a multiple of 2")
        sys.exit(1)

    #step 1: populate global array
    #SPMD pattern 
    local = populateArray(myId, numProcesses) #populate array

    if myId == 0: #initialize global array on master process only
        global_array = np.empty(N)
    else:
        global_array = None

    #gather the local results into global_array (old code)
    comm.Gather(local, global_array, root=0)


    #step 2: compute local sums
    #now scatter the global array to each process
    comm.Scatter(global_array, local, root=0)

    #compute local sums (SPMD)
    local_sum = sum(local)

    #reduction (new change)
    finalTotal = comm.reduce(local_sum, op=MPI.SUM)


    if myId == 0:
        #print out final array
        print(finalTotal)
        print((N*(N+1)/2))


########## Run the main function
main()
