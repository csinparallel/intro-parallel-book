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

    #master-worker pattern/send-receive
    if (myId != 0):    
        comm.send(local, dest=0)

    else:
        #initialize global array, and fill with master's elements
        global_array = np.empty(N)
        for i in range(len(local)):
            global_array[i] = local[i]
        pos = len(local)

        #merge into one array
        for i in range(1, numProcesses):
            loc = comm.recv(source=i)

            for j in range(len(loc)):
                global_array[pos+j] = loc[j]
            pos += len(loc) 


        #print out final array
        total = sum(global_array)
        print(total)
        print((N*(N+1)/2))


########## Run the main function
main()
