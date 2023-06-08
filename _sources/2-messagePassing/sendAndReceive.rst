2.2 Point to Point Communication
--------------------------------

The fundamental basis of coordination between independent processes is point-to-point communication between processes through the communication links in the MPI.COMM_WORLD. The form of communication is called message passing, where one process **sends** data to another one, who in turn must **receive** it from the sender. This is illustrated as follows:

.. image:: images/send_recv.png

Point-to-point communication is a way that pair of processors transmits the data between one another, one processor sending, and the other receiving. MPI provides ``Send()`` and ``Receive()`` functions that allow point-to-point communication taking place in a communicator. For general Python objects, use the 
lowercase ``send()`` and ``receive()`` functions instead. ::

  Send(message, destination, tag)

    - message:  numpy array containing the message
    - destination:  rank of the receiving process
    - tag:    message tag is a way to identify the type of a message (optional)

  Recv(message, source, tag)
    - message: numpy array containing the message
    - source: rank of the sending process 
    - tag: message tag is a way to identify the type of a message

.. note:: The ``send()`` and ``recv()`` functions have identical form, except that the ``message`` parameter could be a standard Python type (e.g. int, string, float etc.). Be sure to use the uppercase form and ``numpy`` arrays whenever dealing with list-like data!


Send and Receive Hello World
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: code/mpi4py/sendReceive.py
  :language: python


This MPI program illustrates the use of ``send()`` and ``recv()`` functions. Notice that we use the lowercase version of the Send/Receive functions due to the 
fact that the message being sent is of type ``String``. 

The above program can be run using the following command:

.. code-block:: bash

   python run.py ./sendReceive.py 4


Integration - First Attempt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The code listing below illustrates how the integration example could be implemented with point-to-point communication:

.. literalinclude:: code/mpi4py/integration.py
  :language: python

The ``trapSum()`` function computes and sums up a set of *n* trapezoids with a particular range. The first part of the ``main()`` function 
follows the SPMD pattern. Each process computes its local range of trapezoids and calls the 
``trapSum()`` function to compute its local sum.


The latter part of the ``main()`` function follows the master-worker pattern. Each worker process sends its local sum to the master 
process. The master process generates a global array (called ``results``), receives the local sum from each worker process, and stores 
the local sums in the ``results`` array. A final call to the ``sum()`` functon adds all the local sums together to produce the final result. 

In later sections, we will see how to improve this example with other communication constructs. For now, ensure that you are comfortable 
with the workings of this program. You can execute it with the command:

.. code-block:: bash

   python run.py ./integration.py 4

(multiple choice about why master worker pattern must be used, and why results cannot be shared)


Exercise - Populate an Array
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As an exercise, let's use point-to-point communication to populate an array in parallel. The algorithm is as follows:

* Each process computes its local range of values, and then calls a function that generates an array of just those values.
* Each worker process sends its array to the master process. 
* The master process generates a master array of the desired length, receives the local array from workers, and then populates 
  the master array with the elements of the local arrays received.

The following program is a partially filled in solution, with the algorithm shown in comments. 

.. literalinclude:: code/mpi4py/tryPopulateArray.py
  :language: python

Fill in the rest of the program, save as ``tryPopulateArray.py`` and test your program using the following commands:

.. code-block:: bash

   python run.py ./tryPopulateArray.py 1
   python run.py ./tryPopulateArray.py 2
   python run.py ./tryPopulateArray.py 4

Remember, in order for a parallel program to be correct, it should return the same value with every run, and regardless of the number of 
processes chosen. Click the button below to see the solution.

.. reveal:: reveal-popArray
    :showtitle: Reveal Content
    :hidetitle: Hide Content

    The following program demonstrates how to implement the populateArray program. Make sure you try to solve the exercise yourself 
    before looking at the solution!

    .. literalinclude:: code/mpi4py/populateArray.py


Ring of passed messages
^^^^^^^^^^^^^^^^^^^^^^^

Another pattern that appears in message passing programs is to use a ring of processes: messages get sent in this fashion:

.. image:: images/ring.png


When we have 4 processes, the idea is that process 0 will send data to process 1, who will receive it from process 0 and then send it to process 2, who will receive it from process 1 and then send it to process 3, who will receive it from process 2 and then send it back around to process 0.

**Program file:** 07messagePassing5.py

.. literalinclude:: code/mpi4py/07messagePassing3.py
  :language: python
  :lines: 22-

**Exercise:**

Run the above program varying the number of processes for *N* = 1 through 8/

.. code-block:: bash

   python run.py ./07messagePassing3.py N


Compare the results from running the example to the code above. Make sure that you can trace how the code generates the output that you see.


**Exercise:**

.. mchoice:: mc-mp-ring
   :answer_A: The last process with the highest id will have 0 as its destination because of the modulo (%) by the number of processes.
   :answer_B: The last process sends to process 0 by default.
   :answer_C: A destination cannot be higher than the highest process.
   :correct: a
   :feedback_A: Correct! Note that you must code this yourself.
   :feedback_B: Processes can send to any other process, including the highest numbered one.
   :feedback_C: This is technically true, but it is important to see how the code ensures this.

   How is the finishing of the 'ring' completed, where the last process determines that it should send back to process 0?