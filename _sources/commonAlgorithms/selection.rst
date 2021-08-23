3.2 Selection
-------------

Author: Dorian Arnold, Emory University

..
  E-mail: dorian.arnold@emory.edu

3.2.1 The Selection Task
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
  Crawling: Concept Overview and Description

  #. Define selection problems:
     * Generalized problem definition: Finding kth element in a collection
     * Specialized version: Finding the global min (1st) or max (last) element in a collection
     * In this module, we use the specialized version for simplicity
  #. Unplugged activity video: Finding oldest coin!
  #. Conclude with a summarizing outline of the basic algorithmic steps

Have you ever had a set of items and needed to *select* a particular one based on its size or value compared to the others, for example, the tenth largest city in the world or the third richest person in a country?
Even more straightforward are versions of this problem where you are selecting an extreme value, for example,
the ripest watermelon in the patch, the carton of milk with the latest expiration date, or the oldest penny in a jar. In computing, we call this *The Selection Problem* the topic of this chapter. In particular, we focus on one specialized case of Selection, particularly *finding the smallest element*. (Hopefully, the extrapolation from smallest element to smallest or largest kth element is readily imaginable.) After a general introduction, we formalize the problem and its serial (or sequential) solution. Then we identify opportunities to parallelize the serial solution and describe parallel solutions using two different multi-tasking approaches, namely multi-threading using OpenMP and multi-processing using MPI. We conclude the chapter with a discussion of things to consider when parallelizing an algorithm, including performance considerations.

Selection is a relevant task used for more complex nearness or proximity search tasks, like finding the shortest path between two nodes in a graph or finding the nearest neighbor of a node in a graph. Many important tasks that we perform all the time are based on proximity searches. For example, web search relies upon proximity search to identify documents that are closely related to given search terms. Proximity search is also fundamental to other applications like data compression, data mining, pattern recognition and even non-computer applications like delivery route scheduling and DNA analysis.


Serial Selection Unplugged
,,,,,,,,,,,,,,,,,,,,,,,,,,,,

The following video elucidates the Selection problem walking through the example of finding the smallest marble from a jar (of unsorted marbles). We discuss the specific necessary steps as well as the problem's time performance complexity, that is the general concept of how long the problem takes as a function of the total number of elements, marbles in this case.

**TODO: Create Serial Selection Unplugged video, upload to CSinParallel server, link here**

.. video:: serial_selection_unplugged
   :controls:
   :thumb: selection/selection-serial-tn.jpg


Formal Definition
,,,,,,,,,,,,,,,,,,,

Formally in computing, the general selection task or problem is defined as follows: given a collection of elements, find the :math:`k^{th}` smallest (or largest) element. Selection assumes that the unique elements of the input collection form a totally ordered set. That is, for the unique elements of the input collection, there is some binary comparator, :math:`\leq`, such that for every :math:`a, b, c`:

:math:`a \leq a`

:math:`a \leq b` or :math:`b \leq a`

If :math:`a \leq b` and :math:`b \leq c`, then :math:`a \leq c`

If :math:`a \leq b` and :math:`b \leq a`, then :math:`a = b`

To find the :math:`k^{th}` element, the general selection algorithm requires that the input collection be sorted. Specialized cases of selection where :math:`k` is the smallest (or largest) element of the the collection can be solved simply by scanning the entire collection, tracking the minimum (or maximum) value observed. As already stated, in this module, we focus on one of the specialized *smallest element* cases. This will simplify or exposition of the concept of partitioning an algorithm into parallel tasks and give you hands-on experience with using task-based decomposition to parallelize a sequential program.

The formal algorithm for "simple" serial selection is:

   Input: Collection of integers

   Output: Minimum value in collection
   
   1. Set min to first element of collection
   2. Compare minimum to every other element in collection.

      2a. If element is less than minimum, set minimum to element

   3. Print/return minimum value

.. mchoice:: selection_steps_sequential
   :correct: d
   :answer_a: 4
   :answer_b: 8
   :answer_c: 12
   :answer_d: 32
   :feedback_d: Correct! Though we can do slightly better by skipping the first element.

   For a collection of 32 elements, how many steps (iterations) does the sequential selection algorithm need?


3.2.2 A Basic (Sequential) Solution
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
   Walking: Building toward a full sequential code implementation
   #. Recall basic selection algorithm from 3.2.1
   #. Build complete basic implementation from algorithm


In the code below, we have defined an integer array, Collection, with 32 random integers. In the designated space, implement the serial selection algorithm to complete the code below, such that it properly prints the smallest value in Collection. Remember, you need to initialize min to the first element, then compare min to every subsequent element of the array.

