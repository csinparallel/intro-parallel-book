1.3 Reduction
---------------------------------

The following program shows how to fix the integration example using the ``omp atomic`` pragma.

Take a look at the updated program below:

.. activecode:: rd_integration
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (parallel - using reduction)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> 

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

      #pragma omp parallel for 
      for(i = 1; i < n; i++) {
          #pragma omp atomic //<--- added this line
          integral += f(a+i*h);
      }  

      integral = integral * h;
      printf("With %d trapezoids, our estimate of the integral from \n", n);
      printf("%f to %f is %f\n", a,b,integral);

      return 0;
   }


Another way to solve this issue is to employ the concept of **reduction**. The notion of a reduction comes from the mathematical operation 
*reduce*, in which a collection of values are combined into a single value via a common mathematical function. Summing up a collection of 
values is therefore a natural example of reduction. OpenMP provides the ``reduction`` clause for the ``omp parallel for`` pragma to show 
that reduction should be used. The following example shows the integration example fixed using ``reduction`` clause:

.. activecode:: rd_integration2
   :language: c
   :compileargs: ['-Wall', '-ansi', '-pedantic', '-std=c99']
   :linkargs: ['-lm', '-fopenmp']
   :caption: Integration (parallel - using reduction)

   #include <stdio.h>
   #include <math.h>
   #include <stdlib.h>
   #include <omp.h> 

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

      #pragma omp parallel for private(i) shared (a, n, h) reduction(+: integral)//<-- modified this line
      for(i = 1; i < n; i++) {
          integral += f(a+i*h);
      }  

      integral = integral * h;
      printf("With %d trapezoids, our estimate of the integral from \n", n);
      printf("%f to %f is %f\n", a,b,integral);

      return 0;
   }

The reduction clause (``reduction(+: integral)``) indicates that the addition operation should be used for reduction, and that that the final reduced value will be stored in the variable ``integral``. 
Note also that the ``integral`` variable was also removed from the ``shared`` clause.


1.3.1 How reduction actually works
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Explain what a reduction is and how that is an alternative.

Introduce the reduction patternlet. 

Ask students to modify their array addition programs to use reduction.




So far, we have introduced three different ways to deal with race conditions:

* use the ``omp critical`` pragma
* use the ``omp atomic`` pragma
* use a ``reduction`` clause

OpenMP offers programmers multiple ways to deal with race conditions, because some 
techniques may be faster in different contexts. In the next section, we will 
discuss how to measure performance.