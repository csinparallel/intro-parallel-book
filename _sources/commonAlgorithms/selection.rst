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
the ripest watermelon in the patch, the carton of milk with the latest expiration date, or the oldest penny in a jar. In computing, we call this *The Selection Problem* the topic of this chapter. After a general introduction in the following video, we formalize the problem and its serial (or sequential) solution. Then we identify opportunities to parallelize the serial solution and describe parallel solutions using two different multi-tasking approaches, namely OpenMP and MPI. We conclude the chapter with a discussion of things to consider when parallelizing an algorithm.

Selection is a relevant task used for more complex nearness or proximity search tasks, like finding the shortest path between two nodes in a graph or finding the nearest neighbor of a node in a graph. Many important tasks that we perform all the time are based on proximity searches. For example, web search relies upon proximity search to identify documents that are closely related to given search terms. Proximity search is also fundamental to other applications like data compression, data mining, pattern recognition and even non-computer applications like delivery route scheduling and DNA analysis. 

**TODO: Serial Selection Unplugged:**

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

To find the :math:`k^{th}` element, the general selection algorithm requires that the input collection be sorted. Specialized cases of selection where :math:`k` is the smallest (or largest) element of the the collection can be solved simply by scanning the entire collection, tracking the minimum (or maximum) value observed. In this module, we study one of the specialized case, particularly *finding the smallest element* to expose you to the concept of partitioning an algorithm into parallel tasks and give you hands-on experience with using task-based decomposition to parallelize a sequential program.

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

(Don't scroll too far before completing this exercise: there's a solution below.)

.. activecode:: sequential_selection_blank
   :language: c
   :caption: Serial Selection

   #include <stdio.h>
   #define COLLECTION_SIZE 32

   int Collection[COLLECTION_SIZE]={18, 83, 80, 12, 86, 66, 68, 41, 91, 84, 57, 93, 67, 6, 50, 75, 58, 85, 45, 96, 72, 33, 77, 48, 73, 10, 99, 29, 19, 65, 26, 25};

   int main( ) {
       int i, min;

       /* Place your solution code here */
    
       printf("The minimum value in the collection is: %d\n", min);
   }

And here's a solution for the previous exercise:
 
.. activecode:: sequential_selection
   :language: c
   :caption: Serial Selection

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

3.2.3: A Parallel Selection Algorithm
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

..
   Jogging :-)

The serial algorithm presents a straightforward opportunity for parallelization. We outline this approach in the following video and then present the parallelization strategy step-by-step.

**TODO: Parallel Selection Unplugged:**

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

   For a collection of 32 elements evenly distributed amongst 4 tasks, how many TIME steps does the parallel selection algorithm execute?

3.2.3 A Parallel Solution using OpenMP
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Running!

TODO: Describe a general, naive openmp strategy: parallel loops (no reduction) ...

.. activecode:: selection_omp_critical
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP

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

TODO: Explain "parallel" and "critical" pragmas, including a high-level description of race conditions.

TODO: describe the use of locks to do the same thing as critical ...

.. activecode:: selection_omp_lock
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP

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

.. shortanswer:: q1

   Can you think of any negative performance impact caused by the use of our critical section synchronization?

When tasks are forced to execute serially, we compromise the performance performance benefit of concurrent task execution. In this instance, we can avoid the performance penalty of lock-based synchronization by using OpenMP's reduction construct. OpenMP reduction creates an independent, local copy of the reduction variable for each thread thereby eliminating sharing of the reduction variable during the threads' execution. At the end of the threads' executions, the local copies are combined into a single value based on the specified reduction operation.

TODO: Describe a better openmp strategy: truly parallel loops then reduction ...

Below we have a new version of shared memory selection using OpenMP's reduction construct:

.. activecode:: selection_omp_reduction
   :language: c
   :linkargs: ['-fopenmp']
   :caption: Selection using OpenMP

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

3.2.4 A Parallel Solution using Message Passing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Running!

TODO: Describe a general MPI strategy: distribute data, parallel loops, collect local minima, find global minimum ...

.. activecode:: selection_mpi
   :language: c
   :caption: Selection using MPI

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


TODO: breakdown the details of the MPI program

3.2.5 Comparing Performance of the Various Solutions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. Sprinting!?

TODO ...

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

TODO ...