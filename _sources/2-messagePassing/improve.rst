2.4 Other Communication Patterns
---------------------------------

There are many cases when a master process obtains or creates data that needs to be sent or 
received from all the other processes. In this section, we will discuss some special 
communication constructs specifically for those purposes.

Broadcast
^^^^^^^^^

A **broadcast** sends data from one process to all other processes. A common use of boradcasting is to send user input to all the processes in a 
parallel program, as shown in the program below:


**Program file:** 09broadcastUserInput.py

.. literalinclude:: code/mpi4py/09broadcastUserInput.py
  :language: python
  :lines: 29-

To run the above example use the following command:

.. code-block:: bash

   python run.py ./09broadcastUserInput.py N dataString


Here the ``N`` signifies the number of processes to start up in MPI, which must be greater than one. The ``dataString`` must be supplied and represents the string that will be broadcast from the master process to the workers.

For example, in this special instance, you can send a string with spaces and other special characters it it in it like this:

.. code-block:: bash

   python run.py ./09broadcastUserInput.py 2 "hello\ world\!"


**Exercise:**

* Run, using N = from 1 through 8 processes, with a string of your choosing.

* Find the place in this code where the data is being broadcast to all of the processes. Match the prints to the output you observe when you run it.



Broadcasting a list
~~~~~~~~~~~~~~~~~~~~

It is also possible to broadcast more complex data structures, like a list. The following program illustrates how to broadcast a list to every 
process:

**Program file:** 11broadcastList.py

.. literalinclude:: code/mpi4py/11broadcastList.py
  :language: python
  :lines: 24-


To run the above example use the following command (``N`` signifies the number of processes):

.. code-block:: bash

   python run.py ./11broadcastList.py N


**Exercise:**

- Run, using N = from 1 through 8 processes.




Scatter and Gather
^^^^^^^^^^^^^^^^^^

There are often cases when each process can work on some portion of a larger data structure. This can be carried out by having the master process maintain the larger structure and send parts to each of the worker processes, keeping part of the structure on the master. Each process then works on their portion of the data, and then the master can get the completed portions back.

This is so common in message passing parallel processing that there are two special collective communication functions called ``Scatter()`` and ``Gather()`` that handle this.

The mpi4py Scatter function, with a capital S, can be used to send portions of a larger array on the master to the workers, like this:

.. image:: images/Scatter_array.png

|

The result of doing this then looks like this, where each process has a portion of the original that they can then work on:

.. image:: images/after_Scatter_array.png

|

The reverse of this process can be done using the Gather function.

In this example, a 1-D array is created by the master, then scattered, using Scatter (capital S). After each smaller array used by each process is changed, the Gather (capital G) function brings the full array with the changes back into the master.

.. note:: In the code below, note how all processes must call the Scatter and Gather functions.

**Program file:** 16ScatterGather.py

.. literalinclude:: code/mpi4py/16ScatterGather.py
  :language: python
  :lines: 24-


**Example usage:**

.. code-block:: bash

   python run.py ./16ScatterGather.py N


**Exercises:**

- Run, using N = from 2 through 8 processes.
- If you want to study the numpy part of the code, look up the numpy method ``linspace()`` used in ``genArray()``.


Applying Gather to PopulateArray
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's use the ``Gather()`` function to simplify the code in the PopulateArray program. The revised code is shown below:

**Program file:** PopulateArrayGather.py

.. literalinclude:: code/mpi4py/populateArrayGather.py
  :language: python

Notice that the Send/Receive pattern used in the Point-to-Point communication section have now been replaced with 
a single ``comm.Gather()`` statement. Additional code however is needed to initialize the global array that holds 
the final results. 

Run this code using the following command (N is the number of processes):

.. code-block:: bash

   python run.py ./populateArrayGather.py N

Even as we increase the number of processes, the result stays the same. 

**Exercises** 

- Modify the PopulateArrayGather program to do array addition. Each processor should compute a local *sum* of the array it produces. The global array should be 
  the length of the number of processes, since the ``Gather()`` function is gathering a number of sums. 
- Modify the Integration example frome earlier to use the ``Gather()`` function.



Reduction
^^^^^^^^^