.. activecode:: sequential_selection_blank
   :language: c
   :caption: Serial Selection
   :nocodelens:

   #include <stdio.h>
   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main( ) {
       int i, min;

       /* Place your solution code here */
    
       printf("The minimum value in the collection is: %d\n", min);
   }

Click "show" below to reveal the solution for the previous exercise:

.. reveal:: seq_sel

  .. activecode:: sequential_selection
     :language: c
     :caption: Serial Selection
     :nocodelens:

     #include <stdio.h>

     #define COLLECTION_SIZE 32

     int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

     int main( ) {
       int i, min;

         /* 1. Initialize min to first element of collection */
         min=Collection[0];

         /* 2. Compare minimum to each element in collection. */
         for( i = 0; i < COLLECTION_SIZE; i++){

             /* 2.a If element is less than minimum, set minimum to element */
             if( Collection[i] < min ){
                 min = Collection[i];
             }
         }
 
         /* 3. Print minimum value */
         printf("The minimum value in the collection is: %d\n", min);
     }

**TODO: Consider encoding time steps (e.g. a counter) into the Serial Solution to show how many "time steps" the solution requires?**


3.2.3: A Parallel Selection Algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
   Jogging :-)

Parallel Selection Unplugged
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

The serial algorithm presents a straightforward opportunity for parallelization: we can distribute the elements to be scanned or searched amongst multiple tasks that can search their respective elements at the same time, thereby reducing the overall physical time needed to execute the task. We outline this approach in the following video and then present the parallelization strategy step-by-step.

**TODO: Create Serial Selection Unplugged video, upload to CSinParallel server, link here**

.. video:: parallel_selection_unplugged
   :controls:
   :thumb: selection/selection-parallel-tn.jpg

Our parallelization strategy follows a standard approach called divide and conquer: the serial algorithm is one large loop to select the minimum, but the collection can be subdivided or partitioned and parallel (or concurrent) loops can be executed to find the minima of each sub-partition. This is called the *parallel loop pattern*. Then a final loop can be executed to find the overall minimum from the set of sub-partition minima. This step may be referred to as a *reduction*.

Here is a formal algorithm for parallel selection:

   Input: Collection of integers

   Output: Minimum value in collection

   1. Divide the collection amongst multiple tasks
   2. Each task sets its local minimum to the first element in its sub-collection
   3. Each task compares its local minimum to each subsequent element in its sub-collection

      3a. If element is less than local minimum, update local minimum to element

   4. After all tasks complete, collect full set of local minima
   5. Find the global minimum from the set of local minima
   6. Print/return global minimum value

Parallel algorithms are most often more complicated than their sequential counterparts. So why do we use them. The answer is short and sweet: to save time! Generally, the total or aggregate number of operations (steps or iterations) distributed across the parallel loops are the same or sometimes even greater than the total number of sequential operations. However, executing the parallel loops concurrently can reduce the total real execution time dramatically.

.. mchoice:: selection_steps_parallel
   :answer_a: 4
   :answer_b: 8
   :answer_c: 12
   :answer_d: 32
   :correct: d
   :feedback_d: Correct! The parallel version of the algorithm must execute the same number of steps, however the steps are distributed amongst multiple tasks.

   For a collection of 32 elements evenly distributed amongst 4 tasks, how many steps (iterations) does the parallel selection algorithm execute?

.. mchoice:: selection_time_parallel
   :answer_a: 4
   :answer_b: 8
   :answer_c: 12
   :answer_d: 32
   :correct: c
   :feedback_c: Correct! The four parallel tasks execute 8 steps to find their local minima. However, these steps execute concurrently so the total number of time steps elapsed is also 8. After the four parallel tasks complete, we need four additional steps to find the global maximum. The grand total is 12 time steps. (Contrast this with the 32 time steps the sequential version.)

   For a collection of 32 elements evenly distributed amongst 4 tasks and assuming an iteration takes one (1) unit of time to execute, how many time units does it take to execute the parallel selection algorithm? (Be sure to consider that each of the four tasks simultaneously can execute an iteration every time unit.)

**TODO: Add diagram, e.g. a work/span graph, to illustrate the number of steps vs time steps. Possibly via a reveal section.**


3.2.3 A Parallel Solution using OpenMP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Running!

As described in ..., we can parallelize a task using the fork-join pattern, in which sequential code (running in a single task or thread) forks into multiple parallel codes (running in multiple tasks or threads) and the multiple parallel codes later join or merge back into the single sequential code. Also, as described in that module, OpenMP is a popular and convenient framework for fork-join task parallelization. In this section, we describe various approaches for implementing Parallel Selection using OpenMP.


OpenMP Parallel Loops (with Critical Regions)
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

