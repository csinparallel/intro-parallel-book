
3.4 Shared Queue
-----------------

Author: Steven Bogaerts, DePauw University


In this section, we will see how to make a process and how to communicate between processes via a **shared queue**. Recall that a queue is a first-in-first-out (FIFO) data structure. The queue is *shared* in that each process has access to the same queue structure. The Python multiprocessing module uses the shared queue data structure to allow processes to pass messages to each other.

After giving an overview of the Python multiprocessing module, we will then practice computing the greatest common divisor (GCD) of many pairs of numbers through an unplugged activity, and finally develop code using the multiprocessing module to perform this task more quickly with parallelism.

.. note:: 
   The ``multiprocessing`` library is not yet supported Runestone activeCode blocks. As such, you will not be able to run code interactively in this section. We recommend that you copy these code examples to your computer and run them locally to complete this section.

The Python multiprocessing module
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The Python multiprocessing module comes with the standard Python distribution. It allows for parallelism through the creation and management of multiple processes in a Python program. To create a worker process, we must first instantiate the ``Process`` class. The process specifies a function to execute via the ``target`` formal parameter, and the arguments to the target function via the ``args`` formal parameter. Consider the "hello world"-style code below, which specifies a target function called ``sayHi`` which receives the single argument ``i``:

.. multiprocessing is not supported by activeCode blocks -- using literal code blocks instead

.. literalinclude:: code/helloEx.py
   :language: python
   :emphasize-lines: 9, 12-13
   :linenos:

.. note::
   * In line 9, there are no parentheses after ``sayHi``, because we are not actually calling the function there. Rather, we are passing the ``sayHi`` function as an *argument* to the ``Process`` constructor, taking advantage of the fact that functions are first-class in Python.

   * In line 9, the ``args`` formal parameter must be a tuple. A tuple in Python is an immutable list, and is created using parentheses. To make a tuple with just one value (``i`` in this case), we must include the trailing comma. Otherwise, we would just have ``(i)``, which the interpreter would consider a parenthesized version of the expression ``i``, rather than a tuple.

   * It is essential that we include lines 12 and 13 in this code. If we only had line 13 (without the if), then each worker process would also try to execute main, leading to workers creating workers, which would create more workers, and so on... 

   * After creating Process object ``p``, we simply call the start method on it to start the process. Each process, once started, runs the ``sayHi`` function with the provided id value passed in to the constructor via the ``args`` formal parameter. 

.. mchoice:: sq-mc-a
   :answer_a: The greetings will be printed in a completely random order.
   :answer_b: The greetings will be printed in mixed-up order, but generally we can expect lower-numbered processes to tend to print before higher-number processes.
   :answer_c: The greetings will always be printed exactly in numerical order.
   :correct: b
   :feedback_a: Try again: The greetings will be mixed-up, yes, but note that there is an order in which the processes are started.
   :feedback_b: Correct! The greetings will be mixed-up due to the processes racing to print, but the lower-numbered processes are started first, so they'll tend to print first. Each process will say "Hello from" followed by its provided id, from 0 to 19.
   :feedback_c: Try again: With processes running simultaneously, the actual order of printing will vary from one run to the next.

   Which of the following do you think is true about the output of the above code?

Creating a shared queue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
One way that processes can communicate is by putting and getting values into and out of a shared queue data structure. A shared queue can be created by calling the ``Queue`` constructor, which has no arguments. It can then be passed to each process via the ``Process`` constructor’s ``args`` formal parameter. The blocking ``put`` and ``get`` methods can then be used to put data on the queue and remove data from the queue, respectively.

For example, consider the code below. Here, two worker processes play the roles of two parrots, speaking (printing) sentences provided by the main process. The sentences are passed to the worker processes via a shared queue.

.. literalinclude:: code/queueEx.py
   :language: python
   :linenos:

The main process creates the ``Queue`` object and passes it to each of two worker processes. When the workers start executing the ``parrotSpeak`` function, there is not yet anything on the queue, and so they both block on the ``q.get()`` call on line 5. After a pause on line 32, the main process begins putting data on the queue. The two workers race to get each message. The 0.1 second ``sleep`` in the ``parrotSpeak`` function makes it more likely that the race winner will vary even with such a small set of messages.

Since this is a shared queue, values are "getted" off the queue in the same order they are "putted" on the queue. Note, however, that due to a race condition, it is possible that the worker processes won’t actually *complete* the processing of a value in this same order.

Note also the two ``"DONE"`` strings at the end of the messages list. These two sentinels are used to tell each worker when to stop calling ``get`` to obtain more messages. There are other approaches that can be used instead, but this approach is simple and effective.

