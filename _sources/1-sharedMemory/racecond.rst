1.2 Race Conditions
-------------------------------------------
This section builds on the simple fork-join and SPMD patterns and introduces the notion of a race condition. By the end of this section, you should be 
able to define what a race condition is, identify race conditions in sample code, and extrapolate some strategies for fixing them.

1.2.1 Estimating the Area Under a Curve
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As our next example, let's look at the problem of estimating the area under a curve. If you have taken a calculus course, you may recognize this 
problem as the Riemann sum or Trapezoidal, which approximates the area under the curve (i.e. the integral) by splitting the area under the curve 
into a series of trapezoids. 

In the following programs, we attempt to use the trapezoid rule to approximate the integral 

.. math::

    \int_0^{\pi} sin(x)_{dx}

using :math:`2^{20}` equal subdivisions. The answer from this computation should be 2.0. The following video shows how a single thread would solve this problem:

.. video:: video-integration1
   :controls:
   :thumb: images/int_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/workshops/numerical_integration_1_thread.mov

In this example, the single thread serially computes the area of each trapezoid and adds all the trapezoids together to one value. 

A C implementation of this program may look like the following:

.. activecode:: rc_integration_serial
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (serial)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>

   //function we are calculating the area under
   double f(double x) {
      return sin(x);
   }

   //estimation of pi
   const double pi = 3.141592653589793238462643383079;

   int main(int argc, char** argv) {
      //Variables
      double a = 0.0, b = pi;         //limits of integration
      int n = 1048576;                //number of subdivisions = 2^20
      double h = (b - a) / n;         //width of each subdivision
      double integral;                // accumulates answer

      integral = (f(a) + f(b))/2.0;  //initial value
      
      //sum up all the trapezoids
      int i;
      for(i = 1; i < n; i++) {
          integral += f(a+i*h);
      }  

      integral = integral * h;
      printf("With %d trapezoids, our estimate of the integral from \n", n);
      printf("%f to %f is %f\n", a,b,integral);

      return 0;
   }


.. mchoice:: rc_mc_ser_1
    :correct: a
    :answer_a: The program works as expected (outputs answer 2.0)
    :answer_b: The program returns a different approximate value (but the same value with every run) 
    :answer_c: The program returns a different approximate value every run.
    :feedback_a: Correct! The area under the curve sums to 2. 
    :feedback_b: Not quite. Did you try and run the code block above?
    :feedback_c: Try again. Did you run the code block above?

    Run the above serial implementation of integration a few times. What do you discover?  


Let's now consider how we can use multiple threads to approximate the area under the curve in parallel. One strategy would be to 
assign each thread a *subset* of the total set of subdivisions, so that each thread separately computes its assigned set of trapezoids.

The following video illustrates how 4 threads would work together to approximate the area under the curve:

.. video:: video-integration2
   :controls:
   :thumb: images/int2_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/workshops/numerical_integration_4_threads.mov



.. mchoice:: rc_mc_tpdp_1
    :correct: a
    :answer_a: Task parallelism
    :answer_b: Data parallelism
    :answer_c: Neither
    :feedback_a: Correct! In this example, each thread is assigned a separate subset of rectangles, and are working together to solve the larger problem.
    :feedback_b: Incorrect. Remember that in data parallelism, each thread is operating on a different unit of data or memory.
    :feedback_c: Actually, it is one of the options listed!

    Is estimating the area under the curve an example of data parallelism or task parallelism? 


1.2.2 Parallel Integration - First Attempt
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
One of the advantages of OpenMP is the ability to incrementally add parallelism to a program. Using what we learned about the fork-join pattern and available 
pragams in the last section, let's update the serial version of the integration program with OpenMP pragmas:

.. activecode:: rc_integration_par1
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (parallel - first attempt)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> //<--- added the omp header file

   //function we are calculating the area under
   double f(double x) {
      return sin(x);
   }

   //estimation of pi
   const double pi = 3.141592653589793238462643383079;

   int main(int argc, char** argv) {
      //Variables
      double a = 0.0, b = pi;         //limits of integration
      int n = 1048576;                //number of subdivisions = 2^20
      double h = (b - a) / n;         //width of each subdivision
      double integral;                // accumulates answer

      integral = (f(a) + f(b))/2.0;  //initial value
      
      //sum up all the trapezoids
      int i;

      #pragma omp parallel for private(i) shared (a, n, h, integral)  //<--- added this line
      for(i = 1; i < n; i++) {
          integral += f(a+i*h);
      }  

      integral = integral * h;
      printf("With %d trapezoids, our estimate of the integral from \n", n);
      printf("%f to %f is %f\n", a,b,integral);

      return 0;
   }

