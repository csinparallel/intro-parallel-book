2.1 First Steps - Programming with Message Passing
---------------------------------------------------

The Message Passing Interface (MPI) is an industry standard passing messages between *processes* in a distributed memory system. MPI is supported 
by a variety of languages, and is widely used for parallel programming. On a multicore system, MPI enables multiple processes to communicate with 
each other. On a distributed memory system (or cluster), one node is specified as the **master node** (or head node), while the other nodes are 
known as **worker nodes**. MPI allows programmers to divide up a task and distribute a component to each worker or to some subset of workers. 
Thus, each node can work on its own sub-task simultaneously.

In this chapter, we use the Python library *mpi4py* to introduce message passing and MPI. The mpi4py library of functions has several collective communication functions that are designed to work with arrays created using the Python library for numerical analysis computations called *NumPy*. As such, all examples involving lists employ NumPy arrays. Unlike Python lists, NumPy arrays hold only one type of data, and generally are faster and take up less space than 
Python lists that contain data of only one type. NumPy arrays are specifically designed for fast mathematical computations and can be reshaped to form matrices 
and other multi-dimensional data structures. A detailed discussion of numpy is beyond the scope of this book; for more about its features and available methods, we recommend consulting the `documentation <https://numpy.org/devdocs/>`_ and `available tutorials <https://www.python-course.eu/numpy.php>`_.


The SPMD Pattern
^^^^^^^^^^^^^^^^
One of the foundational patterns in message passing is the **single program multiple data (SPMD)** pattern, where each process executes the same program, but 
on different units of data. The following program illustrates the concept of SPMD, where each process contains and produces its own small bit of data 
(in this case printing something about itself).

.. literalinclude:: code/mpi4py/00spmd.py
  :language: python
  :lines: 23-

Let's look at each line in main() and the variables used:

1. ``comm`` The fundamental notion with this type of computing is a **process** running independently on the computer. With one single program like this, we can specify that we want to start several processes, each of which can **communicate**. The mechanism for communication is initialized when the program starts up, and the object that represents the means of using communication between processes is called MPI.COMM_WORLD, which we place in the variable comm.

2. ``id`` Every process can identify itself with a number. We get that number by asking ``comm`` for it using the ``Get_rank()`` function.

3. ``numProcesses`` It is helpful to know haw many processes have started up, because this can be specified differently every time you run this type of program. Asking ``comm`` for it is done with the ``Get_size()`` function.

4. ``myHostName`` When you run this code on a cluster of computers, it is sometimes useful to know which computer is running a certain piece of code. A particular computer is often called a *host*, which is why we call this variable ``myHostName``, and get it by asking ``comm`` to provide it with the ``Get_processor_name()`` function.

These four variables are often used in every MPI program. The first three are often needed for writing correct programs, and the fourth one is often used for debugging and analysis of where certain computations are running.

The fundamental idea of message passing programs can be illustrated like this:

.. image:: images/comm_world.png

Each process is set up within a communication network to be able to communicate with every other process via communication links. Each process is set up to have its own number, or id, which starts at 0.

.. note:: Each process holds its own copies of the above 4 data variables. **So even though there is one single program, it is running multiple times in separate processes, each holding its own data values.** This is the reason for the name of the pattern this code represents: single program, multiple data. The print line at the end of ``main()`` represents the multiple different data output being produced by each process.

You can run the above program (stored in ``00spmd.py``) using the following command:

.. code-block:: bash

    python run.py ./00spmd.py 4

In this chapter, we use the wrapper file ``run.py`` to execute the Python program using the general ``mpirun`` command. The ``4`` 
signifies that the program will be run with ``4`` processes.


The Master-Worker Pattern
^^^^^^^^^^^^^^^^^^^^^^^^^

The **master-worker** is one of the most common patterns used in message passing programs. One node (designated the **master**) doles out tasks to a 
series of **worker** nodes that complete their assigned tasks and return the results (if any) to the master.  

.. literalinclude:: code/mpi4py/01masterWorker.py
  :language: python
  :lines: 23-


Run the program using the following command:

.. code-block:: bash

    python run.py ./01masterWorker.py 4


What is different between this example and the previous one?


**Exercises:**

- Rerun, using varying numbers of processes from 1 through 8 (i.e., vary the last argument to run.py).
- Explain what stays the same and what changes as the number of processes changes.


The answer to the above question illustrates what we can do with this pattern: based on the process id, we can have one process carry out something different than the others. This concept is used a lot as a means to coordinate activities, where one process, often called the master, has the responsibility of handing out work and keeping track of results. We will see this in later examples.

.. note:: By convention, the master coordinating process is usually the process number 0.