View the video below in full-screen to see this program in action.

.. video:: video-shared-queue
   :controls:
   :thumb: images/thumbnail-shared-queue.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/filling_array.mov

.. NOTE: The above .mov file is just a placeholder! It should be replaced with the video-shared-queue.mp4 file.
.. I'm also not sure why the thumbnail image doesn't show up.

.. mchoice:: sq-mc-b
   :answer_a: The process ordering will often be different.
   :answer_b: The message ordering might be different.
   :answer_c: It is possible for the same process to print twice in a row.
   :answer_d: It is possible for the same message to be printed twice in a row.
   :correct: d
   :feedback_a: Try again: This statement is actually true. The worker processes are racing to get and print messages, and so the order of process execution may vary.
   :feedback_b: Try again: This statement is actually true. Usually message ordering will be the same because printing occurs immediately after getting, in a short period of time compared to the sleep call. But there is a slight chance that a process is interrupted between the get and print, thus changing the message ordering.
   :feedback_c: Try again: This statement is actually true. Even with the brief sleep, it is possible for one process to continue running long enough to print multiple messages without interruption.
   :feedback_d: Correct! This statement is false. It is not possible for the same message to be printed twice in a row. The Queue class is designed such that only one process can get from it at a time. Each get call removes a message from the queue, so that any subsequent get call will not get the same message again.

   (After watching the video.) Suppose you were to run the code a second time. Which of the following statements is FALSE? Consider both the process ordering (the ordering of 1's and 2's in the output) and the message ordering (the order in which the messages appear).

The Greatest Common Divisor (GCD)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recall that the GCD of two positive integers is the highest number that goes evenly into both numbers. For example, the GCD of 24 and 36 is 12, because 24/12 = 2 and 36/12 = 3, and there is no number larger than 12 that divides both numbers evenly. If you’re uncertain how to compute the GCD, one simple way for now is just to choose relatively small positive integers and see with a calculator if they divide both numbers.

A function that implements the GCD using Euclid's algorithm is shown below. In short, Euclid's algorithm is based on the observation that the GCD of two numbers does not change if the larger number is replaced by the difference of the two numbers. The modulo operation simply finds the difference between the larger and smaller numbers after a sequence of subtractions of the smaller number(i.e. division). **Make sure you understand this code before continuing on**. Pay close attention to Line 4: ``a, b = b%a, a``. This line simultaneously assigns ``a`` the value of ``b%a`` (i.e., the *remainder* when b is divided by a), and assigns ``b`` the old value of ``a``. 

.. activecode:: gcd_simple
   :language: python

   Run this code with different values of ``x`` and ``y`` to learn how this function works. What happens when you use numbers that are not divisible by each other? Use the "Show CodeLens" button to visualize the execution of the code in both instances. 
   ~~~~
   #gcd function
   def gcd(a, b):
       while a != 0:
           a, b = b%a, a
       return b

   #test code
   x = 24
   y = 36

   divisor = gcd(x,y)

   print("The GCD of {0} and {1} is {2}".format(x, y, divisor))


Computing the GCD with a Shared Queue
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Suppose the goal is to compute the GCD of *many* pairs of numbers. Using a shared queue allows many processes to participate in this task.


