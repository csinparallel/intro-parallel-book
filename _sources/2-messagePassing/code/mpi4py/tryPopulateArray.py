from mpi4py import MPI
import numpy as np 

#array size
N = 2000000


def populateArray(rank, nprocs):

    #declare local variables:
    nElems = #number of elemes to generate
    start =  #starting element
    end =  #end element
    length = #length of array to generate

    #generate empty array
    local_array = np.empty(length)

    #fill with desired values (start+1..end+1)
    for i in range(length):
        local_array[i] = #value at index i

    return local_array



def main():
    comm = MPI.COMM_WORLD
    myId = comm.Get_rank()
    numProcesses = comm.Get_size()

    #SPMD pattern 
    local = populateArray(myId, numProcesses) #generate a local array 

    #master-worker pattern/send-receive
    if (myId != 0):    
        #send local array to master 

    else:
        #initialize global array, and fill with master's elements
        global_array = np.empty(N)

        #copy master's local array to 
        for i in range(len(local)):
            global_array[i] = local[i]
        

        #receive local arrays from each worker, 
        #and merge into global_array


        #solution check:  the two sums should be equal
        total = sum(global_array)
        print(total)
        print((N*(N+1)/2))


########## Run the main function
main()
