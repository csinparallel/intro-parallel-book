
1.1 First Steps - Programming Shared Memory
-------------------------------------------

In this book, we use the Open Multi-Processing (**OpenMP**) library to demonstrate how 
to program shared memory systems. While OpenMP is just one of many options for programming 
shared memory systems, we choose OpenMP due to its pervasiveness and relative ease of use. 
OpenMP employs a series of compiler directives to enable users to incrementally add 
parallelism to their programs and is natively supported by GCC. 

1.1.1 The Fork-Join Pattern
^^^^^^^^^^^^^^^^^^^^^^^^^^^

As a means of introducing OpenMP, we begin by introducing the **fork-join pattern** for parallel programming.

.. image:: images/ForkJoin.png

In fork-join, the main thread "forks" (or creates) a series of threads that each perform a separate task in parallel.
When each thread terminates, their executions "join" (or merge) together back into the main thread.

Consider the following serial program. What is its output?


.. _lst_sm_fork_join_serial:

.. activecode:: sm_fork_join
  :language: c
  :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
  :linkargs: ['-fopenmp']
  :caption: Serial Fork-Join

  #include <stdio.h>     // printf()
  #include <omp.h>       // OpenMP

  int main(int argc, char** argv) {

      printf("\nBefore...\n");

  //    #pragma omp parallel 
      printf("\nDuring...");

      printf("\n\nAfter...\n\n");

      return 0;
  }


The above code simply prints out the strings ``Before``, ``During`` and ``After`` in order. 

Now *uncomment* the ``omp parallel pragma`` on line 8 and re-run the program.

.. mchoice:: sm_mc_fork_1
    :correct: c
    :answer_a: Nothing happens. It's the same output.
    :answer_b: The three strings ``Before``, ``During`` and ``After`` are printed multiple times.
    :answer_c: The string ``During`` is printed multiple times.
    :answer_d: The strings ``During`` and ``After`` are each printed multiple times.
    :feedback_a: Did you remember to uncomment the pragma on line 8? Try again.
    :feedback_b: This is not correct. Try uncommenting the pragma and re-running the code!
    :feedback_c: Correct! The string ``During`` is printed 4 times (do you know why?).
    :feedback_d: Close, but not quite. Try uncommenting the pragma and re-running the code!

    What happens when you re-run the example?

The ``omp parallel pragma`` on line 8, when uncommented, tells the compiler to fork a set of threads to execute the next *line* of code
(later you will see how this is done for a block of code). Next, the ``omp parallel pragma`` creates a team of threads and directs each 
thread to run the line ``printf(\nDuring...)`` in parallel. 

Thus, the string ``During`` is printed out a number of times that correspond to the number cores on the system (in this case, 4). Note that in OpenMP the 
join is implicit and does not require a pragma directive. 

1.1.2 The SPMD Pattern
^^^^^^^^^^^^^^^^^^^^^^

A common use of the fork-join pattern is to have each thread run the same block of code on different components of data. This pattern is known as 
**single program multiple data** or the **SPMD** pattern. Let's try running a new code snippet:

.. _lst_sm_spmd_serial:

.. activecode:: sm_spmd_serial
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-fopenmp']
   :caption: SPMD (serial)

   #include <stdio.h>
   #include <omp.h>

   int main(int argc, char** argv) {
      printf("\n");

      //    #pragma omp parallel 
      {
          int id = omp_get_thread_num();
          int numThreads = omp_get_num_threads();
          printf("Hello from thread %d of %d\n", id, numThreads);
      }

      printf("\n");
      return 0;
   }

When the ``omp parallel`` pragma executes, it assigns each thread a unique id (from ``0`` to ``n-1`` for *n* threads). 
A programmer can access this unique id by calling the ``omp_get_thread_num()`` function. Likewise, OpenMP provides the 
``omp_get_num_threads()`` function to provide the programmer the ability to see the total number of threads.
On a single threaded program (like the one shown above), there is 1 total thread, with a thread id of ``0``.

Consider what will happen when the pragma above is uncommented (recall that there are ``4`` total cores on the system).
What do you think the output would be?


.. mchoice:: sm_mc_spmd_1
    :correct: c
    :answer_a: There will be 4 hello messages, each having the thread id 0
    :answer_b: There will be 4 hello messages, each having different thread ids, printed in order
    :answer_c: There will be 4 hello messages, each having different thread ids, printed in random order
    :answer_d: Something else
    :feedback_a: Recall that each thread is assigned a unique id.
    :feedback_b: This seems like the correct answer, but it is not (see below).
    :feedback_c: This is in fact the correct answer (do you know why?).
    :feedback_d: Actually, the correct answer is one of the listed options!

    What will be the output when the pragma is uncommented in the spmd_serial program?

Let's now run a version of the program with the ``omp parallel`` pragma uncommented:

.. _lst_sm_spmd_parallel:

.. activecode:: sm_spmd_parallel
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-fopenmp']
   :caption: SPMD (parallel)

   #include <stdio.h>
   #include <omp.h>

   int main(int argc, char** argv) {
      printf("\n");

      #pragma omp parallel //this line is now uncommented!
      {
          int id = omp_get_thread_num();
          int numThreads = omp_get_num_threads();
          printf("Hello from thread %d of %d\n", id, numThreads);
      }

      printf("\n");
      return 0;
   }

Running this program reveals two things. First, since there are 4 total cores on the system, the ``omp parallel``
pragma generates a team of 4 threads, assigning each a unique id from 0 to 3. Each thread then runs the code 
in the scope of the pragma (denoted by curly braces). The process can be visualized as follows:

.. image:: images/ForkJoin_SPMD.png