An Unplugged Activity 
""""""""""""""""""""""""""""
Let’s first practice computing the GCD with a shared queue through an unplugged activity. In this activity, a main process will generate numbers and then put them on a shared queue that workers can access for GCD calculations. To compare parallel and serial computation, the main process will also compute these GCDs itself.

This activity requires at least five people. For three of these five people:
    * One person will play the main process and will need 1 sheet of paper and one writing utensil.
    * One person will play the input queue and will need 1 writing utensil.
    * One person will play the output queue and will need 1 sheet of paper and one writing utensil.

At least two additional people are needed. Each will play a separate worker and need one sheet of paper, one writing utensil, and one calculator.

Each of the workers should sit as far apart as possible in the room. The main process and both queues should be in a central location in the room.

Main process procedure:
    1. Fill out one line at a time on a sheet of paper. Each line should contain two randomly chosen two-digit positive integers. Write 7 lines  of numbers in this manner.
    2. Give this sheet of paper to the input queue.
    3. Tell the workers to begin their procedures.
    4. Compute all GCDs yourself as well, reading one pair of numbers at a time from the input queue's paper. This serves as an example of serial calculation.

Worker procedure:
    1. Say "get" to the input queue and wait until there is a response from the input queue (ignore verbal responses to other workers)
    2. While the input queue has not said "done":
        a. Write down the pair of numbers received
        b. Compute the greatest common divisor (GCD) of the two numbers.
        c. Say "put" to the output queue and wait until the output queue acknowledges you.
        d. Tell the output queue the pair of numbers and their GCD.
        e. Say "get" to the input queue and wait until there is a response from the input queue (ignore verbal responses to other workers)
        f. Loop back up to step 2

Input queue procedure:
    1. Receive a sheet of paper from the main process, with pairs of numbers. Keep the paper in a location where the main process can see it too, since it will need to access the paper for the serial calculations.
    2. Wait for a "get" message from a worker.
        a. When received, give the worker a pair of non-crossed-out numbers, and cross out the numbers given.
        b. If multiple requests come in simultaneously, handle them one at a time, with distinct pairs of numbers for each request.
        c. If there are no more numbers when a worker requests some, say “done” to that worker.

Output queue procedure:
    1. Start with a blank sheet of paper.
    2. Wait for messages:
        a. "put" (from a worker): Receive the worker’s three numbers and write them on the highest blank line on the paper.
        b. "get" (from the main process): Tell the main process the three values on the highest non-crossed-out line of the blank paper, and then cross out that line.
            i. If a get message comes when no values are on the paper, tell the main process to do nothing until you respond later with three numbers.
        c. If multiple requests come in simultaneously, handle them one at a time.


In the unplugged activity above, very little synchronization between the workers is needed. Only one worker can access a queue at a time, but otherwise each worker is free to work as quickly or slowly as needed. If each task (computing the GCD) is enough work to justify potentially waiting briefly for queue access, the parallel approach will show speedup over the sequential approach. This will most likely be the case in this activity: the parallel workers will complete all GCD calculations before the main process is able to do the same.

.. note::
   The unplugged activity could be implemented directly in code. However, computing the GCD, even of very large numbers, is a fast operation. To see why this is a bit of a problem, imagine if the unplugged activity asked workers to add 1 to each of the provided numbers, instead of computing the GCD. The workers would be saying “get” and “put” much more frequently, and so the proportion of time spent waiting for queue access, instead of calculating, would grow. In other words, the overhead of process communication will outweigh any benefits of parallelism.

   A similar situation would occur if we were to program the unplugged activity as is. GCD is easy for a computer to compute quickly. To make the overhead of the shared queue worthwhile, then, we need to increase the amount of work required per task. We can easily accomplish this by having each worker request not just a single pair of numbers, but rather a *block* of many pairs of numbers. Only when the worker has handled the entire block will it put all results on the output queue and get another block from the input queue. This increases the amount of work that each process performs, reducing the number of times workers would be saying "get" and "put", thus also reducing communication overhead.

Translating it to code: Serial Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Let's now write a Shared Queue implementation of GCD. In the serial version, one process will "put" all the GCD pairs in the input queue, and then "get" a *block* of GCD pairs, find the GDC of each pair, and then place the result in the output queue.

Download the file `gcdWithBlanksSerial.py <https://github.com/csinparallel/intro-parallel-book/blob/master/_sources/commonAlgorithms/code/gcdWithBlanksSerial.py>`_. 

The code begins running in the ``main`` namespace at the bottom. 

.. literalinclude:: code/gcdWithBlanksSerial.py
   :language: python
   :lines: 65-66

   


The main process then runs the ``gcdSequential`` function:

.. literalinclude:: code/gcdWithBlanksSerial.py
   :language: python
   :lines: 48-59

Specifically, ``gcdSequential`` executes the following steps:

* The ``buildInputs`` function is called, which creates NUM_BLOCKS blocks of numbers, with PAIRS_PER_BLOCK pairs of numbers in each block. The numbers range from MIN_VALUE to MAX_VALUE.

* ``computeGCDs`` is then called, which gets one block at a time from inputQ, then one pair at a time from the current block. It computes the GCD by calling the provided gcd function (an implementation of Euclid’s algorithm), and appends the results to a blockOutput variable. When the block is fully processed, the results for the block are put on the output, and a new block is obtained.

* ``processOutputs`` is then called, which simply obtains one output at a time. If ``VERBOSE`` is set to ``True``, then all results will be printed. Otherwise, nothing is really done to "process" the outputs beyond simply obtaining them, but this function simulates what would be done as the next step in a larger application.

Try it out: the ``buildInputs`` function
"""""""""""""""""""""""""""""""""""""""""
A copy of the ``buildInputs`` function from ``gcdWithBlanksSerial.py`` is shown below:

.. code-block:: python

   def buildInputs(inputQ):
       for i in range(_______________):  #a
           block = []
       for i in range(_______________): #b
           block.append([random.randint(MIN_VALUE, MAX_VALUE), random.randint(MIN_VALUE, MAX_VALUE)])
           inputQ.put(block)

       # use sentinels to avoid possible race condition (multiple checks for not empty, then one gets, other hangs on get)
       for i in range(_______________): #c
           inputQ.put("DONE")

A single variable is needed for each of the ``range()`` functions in the above code snippets. Can you figure out what they are? Read the description of the ``buildInputs`` function above if you are having trouble.

.. dragndrop:: dnd-sq-ser-1
    :match_11: NUM_BLOCKS|||#a
    :match_12: PAIRS_PER_BLOCK|||#b
    :match_13: WORKERS|||#c

    Match the variable with its appropriate place in the code 


Try it out: the ``computeGCDs`` function
"""""""""""""""""""""""""""""""""""""""""

Now, let's look at of the ``computeGCDs`` function.

.. code-block:: python

   def computeGCDs(id, inputQ, outputQ):
       block = _______________ #d
       while(block != _______________): #e
           blockOutput = []
           for i in range(_______________): #f
               pair = block[i]
               blockOutput.append([id, pair[0], pair[1], gcd(pair[0], pair[1])])
               outputQ.put(blockOutput)
           block = _______________ #d

.. dragndrop:: dnd-sq-ser-2
    :match_11: inputQ.get()|||#d
    :match_12: PAIRS_PER_BLOCK|||#f
    :match_13: "DONE"|||#e

    Match the variable with its appropriate place in the code 

Try it out: timing the serial version
""""""""""""""""""""""""""""""""""""""""""""""
Fill in the blanks in your local copy of ``gcdWithBlanksSerial.py``. Once you are done, add a ``print()`` statement to the ``main()`` function to display the amount of time it takes to run the code:

.. code-block:: python

    def main():
        print("NUM_BLOCKS: {}\nPAIRS_PER_BLOCK: {}\nMIN_VALUE: {}\nMAX_VALUE: {}\nNUM_WORKERS: {}".format(NUM_BLOCKS, PAIRS_PER_BLOCK, MIN_VALUE, MAX_VALUE, NUM_WORKERS))
        seqTime = gcdSequential()
        print("Sequential Time is: {} seconds".format(seqTime)) #add this line

.. shortanswer:: short-sq-ser-1

   Run the code a few times. What kind of performance do you see?

Study the sequential code as best as you can before moving forward. 


Translating it to code: Parallel Version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To create a parallel version of this program, first copy your completed ``gcdWithBlanksSerial.py`` file to a new file called ``gcdWithBlanks.py``. Next, modify the main function so that a new function, ``gcdParallel()`` is called:


.. code-block:: python

    def main():
        print("NUM_BLOCKS: {}\nPAIRS_PER_BLOCK: {}\nMIN_VALUE: {}\nMAX_VALUE: {}\nNUM_WORKERS: {}".format(NUM_BLOCKS, PAIRS_PER_BLOCK, MIN_VALUE, MAX_VALUE, NUM_WORKERS))
        seqTime = gcdSequential()
        print("Sequential Time is: {} seconds".format(seqTime)) 
        parTime = gcdParallel() #add this line
        print("Parallel Time is: {} seconds".format(seqTime)) #add this line too

The great news is that the parallel version of this code uses exactly the same functions! The only difference is that the main process creates NUM_WORKERS child processes that will each do the work in parallel. Copy and paste the following fill-in-the-blank function to your ``gcdWithBlanks.py`` file:

.. code-block:: python

    def gcdParallel():
        print("----------\ngcdParallel")
        inputQ = _______________ #g
        outputQ = _______________ #g

        buildInputs(inputQ)

        startTime = timeit.default_timer()
        for i in range(1, NUM_WORKERS+1):
            #h: create and start a process here

        ________________________________ #i
        elapsedTime = timeit.default_timer() - startTime
        print("Elapsed time (s):", elapsedTime)
        return elapsedTime


The code contains many blanks. Let's fill in the blanks together to complete the implementation.

Initializing new queues
""""""""""""""""""""""""""

.. fillintheblank:: sq-fitb1

   Fill in the blanks to complete the statements commented with ``#g``. The goal here is to initialize ``inputQ`` and ``outputQ`` with *new queues*.

   inputQ = ``|blank|``
    
   outputQ = ``|blank|``

   -   :Queue\(\): Correct.
       :x: Incorrect. Take a look at the serial implementation. How are queues initialized?
   -   :Queue\(\): Correct.
       :x: Incorrect. Take a look at the serial implementation. How are queues initialized?