Our parallel implementation adds just two lines the serial code. First, we include the header file ``<omp.h>``, in order to 
access all the functions available to us in the OpenMP library. The second line is the inclusion of the ``omp parallel for`` 
pragma on line 26. 

Recall that the ``omp parallel for`` pragma combines the functionality of the ``omp parallel``  and ``omp for`` pragmas we covered in the last section. 
Specifically, the ``omp parallel for`` pragma:

* creates a team of threads
* assigns each thread a subset of iterations of the for loop
* joins the threads back into a single threaded process at the end of the for loop.

For a machine running 4 threads, each thread receives *n*/4 (in this case 262,144) iterations of the for loop, with each thread running 
its subset of the for loop in parallel. The ``omp parallel for`` pragma has some additional clauses. The ``private(i)`` clause 
states that the variable i is *private* to each thread. In other words, each thread has its own copy of variable ``i``. In contrast, the 
``shared(a, n, h, integral)`` clause specifies that the variables ``a``, ``n``, ``h``, and ``integral`` are *shared* amongst the threads.
In other words, there is exactly one copy of the ``a``, ``n``, ``h``, and ``integral`` variables, and all the threads have equal access 
to them.

If our program is parallelized correctly, the program should estimate the area under the curve as 2.00, which would be identical to the 
output of the serial program. 


.. mchoice:: rc_mc_par_1
    :correct: c
    :answer_a: The program works as expected (outputs answer 2.0)
    :answer_b: The program returns a different approximate value (but the same value with every run) 
    :answer_c: The program returns a different approximate value every run.
    :feedback_a: Not quite. Try running the program a few more times. What do you see?
    :feedback_b: Close, but not correct. Try running the program again. Do you really get the same answer?
    :feedback_c: Correct. Something is seriously wrong with our program!

    Run the OpenMP implementation of integration a few times. What do you discover?  


.. mchoice:: rc_mc_par_2
    :correct: b
    :answer_a: This scenario illustrates a classic limitation of task parallelism.
    :answer_b: The program is losing values or overwriting values somewhere. 
    :answer_c: Fairies have infested the computer and are wrecking havoc as we speak. 
    :answer_d: It's some other issue.
    :feedback_a: Nope. This is actually not an issue with task parallelism. We can reproduce the issue with data parallelism too.
    :feedback_b: Correct! Can you figure out why?
    :feedback_c: Nope! Thankfully, our servers are fairy-proof. :)
    :feedback_d: Actually, the issue is listed in one of the options!

    Do you have any guesses on what could be causing the issue?  

1.2.3 Returning to the Array Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While some may find it tempting to point the finger at task parallelism for our incorrect result, the truth is that 
we can get an incorrect result even when employing the SPMD pattern. Suppose we modify the populating array problem to 
one of array addition. In other words, instead of simply populating an array with random values, we are adding up the 
values in the array in parallel.  

Here is a modified code snippet with the ``omp parallel for`` pragma placed in the correct place but commented out. Since 
the sum of *n* elements from :math:`1 \ldots n` is :math:`\frac{n(n+1)}{2}`, we know the sum when *n* is 20 million 
is a really long number: 200,000,010,000,000. 

Here is an updated code snippet that has the pragma around the sum commented out. Running it should confirm that the 
sum is the long value shown above.

.. activecode:: rc_add_array
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Array example - parallel sum

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> //<--- added the omp header file

   #define N 20000000 //size of the array

   int main(void){

       int * array = malloc(N*sizeof(int)); //declare array of size N
       int i;

       //populate array
       #pragma omp parallel for  //<-- from our earlier example
       for (i = 0; i < N; i++) {
           array[i] = i+1;
       }
       printf("Done populating %d elements!\n", N);
       printf("Summing elements together...\n");

       long sum = 0;
       //#pragma omp parallel for
       for (i = 0; i < N; i++) {
           sum+= array[i];
       }
       printf("Sum is: %ld\n", sum);

       return 0;
   }


.. mchoice:: rc_mc_array_1
    :correct: b
    :answer_a: Yes, the program always prints out the correct result.
    :answer_b: No, the result is different every time.  
    :feedback_a: Incorrect. Did you remember to uncomment the pragma? Did you run the code a few times?
    :feedback_b: Correct! Once again, the program is losing or overwriting values somewhere...

    Now uncomment the pragama on line 22 and re-run the program a few times. Do you always get the correct result?


1.2.4 Race Conditions and Critical Sections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To understand what is going on, let's use an analogy to describe 
the process of adding an array in parallel.