At the beginning of an OpenMP program, the OpenMP framework is either implicitly or explicitly instructed to execute parallel sections with a certain number of tasks called threads. Multiple threads within the same program instance share the same memory and, therefore, are able to access common data structures. As we will see below, this requires some special consideration to avoid conflict issues that can arise as a result of data sharing.

Using the OpenMP "parallel" pragma, a user can specify that a loop be executed in parallel amongst the program's threads. In response, OpenMP will automatically divide and distribute the iterations of the loop among the parallel threads, that is, each thread will execute a different set of the loop's iterations, and together all threads will execute all of the loop's iterations.

Naively, this might appear to work for our Parallel Selection problem: each thread scans its part of the Collection updating the minimum value with new minima as they are encountered. However, when multiple threads can update the same data simultaneously, we encounter a subtle but important data sharing problem called "race conditions". Briefly, as different threads race to update the same data, the order in which they execute can cause a slower thread to overwrite an updated data item with older data, leading to incorrect results. In our case imagine, one thread updating the minimum value and another thread erroneously overwriting that value with a minimum value that is actually larger than the one already stored. For more information on race conditions, visit this section: https://pdcbook.calvin.edu/pdcbook/PDCBeginners/sharedMemory/racecond.html.

To avoid race conditions in OpenMP parallel loops, we must use the OpenMP "critical" pragma to specify data sharing regions that could render race conditions. OpenMP resolves these potential race conditions by executing critical regions sequentially. In other words, for critical regions within a parallel loop, we no longer get the benefit of multiple tasks or threads executing simultaneously.

.. activecode:: selection_omp_critical
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP
   :nocodelens:


   #include <stdio.h>
   #include <omp.h>

   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main( ) {
       int i, min;

       omp_set_num_threads(4);

       /* 1. Initialize min to first element of collection */
       min=Collection[0];

       /* 2. Compare minimum to each element in collection. */
       #pragma omp parallel for
       for( i = 0; i < COLLECTION_SIZE; i++){

           /* 2.a If element is less than minimum, set minimum to element */
           #pragma omp critical
           if( Collection[i] < min ){
               min = Collection[i];
           }

       }
 
       /* 3. Print minimum value */
       printf("The minimum value in the collection is: %d\n", min);
   }

.. shortanswer:: q1

   Can you think of any negative performance impact caused by the use of our critical section synchronization?


Potentially, if we are not careful, this can eliminate all the potential time savings we sought with the parallel solution in the first place! Indeed, our OpenMP Parallel Loop solution suffers this consequence. In fact, if you were to time its execution, you would observe that it runs even slower than the sequential code: it suffers all the overhead in setting up and executing parallel threads but gains none of the advantages of doing so.

Nonetheless, it is a simple, straightforward, naive solution that demonstrates how one might go about parallelizing the selection algorithm. The approach is reasonable, but the solution suffers due to practical shared data problems.

.. shortanswer:: q11

   As an additional exercise, how can you extend our OpenMP Parallel Loop approach to eliminate the race condition caused by simultaneous updates to the single, global "min" parameter?



OpenMP Parallel Loops (with Locks)
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,


With shared memory programming and OpenMP, you likely will encounter a concept called "locking". Briefly, locking is used to solve the same data sharing and race condition issues just described. A thread that attempts to "set" a lock can only do so if the lock is free: if the lock is free, that thread is said to have acquired the lock. When a lock is set or "held" by one thread, another thread trying to acquire the lock will be blocked until the lock becomes available for that thread. In fact, "locks" are most often the lower-level primitive OpenMP uses to implement a critical region. Below we show another implementation of Parallel Loops this setting and unsetting an OpenMP lock instead of using the critical region pragma. In principle, both codes take the same approach and suffer the same problem of serializing the execution of all the parallel threads.


.. activecode:: selection_omp_lock
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP
   :nocodelens:

   #include <stdio.h>
   #include <omp.h>

   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main( ) {
       int i, min;

       omp_set_num_threads(4);
       omp_lock_t lck;
       omp_init_lock(&lck);

       /* 1. Initialize min to first element of collection */
       min=Collection[0];

       /* 2. Compare minimum to each element in collection. */
       #pragma omp parallel for
       for( i = 0; i < COLLECTION_SIZE; i++){

           /* 2.a If element is less than minimum, set minimum to element */
           omp_set_lock(&lck);
           if( Collection[i] < min ){
               min = Collection[i];
           }
           omp_unset_lock(&lck);


       }
 
       /* 3. Print minimum value */
       printf("The minimum value in the collection is: %d\n", min);
   }

Functionally, both the solution using the OpenMP critical pragma and the section using OpenMP locks work. But the synchronization at the critical section serializes our program by enforcing that the code within the locks is executed serially. In other words, only one thread at a time can check and execute its potential update to min.