There are often cases when every process needs to complete a partial result of an overall computation. For example if you want to process a large set of numbers by summing them together into one value (i.e. *reduce* a set of numbers into one value, its sum), you could do this faster by having each process compute a partial sum, then have all the processes communicate to add each of their partial sums together.

This is so common in parallel processing that there is a special collective communication function called **reduce** that does just this.

The type of reduction of many values down to one can be done with different types of operators on the set of values computed by each process.

Reduce all values using sum and max
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In this example, every process computes the square of (id+1). Then all those values are summed together and also the maximum function is applied.

**Program file:** 12reduction.py

.. literalinclude:: code/mpi4py/12reduction.py
  :language: python
  :lines: 23-



**Example usage:**

.. code-block:: bash

   python run.py ./12reduction.py N


**Exercises:**

- Run, using N = from 1 through 8 processes.
- Try replacing MPI.MAX with MPI.MIN(minimum) and/or replacing MPI.SUM with MPI.PROD (product). Then save and run the code again.
- Find the place in this code where the data computed on each process is being reduced to one value. Match the prints to the output you observe when you run it.



Reduction on a list of values
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can try reduction with lists of values, but the behavior matches Python semantics regarding lists.

.. note:: There are two ways in Python that you might want to sum a set of lists from each process: 1) concatenating the elements together, or 2) summing the element at each location from each process and placing the sum in that location in a new list. In the latter case, the new list is the same length as the original lists on each process.


**Program file:** 13reductionList.py

.. literalinclude:: code/mpi4py/13reductionList.py
  :language: python
  :lines: 27-


**Example usage:**

.. code-block:: bash

   python run.py ./13reductionList.py N


**Exercises:**

- Run, using N = from 1 through 4 processes.
- Uncomment the two lines of runnable code that are commented in the main() function. Observe the new results and explain why the MPI.SUM (using the + operator underneath) behaves the way it does on lists, and what the new function called sumListByElements is doing instead.
- In this code, try to explain what the function called sumListByElements does. If you are unfamiliar with the zip function, look up what it does.


Returning to the Array Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Let's return to the problem of array addition, where the goal is to sum all the elements in an array together in parallel. We build on our earlier PopulateArray 
program. After populating the array in parallel, we will use the ``scatter()`` method first to re-distribute the contents of the ``global_array`` to each 
process:

.. literalinclude:: code/mpi4py/arrayAddition1.py
  :language: python
  :lines: 45-55

Here, the ``local`` array is overwritten with the scattered results of ``global_array``. Each process then computes its local sum (stored in ``local_sum``). 


Computing the final total using Gather
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to compute the final total is to use a second invocation of the ``Gather()`` function as shown below:

.. literalinclude:: code/mpi4py/arrayAddition1.py
  :language: python
  :lines: 45-70


The master process allocates a new array called ``all_sums``, which is then populated by a second ``Gather()`` call. Finally, the master process computes 
the final total by summing together all the subtotals located in the ``all_sums`` array. 


Computing the final total using Reduce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recall that the ``Reduce()``  function combines all the local values using a common function (i.e. Sum, Max, Min, Prod). Since our goal is to add together 
all the elments of our array, we can use the ``Reduce()`` function as follows:

.. literalinclude:: code/mpi4py/arrayAddition2.py
  :language: python
  :lines: 45-64

In addition to being shorter, this code snippet is much simpler than the one employing ``Gather``, as all the master process is doing is printing out the result.

**Exercise:**

.. mchoice:: arrayAdd_compare
   :answer_A: The version using Gather is faster than the version using Reduce.
   :answer_B: Both implementations perform about the same.
   :answer_C: The version using Reduce is faster than the version using Gather.
   :correct: c
   :feedback_A: No. Ensure that the Gather version uses Gather to collect the sums. 
   :feedback_B: No. Did you time each implementation?
   :feedback_C: Correct! Not only is version employing Reduce shorter and simpler, it is much faster.

   Add timing code and compare the performance of array Addition example employing Gather vs. Reduce. How do they compare?

**Exercise:**

Now modify the integration example to use ``Reduce()``. Compare the performance of the integration example with the earlier one that uses ``Gather()``. Which is faster?