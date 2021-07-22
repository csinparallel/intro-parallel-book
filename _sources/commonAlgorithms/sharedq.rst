
3.4 Shared Queue
-----------------

In this section, we will see how to make a process and how to communicate between processes via a **shared queue**, a special type of data data structure 
through which processes can communicate with each other. Recall that a queue is a first-in-first-out (FIFO) data structure. The queue is *shared* in that each process has access to the same queue structure.

After giving an overview of the multiprocessing module, we will then practice computing the greatest common divisor (GCD) of many pairs of numbers through an unplugged activity, and finally develop code using the multiprocessing module to perform this task more quickly with parallelism.

.. note:: 
   The ``multiprocessing`` library is not yet supported Runestone activeCode blocks. As such, you will not be able to run code interactively in this 
   section. We recommend that you copy these code examples to your computer and follow along.

The Python multiprocessing module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Python multiprocessing module comes with the standard Python distribution. It allows for parallelism through the creation and management of multiple processes in a Python program. To create a worker process, we must first instantiate the ``Process`` class. The process specifies a function to execute via the ``target`` formal parameter, and the arguments to the target function via the ``args`` formal parameter. Consider the "hello world"-style code below, which specifies a target function called ``sayHi`` which receives the single argument ``i``:

.. multiprocessing is not supported by activeCode blocks -- using literal code blocks instead

.. literalinclude:: code/helloEx.py
   :language: python
   :emphasize-lines: 9, 12-13
   :linenos:

.. note::
    * In line 9, there are no parentheses after ``sayHi``, because we are not actually calling the function there. Rather, we are passing the ``sayHi1`` function as an *argument* to the ``Process`` constructor, taking advantage of the fact that functions are first-class in Python.

    * In line 9, the ``args`` formal parameter must be a tuple. A tuple in Python is an immutable list, and is created using parentheses. To make a tuple with just one value (``i`` in this case), we must include the trailing comma. Otherwise, we would just have ``(i)``, which the interpreter would consider a parenthesized version of the expression ``i``, rather than a tuple.

    * It is essential that we include lines 12 and 13 in this code. If we only had line 13 (without the if), then each worker process would also try to execute main, leading to workers creating workers, which would create more workers, and so on…
 
 After creating Process object ``p``, we simply call the start method on it to start the process. Each process, once started, runs the ``sayHi`` function with the provided id value passed in to the constructor via the ``args`` formal parameter. 
 .. what happens when the code is run? Add a sentence. 

Creating a shared queue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
A shared queue can be created by calling the 0-argument ``Queue`` constructor. It can then be passed to each process via the ``Process`` constructor’s ``args`` formal parameter. The blocking ``put`` and ``get`` methods can then be used to put data on the queue and remove data from the queue, respectively.

For example, consider the code below:

.. literalinclude:: code/queueEx.py
   :language: python
   :linenos:

Here, the main process creates the ``Queue`` object and passes it to each of two worker processes. When the workers start executing the ``parrotSpeak`` function, there is not yet anything on the queue, and so they both block on the ``q.get()`` call on line 5. After a pause on line 32, the main process begins putting data on the queue. The two workers race to get each message. The 0.1 second ``sleep`` in the ``parrotSpeak`` function makes it more likely that the race winner will vary even with such a small set of messages.

Since this is a shared queue, values are “getted” off the queue in the same order they are “putted” on the queue. Note, however, that due to a race condition, it is possible that the worker processes won’t actually complete the processing of a value in this same order.

Note also the two ``"DONE"`` strings at the end of the messages list. These two sentinels are used to tell each worker when to stop calling get to obtain more messages. There are other approaches that can be used instead, but this approach is simple and effective.


Unplugged activity
^^^^^^^^^^^^^^^^^^^^^^

Let’s practice the use a shared queue through an unplugged activity. In this activity, we’ll compute the greatest common divisor (GCD). Recall that the GCD of two positive integers is the highest number that goes evenly into both numbers. For example, the GCD of 24 and 36 is 12, because 24/12 = 2 and 36/12 = 3, and there is no number larger than 12 that divides both numbers evenly. If you’re uncertain how to compute the GCD, for now just do your best by choosing relatively small positive integers and seeing with a calculator if they divide both numbers. We’ll see a better algorithm soon.

