
CHAPTER 1: Shared Memory
:::::::::::::::::::::::::

`Recall <https://www.learnpdc.org/PDCBeginners/introduction/1.hardware.html>`_that a **shared-memory multiprocessor** is a type of computer where its compute units (or **cores**) all share the same main memory. In 
`Section 0.5 <https://www.learnpdc.org/PDCBeginners/introduction/5.platforms.html>`_ we discussed how most computers today are shared-memory multiprocessors thanks to multicore CPUs. Virtually all modern Desktop and laptop computers, and even small single board computers such as the Raspberry Pi, contain multicore CPUs. 

Processes and Threads
^^^^^^^^^^^^^^^^^^^^^^^^
Before we can discuss what a thread is, we must first discuss what a **process** is. A process can be thought of as an abstraction of a running program. When you type a command into the command line and press ``Enter``, the Bash shell launches a process associated with that program executable. Each process contains 
a copy of the code and data of the program executable, and its own allocation of the stack and heap. 

A **thread** is a light-weight process. While each thread gets its own stack allocation, it *shares* the heap, code and data of the parent process. As a result, all the threads in a multi-threaded process can access a *common pool of memory*. This is why multithreading is commonly referred to as **shared memory programming**. A single-threaded process is also referred to as a **serial** process or program.

A multicore CPU allows multiple processes to execute simultaneously, or in **parallel**. While the terms *concurrency* and *parallel* are related, it is useful to think of *concurrency* as a software/OS-level concept, while *parallel* as a hardware/execution concept. A multi-threaded program, while capable of parallel execution, runs concurrently on a system with only a single CPU core.

.. mchoice:: mc_mc_1
    :correct: a
    :answer_a: It stays more or less the same. 
    :answer_b: Approximately 50 seconds. 
    :answer_c: Aproximately 25 seconds.
    :feedback_a: Correct! While a multicore CPU increases the number of opportunities that a process can execute, the process will take 100 seconds to execute!
    :feedback_b: Not quite. Remember, the process is serial!
    :feedback_c: No. Remember, we are talking about a serial process!

    Suppose a serial process takes 100 seconds to execute on one core. How long will it take to execute it on a multi-core system with 4 cores? 



Thread Execution
^^^^^^^^^^^^^^^^^^^

The primary goal of creating multithreaded programs is to decrease the speed of a program's execution. In a program that is perfectly parallelizable (that is, all components are paralleizable), it is usually possible to distribute the work associated with a program equally among all the threads. For a program :math:`p` 
whose work is equally distributed among :math:`t` threads, it will take roughly :math:`p/t` time, if executed on :math:`t` cores.

.. mchoice:: mc_mc_2
    :correct: c
    :answer_a: It stays more or less the same. 
    :answer_b: Approximately 50 seconds. 
    :answer_c: Aproximately 25 seconds.
    :feedback_a: Nope. Remember, we are now dealing with a multi-threaded process. Furthermore, it is perfectly parallelized (i.e its work is split evenly between all threads).
    :feedback_b: Not quite. Check your math.
    :feedback_c: Correct!

    Suppose a multi-threaded process that is perfectly parallelized takes 100 seconds to execute on one core. How long will it take to execute 4 threads on a multi-core system with 4 cores? 


.. mchoice:: mc_mc_3
    :correct: b
    :answer_a: It stays more or less the same. 
    :answer_b: Approximately 50 seconds. 
    :answer_c: Aproximately 25 seconds.
    :feedback_a: Nope. Remember, we are now dealing with a multi-threaded process. Furthermore, it is perfectly parallelized (i.e its work is split evenly between all threads).
    :feedback_b: Correct! Even though there are 4 threads, if there are only 2 available cores, two of the threads will need to essentially run sequentially.
    :feedback_c: Not quite. In this case, there are only two available cores. How does this impact run-time?

    Suppose a multi-threaded process that is perfectly parallelized takes 100 seconds to execute on one core. How long will it take to execute 4 threads on a multi-core system with 2 cores? 

Introducing OpenMP
^^^^^^^^^^^^^^^^^^^^^^^^

Programmers can utilize several languages and libraries to program shared-memory multiprocessors. In this chapter, we will discuss **OpenMP** (or 
**Open** **M**uliti-**P**rocessing), a standard API for multithreading that has existed for over 25 years. A key advantage of OpenMP over other API and libraries is its use of **pragmas**, or compiler directives that indicate where in a program parallelism should occur. The actual task of 
creating and destroying teams of threads is done automatically and silently by the compiler, abstracting a way a lot of details that made writing 
multithreaded applications particularly difficult. In addition, OpenMP makes it possible for programmers to *incrementally* add parallelism to their programs. 



Re-define terms such as core, process thread.

Use analogy or unplugged activity to remind users how shared memory computations work (e.g. Jigsaw Analogy)

.. toctree::
    :maxdepth: 2

    firststeps.rst
    racecond.rst
    reduction.rst
    performance.rst
    drugdesign.rst