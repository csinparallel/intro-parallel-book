from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    numProcesses = comm.Get_size()

    if id == 0:
        hello_message = "Hello from master node!"
        print("Process {0} (master) sending messages to workers: {1}".format(\
              id, hello_message))
        
        for i in range(1,numProcesses): #send to each worker process
            comm.send(hello_message, dest=i)
    else:
        my_message = comm.recv(source=0)
        print("Process {0} (worker) received message from master: {1}".format(\
              id, my_message))

########## Run the main function
main()
