from mpi4py import MPI
import math

#constants
n = 1048576 #number of trapezoids = 2**20

def f(x):
    return math.sin(x)

def trapSum(my_a, my_b, my_n, h):
    my_a*=h 
    my_b*=h
    total = (f(my_a) + f(my_b))/2.0 #initial value
    for i in range(1, my_n): #for each trapezoid
        total += f(my_a+i*h)
    return total*h

def main():
    comm = MPI.COMM_WORLD
    id = comm.Get_rank()
    numProcesses = comm.Get_size()
    
    #desired range    
    a, b = 0, math.pi

    #all processes: compute local variables
    local_n  = n/numProcesses #num trapezoids per process
    start  = id*local_n #starting trapeziod
    end = (id+1)*local_n #ending trapezoid
    if id == numProcesses-1: #in case processors don't divide things evenly
        end = n
    h = (b-a)/n #width of trapezoid (scaling factor)

    #all processes: calculate local sum
    my_sum = trapSum(start, end, local_n, h)

    if id != 0: #if a worker process       
        comm.send(my_sum, dest=0) #send master the sum

    else: #master process
        results = [0.0]*numProcesses #generate master list to hold results 
        results[0] = my_sum #places master's local sum in first element

        for i in range(1,numProcesses):
            other_sum = comm.recv(source=i) #get local sums from other processes
            results[i] = other_sum #place in result array

        print("Done receiving all messages")
        print("Final sum is {0}".format(sum(results)))


########## Run the main function
main()