.. video:: video-racecond12
   :controls:
   :thumb: images/race_conditions1_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/raceconditions1-2.mov.mov

To understand what is going on, we need to define a few new terms, specifically **race condition** 
**critical section**, and **lock**. Watch the following video to learn what these terms mean:

.. video:: video-racecond3
   :controls:
   :thumb: images/race_conditions3_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/raceconditions3.mov.mov

.. dragndrop:: dnd-rc-1
   :feedback: Feedback that is displayed if things are incorrectly matched.
   :match_1: arises when two or more threads attempt to modify a shared variable ||| race condition
   :match_2: smallest set of instructions that must execute sequentially to ensure correctness |||critical section
   :match_3: a mechanism by which to protect a resource |||lock
   :match_4: common pattern that often causes race conditions|||read-modify-write

   Match descriptions that best define each term.


Let's watch another video that explains how these mechanisms can help fix the issue in our program:

.. video:: video-racecond4
   :controls:
   :thumb: images/race_conditions4_thumb.png

   https://d32ogoqmya1dw8.cloudfront.net/files/csinparallel/raceconditions4.mov.mov

The ``omp critical`` pragma allows a programmer to define a critical section. At an 
initial glance, it is tempting to place the ``omp critical`` pragma around the 
statement ``sum+=array``. However, since the critical section should be as small as possible,
its necessary to separate the summing of the array elements from the update to the shared sum variable.

The following program does just that:


.. activecode:: rc_add_array_fixed
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (parallel - first attempt)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> //<--- added the omp header file

   #define N 20000000 //size of the array

   int main(void){

       int * array = malloc(N*sizeof(int)); //declare array of size N
       int i;

       //populate array
       #pragma omp parallel for  //<-- from our earlier example
       for (i = 0; i < N; i++) {
           array[i] = i+1;
       }
       printf("Done populating %d elements!\n", N);
       printf("Summing elements together...\n");

       long sum = 0;
       #pragma omp parallel shared(sum)
       {
           int x;
           long local_sum = 0; //variables local to each thread

           #pragma omp for
           for (x = 0; x < N; x++) {
               local_sum += array[x]; //each thread computes a local sum
           }

           #pragma omp critical
           {
               sum+= local_sum; //read-modify-write of sum variable
           }
       }
       printf("Sum is: %ld\n", sum);

       return 0;
   }

If you are having trouble understanding how the ``sum+=local_sum`` statement 
on line 34 translates to a read-modify-write pattern, recall that a single 
line of code often translates to multiple instructions in assembly. The 
line can also be written as ``sum = sum + local_sum``. This single line 
of code involves:

* reading the ``sum`` variable (and ``local_sum`` variable)
* adding the values of ``sum`` and ``local_sum`` together, and 
* writing the total to the ``sum`` variable.


Lastly, observe that fixing the race condition added several lines to 
our program. One way to fix this is to use a new pragma called 
``omp atomic``. The ``omp atomic`` pragma forces the program to 
treat the enclosed section as being **atomic**, or something 
that is executed without interruption.

The following program illustrates how the ``omp atomic`` pragma
can be used to shorten the program:

.. activecode:: rc_add_array_atomic
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (parallel - first attempt)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> //<--- added the omp header file

   #define N 20000000 //size of the array

   int main(void){

       int * array = malloc(N*sizeof(int)); //declare array of size N
       int i;

       //populate array
       #pragma omp parallel for  //<-- from our earlier example
       for (i = 0; i < N; i++) {
           array[i] = i+1;
       }
       printf("Done populating %d elements!\n", N);
       printf("Summing elements together...\n");

       long sum = 0;
       #pragma omp parallel for
       for (i = 0; i < N; i++) {
           #pragma omp atomic 
           sum+= array[i];
       }
       printf("Sum is: %ld\n", sum);

       return 0;
   }


.. mchoice:: rc_mc_array_2
    :correct: a
    :answer_a: The revised program is slower.
    :answer_b: Both versions of the program take an equal amount of time to execute.  
    :answer_c: The revised program is faster.
    :answer_d: The program is impossible to revise. You always get a syntax error.
    :feedback_a: Correct! In fact, it is so slow it exceeds runestone's time limit!
    :feedback_b: Incorrect. Did you try modifying the program and re-running it?
    :feedback_c: Incorrect. Did you try modifying the program and re-running it?
    :feedback_d: No, it's fixable. Try replacing the world 'atomic' with the word 'critical'.

    Try replacing the ``omp atomic`` pragma (line 24) with the ``omp critical`` pragma and re-run the program. What happens?

In the next section, we cover a technique called reduction that offers another alternative.