The code in main up until line 6 is run in one thread on one core; the forking of separate threads to run the code
between lines 7 and 12 is shown in the middle of the diagram. The final last couple of lines of code are run back in
the single thread 0 after all the threads have completed and join back to the main thread.

.. mchoice:: sm_mc_spmd_2
    :correct: b
    :answer_a: The hello messages always print in order (0 .. 3)
    :answer_b: The ordering of the hello messages is random and cannot be predicted.
    :answer_c: The hello messages always prints in a random order, but is consistent over multiple runs
    :feedback_a: Try running the program a few more times.
    :feedback_b: Correct!
    :feedback_c: Try running the program a few more times. Is the order always the same?

    Try re-running the sm_spmd_parallel example a few times. What do you observe about the order of the printed lines?


Re-running the program multiple times illustrates an important point about threaded programs: 
the ordering of execution of statements between threads is *not* guaranteed. In fact, the order in which any set of 
threads execute is not guaranteed, and is determined by the operating system. This situation illustrates the concept 
of **non-determinism**, where an algorithm or program can have different outputs over multiple runs. While all 
parallel algorithms have inherent non-deterministic properties, experienced programmers can *leverage* the non-deterministic
execution to their advantage (e.g. run the code on multiple cores) and still get correct output. We will study several such 
examples in the coming sections.  

1.1.3 A Larger Example - Filling an Array
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The fork-join and SPMD patterns are some of the most widely used for programming shared memory systems.
In general, the fork-join pattern is used for **task parallelism**, or when a team of threads receive a 
component of a larger problem and work together to come up with a solution. The SPMD pattern is commonly 
used for **data parallelism** where a team of threads run the same program on different components of 
*data* or *memory*. In this scenario, each thread does the exact same task -- the only difference is that 
each thread is operating on a different unit of data or memory.

As an example, consider the process of filling an array of size *n* with elements from 1 .. *n* -1:

.. video:: video-fill-array
   :controls:
   :thumb: images/array-fill-par_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/filling_array.mov

The following snippet of C code is a serial implementation that populates an array with 20 million elements:

.. activecode:: sm_arrayfill_serial
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-fopenmp']
   :caption: Array Fill (serial)

   #include <stdio.h>
   #include <stdlib.h>

   #define N 20000000 //size of the array

   int main(void){

        int * array = malloc(N*sizeof(int)); //declare array of size N
        int i;

        //populate array
        for (i = 0; i < N; i++) {
            array[i] = i+1;
        }

        printf("Done populating %d elements!", N);
        return 0;
   }

Let's consider how we would parallelize a program like this. One way is to assign each thread a different 
segment of the array, and have each thread populate its own component of the array. The following 
video illustrates how 4 threads would populate an array (each thread is assigned a different color):

.. video:: video-fill-part
   :controls:
   :thumb: images/array-fill-par_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/filling_array_parallel.mov


.. mchoice:: sm_mc_tpdp_1
    :correct: b
    :answer_a: Task parallelism
    :answer_b: Data parallelism
    :answer_c: Neither
    :feedback_a: Incorrect. Remember that in task parallelism, each thread is performing something different. 
    :feedback_b: Correct! In this example, each thread is performing the same task on a different unit of memory.
    :feedback_c: Actually, it is one of the options listed!

    Is populating an array in parallel an example of data parallelism or task parallelism? 


The notions of "task parallelism" and "data parallelism" are two extremes on a spectrum. Most parallel programs
fall somewhere along the spectrum. For now, it is sufficient to recognize that both fork-join and SPMD are valid 
ways to assign work to threads.


1.1.3 For-Loop Pragmas
^^^^^^^^^^^^^^^^^^^^^^

Before we parallelize the populate array program, we need to introduce two new pragmas. The first is the 
``omp for`` pragma. This pragma parallelizes the iterations of a for loop by assigning each thread a chunk of 
iterations of the loop. The following code snippet illustrates how to use the ``omp for`` pragma to parallelize 
the populate array program:

.. activecode:: sm_arrayfill_parallel1
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-fopenmp']
   :caption: Array Fill (serial)

   #include <stdio.h>
   #include <stdlib.h>

   #define N 20000000 //size of the array

   int main(void){

        int * array = malloc(N*sizeof(int)); //declare array of size N

        #pragma omp parallel //<-- entered omp parallel pragma here
        {
            //populate array

            #pragma omp for //<-- entered omp for pragma here
            for (int i = 0; i < N; i++) {
                array[i] = i+1;
            }

        }
        printf("Done populating %d elements!", N);
        return 0;
   }


Notice that in the body of the above program that there is nothing between the ``omp parallel`` and the ``omp for`` pragmas. This is fairly common, as sometimes the key piece of code to be parallelized is just a for loop. To simplify the process for programmers, OpenMP provides the ``omp parallel for`` pragma, which literally combines the functionality of the ``omp parallel`` and the ``omp for`` pragmas into one line of code. 

The following program illustrates this new pragma in action:

.. activecode:: sm_arrayfill_parallel_for
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-fopenmp']
   :caption: Array Fill (serial)

   #include <stdio.h>
   #include <stdlib.h>

   #define N 20000000 //size of the array

   int main(void){

        int * array = malloc(N*sizeof(int)); //declare array of size N
        int i;

        //populate array
        #pragma omp parallel for //<-- inserted omp parallel for pragma
        for (i = 0; i < N; i++) {
            array[i] = i+1;
        }

        printf("Done populating %d elements!", N);
        return 0;
   }

Notice how much shorter and simpler this code is. However, the ``omp parallel for`` isn't always appropriate for all cases, as we will see in 
the next section.