Completing the for loop:
""""""""""""""""""""""""""""""""
The for loop in ``gcdParallel()`` is where all the parallelization happens. Essentially, we want each worker to compute the gcd, using the created input and output queues. Let's build this code together:

    .. code-block:: python

       for i in range(1, NUM_WORKERS+1):
            #h: create a start a process here

.. mchoice:: sq-mc-1
   :answer_a: create_process()
   :answer_b: process()
   :answer_c: Process()
   :answer_d: make_process()
   :correct: c
   :feedback_a: Take a look at the shared queue parrot example. How are processes created?
   :feedback_b: Take a look at the shared queue parrot example. Is the function call lowercase?
   :feedback_c: Great work!
   :feedback_d: Take a look at the shared queue parrot example. How are processes created?

   What function allows for a worker to start a process?


.. mchoice:: sq-mc-2
   :answer_a: target
   :answer_b: format
   :answer_c: put
   :answer_d: args
   :answer_e: get
   :correct: a,d
   :feedback_a: Great job!
   :feedback_b: Take another look at process creation in the "hello world" example. What are its arguments?
   :feedback_c: Take another look at process creation in the "hello world" example. What are its arguments?
   :feedback_d: Nice work!
   :feedback_e: Take another look at process creation in the "hello world" example. What are its arguments?

   The function that creates a process has two formal parameters. What are they?


.. fillintheblank:: sq-fitb2

   Let's assign values to the two formal parameters:

   target = ``|blank|``, args = (``|blank|``)

   -   :computeGCDs: Correct! That is the correct target function!
       :x: Not quite. What is the name of the function we want each process to call? 
   -   :i\, inputQ\, outputQ: Correct! Those are the correct arguments that the target function needs!
       :x: Incorrect. Consider what the target function is, what arguments it usually takes, and what they should be in the context of the loop.

.. mchoice:: sq-mc-3
   :answer_a: process()
   :answer_b: begin()
   :answer_c: start()
   :answer_d: put()
   :answer_e: get()
   :correct: c
   :feedback_a: No, this is similar to the function that creates processes. We are looking for a method to start the process!
   :feedback_b: No. Take another look at the "hello world" program. How are processes started?
   :feedback_c: Great job!
   :feedback_d: Take another look at the "hello world" program. How are processes started?
   :feedback_e: Take another look at the "hello world" program. How are processes started?

   The process creation function invokes a method to start a process. What is that method called?

Finishing up the function
""""""""""""""""""""""""""""""""

.. fillintheblank:: sq-fitb3

   The last thing the parallel version does is manage all the data in the output queue. What function should be called at line ``#i``? Be sure to include any arguments.

   -   :processOutputs\(outputQueue\): That's correct! Wonderful job!
       :computeGCDs\(.*\): Nope. This was run inside the for loop!
       :processOutputs\(.*\): Close. What are the arguments?
       :buildInputs\(.*\): Not quite. This function was used to set up the queues for initial use. We want to conclude the function!  
       :x: Try again. Take a look at the serial version of this code. What happens after the gcd is computed?


Putting it all together
"""""""""""""""""""""""""""""""""

Using the solutions to the previous exercises, complete the ``gcdParallel()`` function.

.. reveal:: re-sq-final
    :showtitle: Show solution
    :hidetitle: Hide solution

    .. code-block:: python

        def gcdParallel():
            print("----------\ngcdParallel")
            inputQ = Queue()
            outputQ = Queue()

            buildInputs(inputQ)

            startTime = timeit.default_timer()
            for i in range(1, NUM_WORKERS+1):
                Process(target=computeGCDs, args=(i, inputQ, outputQ)).start()

            processOutputs(outputQ)
            elapsedTime = timeit.default_timer() - startTime
            print("Elapsed time (s):", elapsedTime)
            return elapsedTime


Timing the parallel version
""""""""""""""""""""""""""""""""""""""""""""""

.. shortanswer:: short-sq-par-1

   Run the code a few times, modifying the ``WORKERS`` variable. What kind of times do you see?


.. shortanswer:: short-sq-par-2

   Add code to the main function to compute the speedup of the parallel version over the serial version. Re-run your code, modifying the ``WORKERS`` variable each time. What kind of speedup do you see?


A fully working program can be downloaded `here <https://github.com/csinparallel/intro-parallel-book/blob/master/_sources/commonAlgorithms/code/gcd.py>`_.