OpenMP Parallel Loops (with Reduction)
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

As already described, when tasks are forced to execute serially, we compromise the performance performance benefit of concurrent task execution. In this instance, we can avoid the performance penalty of critical region or lock-based synchronization by using OpenMP's reduction construct. OpenMP reduction creates an independent, local copy of the reduction variable for each thread thereby eliminating sharing of the reduction variable during the threads' execution. At the end of the threads' executions, the local copies are combined into a single value based on the specified reduction operation. This approach is shown in the code below.


Below we have a new version of shared memory selection using OpenMP's reduction construct:

.. activecode:: selection_omp_reduction
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP
   :nocodelens:

   #include <stdio.h>
   #include <omp.h>

   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main( ) {
       int i, min;

       omp_set_num_threads(4);

       /* 1. Initialize min to first element of collection */
       min=Collection[0];

       /* 2. Compare minimum to each element in collection. */
       #pragma omp parallel for reduction(min:min)
       for( i = 0; i < COLLECTION_SIZE; i++){

           /* 2.a If element is less than minimum, set minimum to element */
           if( Collection[i] < min ){
               min = Collection[i];
           }

       }
 
       /* 3. Print minimum value */
       printf("The minimum value in the collection is: %d\n", min);
   }

**TODO: For all OMP coding examples, explain specifically, line by line, not just abstractly and generally.**

3.2.4 A Parallel Solution using Message Passing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Running!

**TODO: Describe a general MPI strategy: distribute data, parallel loops, collect local minima, find global minimum ...**

.. activecode:: selection_mpi
   :language: c
   :caption: Selection using MPI
   :nocodelens:

   #include <stdio.h>
   #include <mpi.h>
   #include <stdlib.h>

   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main(int argc, char **argv)
   {
       int i;
       int lsize;
       char min;
       int world_rank, world_size;

       /* PREPARATIONS */
       MPI_Init(NULL, NULL);
       MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
       MPI_Comm_size(MPI_COMM_WORLD, &world_size);
    
       /* 1. Divide Collection amongst tasks */
       /* Compute size of local collections */
       lsize = COLLECTION_SIZE / world_size;

       // For each process, create a buffer for local collection
       int *lcollection = (int *)malloc( sizeof(int) * lsize );
    
       // Scatter collection from root process to all others
       MPI_Scatter(Collection, lsize, MPI_INT, lcollection, lsize, MPI_INT, 0, MPI_COMM_WORLD);

       // 2. Initialize each task's local minimum
       min=lcollection[0];

       // 3. Each task compares its local minimum to each element in its local collection.
       for( i = 0; i < lsize; i++){
           // 3.a If element is less than minimum, set minimum to element
           if( lcollection[i] < min ){
               min = lcollection[i];
           }
       }
    
       // 4. Collect all local minima
       char *lmins = (char *)malloc(sizeof(char) * world_size);
       MPI_Allgather(&lmins, 1, MPI_LONG, lcollection, 1, MPI_LONG, MPI_COMM_WORLD);
                                                                                                                                       
       // 5. Find the global minimum from the local minima
       min=lmins[0];
       for( i = 0; i < world_size; i++){
           if( lmins[i] < min ){
               min = lmins[i];
           }
       }

       // 6. Print global minimum value */
       printf("The minimum value in the collection is: %d\n", min);

       // Clean up
       free(lcollection);
       free(lmins);
       MPI_Barrier(MPI_COMM_WORLD);
       MPI_Finalize();

       return 0;
   }


**TODO: Breadkdown MPI coding example, line by line, not just abstractly and generally.**

**TODO: Tie MPI solution to the previous discussion on critical sections vs reduction.**

**TODO: Consider discussing MPI_Reduce as well? (If so, reference back to general reduction discussion.)**


3.2.5 Comparing Performance of the Various Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Sprinting!?

**TODO: Add performance section with data/graphs**

.. not a very deep dive. Goal to expose the reader to how these basic concepts can evolve into deeper, interesting and sophisticated challenges.

#. Plots of number of steps for sequential and parallel solutions vs. collection size
#. Plots of time performance for sequential and parallel solutions vs. collection size
#. Exercise: will parallel solution always outperform sequential solution?
#. Things to consider

   #. Opportunity/Costs: When does parallelization begin to pay off?
   #. Diminishing Returns: When does parallelization stop paying off?
   #. Load Imbalance: What if concurrent work is not evenly distributed?
   #. Ways to further increase parallelism, e.g. deeper divide/conquer hierarchies

3.2.6 Summary
^^^^^^^^^^^^^^^

**TODO: Add Chapter Summary**