Roles (minimum 5 people) and items needed:
    * 1 main process (1 sheet of paper and one writing utensil)
    * 2 - 4 workers (1 sheet of paper, one writing utensil, and one calculator, each)
    * 1 input queue (1 writing utensil)
    * 1 output queue (1 sheet of paper and one writing utensil)

Each of the four workers should sit in separate corners of the room. The main process and both queues will stay in the middle of the room.

Main process procedure:
    1. Fill out one line at a time on a sheet of paper. Each line should contain two randomly chosen two-digit positive integers. Write 7 lines of numbers in this manner.
    2. Give this sheet of paper to the input queue.
    3. Tell the workers to begin their procedures.

Worker procedure:
    1. Say “get” to the input queue and wait until there is a response from the input queue (ignore verbal responses to other workers)
    2. While the input queue has not said “done”:
        a. Write down the pair of numbers received
        b. Compute the greatest common divisor (GCD) of the two numbers.
        c. Say “put” to the output queue and wait until the output queue acknowledges you.
        d. Tell the output queue the pair of numbers and their GCD.
        e. Say “get” to the input queue and wait until there is a response from the input queue (ignore verbal responses to other workers)
        f. Loop back up to step 2

Input queue procedure:
    1. Receive a sheet of paper from the main process, with pairs of numbers.
    2. Wait for a “get” message from a worker.
        a. When received, give the worker a pair of non-crossed-out numbers, and cross out the numbers given.
        b. If multiple requests come in simultaneously, handle them one at a time, with distinct pairs of numbers for each request.
        c. If there are no more numbers when a worker requests some, say “done” to that worker.

Output queue procedure:
    1. Start with a blank sheet of paper.
    2. Wait for messages:
        a. “put” (from a worker): Receive the worker’s three numbers and write them on the highest blank line on the paper.
        b. “get” (from the main process): Tell the main process the three values on the highest non-crossed-out line of the blank paper, and then cross out that line.
            i. If a get message comes when no values are on the paper, tell the main process to do nothing until you respond later with three numbers.
        c. If multiple requests come in simultaneously, handle them one at a time.


In the unplugged activity above, very little synchronization between the workers is needed. Only one worker can access a queue at a time, but otherwise each worker is free to work as quickly or slowly as needed. If each task (computing the GCD) is enough work to justify potentially waiting briefly for queue access, the parallel approach will show speedup over a sequential approach.

Translating it to code
^^^^^^^^^^^^^^^^^^^^^^^^^

The unplugged activity could be implemented directly in code. However, computing the GCD, even of very large numbers, is a fast operation. To see why this is a bit of a problem, imagine if the unplugged activity asked workers to add 1 to each of the provided numbers, instead of computing the GCD. The workers would be saying “get” and “put” much more frequently, and so the proportion of time spent waiting for queue access, instead of calculating, would grow.

A similar situation would occur if we were to program the unplugged activity as is. GCD is easy for a computer to compute quickly. To make the overhead of the shared queue worthwhile, then, we need to increase the amount of work required per task. We can easily accomplish this by having each worker request not just a single pair of numbers, but rather a block of many pairs of numbers. Only when the worker has handled the entire block will it put all results on the output queue and get another block from the input queue.

We will now write the corresponding code in Python. Consider the provided code, with blanks:

.. literalinclude:: code/gcdWithBlanks.py
   :language: python
   :linenos:

The code begins running in the if block at the bottom. Sequential and parallel versions of the code are run and compared.

In the sequential version of the code, the main process does everything:
    • buildInputs creates NUM_BLOCKS blocks of numbers, with PAIRS_PER_BLOCK pairs of numbers in each block. The numbers range from MIN_VALUE to MAX_VALUE.
    • computeGCDs is then called, which gets one block at a time from inputQ, then one pair at a time from the current block. It computes the GCD by calling the provided gcd function (an implementation of Euclid’s algorithm), and appends the results to a blockOutput variable. When the block is fully processed, the results for the block are put on the output, and a new block is obtained.
    • processOutputs is then called, which simply obtains one output at a time. If VERBOSE is true, then all results will be printed. Otherwise, nothing is really done to “process” the outputs beyond simply obtaining them, but this function simulates what would be done as the next step in a larger application.

Study the sequential code as best as you can before moving forward. The great news is that the parallel code uses exactly the same functions! The only difference is that the main process creates NUM_WORKERS child processes that will each do the work in parallel.

The code contains many blanks. Fill in the blanks to complete the implementation.

<gcd.py is the answer key>



