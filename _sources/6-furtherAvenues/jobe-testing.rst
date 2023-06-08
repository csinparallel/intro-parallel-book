This is a test page
---------------------






.. activecode:: gcc-no-pdc
   :language: c
   :compileargs: ['-Wall', '-Wextra', '-pedantic', '-fopenmp']
   :runargs: ['4', '10']
   :enabledownload:
 
    // A simple test for gcc compiler
    #include <stdio.h>
    #include <stdlib.h>
    #include "omp.h"

    int main (int argc, char **argv) {
      
      printf("num args = %d\n", argc);

      for (int i = 0; i<argc; i++) {
         printf("arg %d : %s \n", i, argv[i]);
      }

      int numthreads = atoi(argv[1]);
      omp_set_num_threads(numthreads);
      #pragma omp parallel
      {
        int id = omp_get_thread_num();
        int numThreads = omp_get_num_threads();
        printf("Hello from thread %d of %d\n", id, numThreads);
      }

      return 0;
    }

.. activecode:: pdc-cpp11
   :language: pdc
   :compiler: 'g++'
   :compileargs: ['-Wall', '-Wextra', '-pedantic', '-std=c++11', '-fopenmp']
   :runargs: ['4', '10']
   :enabledownload:

   // A simple test for C++11 compiler
    #include <iostream>
    #include <string>
    #include "omp.h"

    int main (int argc, char **argv) {
      
      std::cout << "num args = " << argc << "\n";

      for (int i = 0; i<argc; i++) {
         std::cout << "arg " << i << ": " << argv[i] << "\n";
      }

      int numthreads = atoi(argv[1]);
      omp_set_num_threads(numthreads);
      #pragma omp parallel
      {
        int id = omp_get_thread_num();
        int numThreads = omp_get_num_threads();
        printf("Hello from thread %d of %d\n", id, numThreads);
      }

      return 0;
    }



.. activecode:: pdc-gcc
   :language: pdc
   :compiler: 'gcc'
   :compileargs: ['-Wall', '-Wextra', '-pedantic',  '-fopenmp']
   :runargs: ['4', '10']
   :enabledownload:

   // A simple test for gcc compiler
    #include <stdio.h>
    #include <stdlib.h>
    #include "omp.h"

    int main (int argc, char **argv) {
      
      printf("num args = %d\n", argc);

      for (int i = 0; i<argc; i++) {
         printf("arg %d : %s \n", i, argv[i]);
      }

      int numthreads = atoi(argv[1]);
      omp_set_num_threads(numthreads);
      #pragma omp parallel
      {
        int id = omp_get_thread_num();
        int numThreads = omp_get_num_threads();
        printf("Hello from thread %d of %d\n", id, numThreads);
      }

      return 0;
    }

Simple CUDA code without command line arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. activecode:: pdc-nvcc-noargs
   :language: pdc
   :compiler: 'nvcc'
   :enabledownload:

    #include <stdio.h>
    #include <cuda_runtime.h>

    // !!!!!! NOTE:
    //  NVIDIA refers to these functions prefaced with __global__ 
    //  as 'kernel' functions that run on the GPU 'device'.
    __global__ void hello() {
        // special dim3 variables available to each thread in a kernel
        // or device function:
        // blockIdx    the x, y, z coordinate of the block in the grid
        // threadIdX   the x, y, z coordinate of the thread in the block
        printf("I am thread (%d, %d, %d) of block (%d, %d, %d) in the grid\n",
              threadIdx.x, threadIdx.y, threadIdx.z, 
              blockIdx.x, blockIdx.y, blockIdx.z );
    }

    // Note that this is called from the host, not the GPU device.
    // We create dim3 structs there and can print their components
    // with this function.
    void printDims(dim3 gridDim, dim3 blockDim) {
        printf("Grid Dimensions : [%d, %d, %d] blocks. \n",
        gridDim.x, gridDim.y, gridDim.z);

        printf("Block Dimensions : [%d, %d, %d] threads.\n",
        blockDim.x, blockDim.y, blockDim.z);
    }

    int main(int argc, char **argv) {

        // dim3 is a special data type: a vector of 3 integers.
        // each integer is accessed using .x, .y and .z 
        // (see printDims() above)

        // 1 dimensionsional case is the following: 1D grid of 1D block
        dim3 gridDim(1);      // 1 blocks in x direction, y, z default to 1
        dim3 blockDim(8);     // 8 threads per block in x direction

        // TODO: Try 128 threads in a block. What do you observe?
        //       Try the maximum threads per block allowed for your card.
        //       See device_info example.
        //       Try over the maximum threads per block for your card.
      
        printDims(gridDim, blockDim);
        
        printf("From each thread:\n");
        hello<<<gridDim, blockDim>>>();
        cudaDeviceSynchronize();     // need for printfs in kernel to flush

        return 0;
    }

Vactor Add with command line argument
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. activecode:: pdc-nvcc
   :language: pdc
   :compiler: 'nvcc'
   :runargs: ['256']
   :enabledownload:

      #include <math.h>   // ceil function
      #include <stdio.h>  // printf
      #include <iostream> // alternative cout print for illustration

      #include <cuda.h>

      void initialize(float *x, float *y, int N);
      void verifyCorrect(float *y, int N);
      void getArguments(int argc, char **argv, int *blockSize);

      
      #define cudaCheckErrors(msg) \
          do { \
              cudaError_t __err = cudaGetLastError(); \
              if (__err != cudaSuccess) { \
                  fprintf(stderr, "Fatal error: %s (%s at %s:%d)\n", \
                      msg, cudaGetErrorString(__err), \
                      __FILE__, __LINE__); \
                  fprintf(stderr, "*** FAILED - ABORTING\n"); \
                  exit(1); \
              } \
          } while (0)


      // Kernel function based on 1D grid of 1D blocks of threads
      // In this version, thread number is:
      //  its block number in the grid (blockIdx.x) times 
      // the threads per block plus which thread it is in that block.
      //
      // This thread id is then the index into the 1D array of floats.
      // This represents the simplest type of mapping:
      // Each thread takes care of one element of the result
      __global__ void vecAdd(float *x, float *y, int n)
      {
          // Get our global thread ID
          int id = (blockIdx.x * blockDim.x) + threadIdx.x;
      
          // Make sure we do not go out of bounds
          if (id < n)
              y[id] = x[id] + y[id];
      }

      ////////////////////                   main
      int main(int argc, char **argv)
      {
        printf("Vector addition using managed memory.\n");
        // Set up size of arrays for vectors 
        int N = 32*1048576;
        // TODO: try changng the size of the arrays by doubling or
        //       halving (32 becomes 64 or 16). Note how the grid size changes.
        printf("size (N) of 1D arrays are: %d\n\n", N);
        
        // host vectors, which are arrays of length N
        float *x, *y;

        // Size, in bytes, of each vector; just use below
        size_t bytes = N*sizeof(float);

        // 1.1 Allocate Unified Memory  accessible from CPU or GPU
        cudaMallocManaged(&x, bytes);
        cudaMallocManaged(&y, bytes);
        cudaCheckErrors("allocate managed memory");

        // 1.2 initialize x and y arrays on the host
        initialize(x, y, N);  // set values in each vector

        // Number of threads in each thread block
        int blockSize = 256;
        getArguments(argc, argv, &blockSize); //update blocksize from cmd line
      
        // Number of thread blocks in grid needs to be based on array size
        int gridSize = (int)ceil((float)N/blockSize);
      
        printf("add vectors on device using grid with ");
        printf("%d blocks of %d threads each.\n", gridSize, blockSize);
        // 2. Execute the kernel
        vecAdd<<<gridSize, blockSize>>>(x, y, N);
        cudaCheckErrors("vecAdd kernel call");

        // 3. Wait for GPU to finish before accessing on host
        cudaDeviceSynchronize();
        cudaCheckErrors("Failure to synchronize device");

        // 4. Check that the computation ran correctly
        verifyCorrect(y, N);

        printf("execution complete\n");

        // 5. free unified memory
        cudaFree(x);
        cudaFree(y);
        cudaCheckErrors("free unified memory");

        return 0;

      }

      // To reset the arrays for each trial
      void initialize(float *x, float *y, int N) {
        // initialize x and y arrays on the host
        for (int i = 0; i < N; i++) {
          x[i] = 1.0f;
          y[i] = 2.0f;
        }
      }

      // check whether the kernel functions worked as expected
      void verifyCorrect(float *y, int N) {
      
        float maxError = 0.0f;
        for (int i = 0; i < N; i++)
          maxError = fmax(maxError, fabsf(y[i]-3.0f));
        std::cout << "Max error: " << maxError << std::endl;
      }

      // simple argument gather for this simple example program
      void getArguments(int argc, char **argv, int *blockSize) {

        if (argc == 2) {
          *blockSize = atoi(argv[1]);
        }

      }

MPI  C Example
^^^^^^^^^^^^^^^

.. activecode:: pdc-mpicc
   :language: pdc
   :compiler: 'mpicc'
   :compileargs: ['-Wall', '-ansi', '-pedantic',  '-std=c99']
   :interpreterargs: ['-np 4']
   :enabledownload:

    /* conductorWorker.c
    * ... illustrates the basic conductor-worker pattern in MPI ...
    * Joel Adams, Calvin College, November 2009.
    *
    * Usage: mpirun -np N ./conductorWorker
    *
    * Exercise:
    * - Compile and run the program, varying N from 1 through 8.
    * - Explain what stays the same and what changes as the
    *    number of processes changes.
    */

    #include <stdio.h>
    #include <mpi.h>

    int main(int argc, char** argv) {
      int id = -1, numWorkers = -1, length = -1;
      char hostName[MPI_MAX_PROCESSOR_NAME];

      MPI_Init(&argc, &argv);
      MPI_Comm_rank(MPI_COMM_WORLD, &id);
      MPI_Comm_size(MPI_COMM_WORLD, &numWorkers);
      MPI_Get_processor_name (hostName, &length);

      if ( id == 0 ) {  // process 0 is the conductor 
        printf("Greetings from the conductor, #%d (%s) of %d processes\n",
                id, hostName, numWorkers);
      } else {          // processes with ids > 0 are workers 
        printf("Greetings from a worker, #%d (%s) of %d processes\n",
                id, hostName, numWorkers);
      }

      MPI_Finalize();
      return 0;
    }

mpic++ drug design code
^^^^^^^^^^^^^^^^^^^^^^^^
.. activecode:: pdc-mpic++
   :language: pdc
   :compiler: 'mpic++'
   :compileargs: ['-std=c++11']
   :interpreterargs: ['-np 8']
   :enabledownload:

    #include <cmath>
    #include <cstdlib>
    #include <algorithm>
    #include <iostream>
    #include <sstream>
    #include <string>
    #include <queue>
    #include <vector>
    #include <mpi.h>

    #define DEFAULT_max_ligand 7
    #define DEFAULT_nligands 120
    #define DEFAULT_nthreads 4
    #define DEFAULT_protein "the cat in the hat wore the hat to the cat hat party"

    #define MAX_BUFF 100
    #define VERBOSE 0  // non-zero for verbose output

    struct Pair {
      int key;
      std::string val;
      
      Pair(int k, const std::string& v) : key(k), val(v) {}
    };

    class Help {
    public:
      static std::string get_ligand(int max_ligand);
      static int score(const char*, const char*);
    };

    class MR {
    private:
      enum MsgType {
        GET_TASK, // worker request for a fresh ligand to score
        TASK_RESULT, // worker delivery of a score for a ligand
        ACK // protocol acknowledgment message
      };
      
      int max_ligand;
      int nligands;
      int nnodes;
      int rank;
      static const int root = 0;
      std::string protein;
      
      std::queue<std::string> tasks;
      std::vector<Pair> results;
      
      void Generate_tasks(std::queue<std::string>& q);
      //void Map(const std::string& str, std::vector<Pair>& pairs);
      void Sort(std::vector<Pair>& vec);
      int Reduce(int key, const std::vector<Pair>& pairs, int index, 
          std::string& values);
      
    public:
      const std::vector<Pair>& run(int ml, int nl, const std::string& p);
    };

    int main(int argc, char **argv) {
      int max_ligand = DEFAULT_max_ligand;
      int nligands = DEFAULT_nligands;
      std::string protein = DEFAULT_protein;
      
      if (argc > 1)
        max_ligand = strtol(argv[1], NULL, 10);
      if (argc > 2)
        nligands = strtol(argv[2], NULL, 10);
      if (argc > 3)
        protein = argv[4];
      // command-line args parsed
      
      MPI_Init(&argc, &argv);
      
      MR map_reduce;
      std::vector<Pair> results = map_reduce.run(max_ligand, nligands, protein);
      
      if(results.size()) {
        std::cout << "maximal score is " << results[0].key 
            << ", achieved by ligands " << std::endl 
            << results[0].val << std::endl;
      }
      
      MPI_Finalize();
      
      return 0;
    }

    const std::vector<Pair>& MR::run(int ml, int nl, const std::string& p) {
      max_ligand = ml;
      nligands = nl;
      protein = p;
      
      MPI_Comm_rank(MPI_COMM_WORLD, &rank);
      MPI_Comm_size(MPI_COMM_WORLD, &nnodes);
      
      char buff[MAX_BUFF];
      
      MPI_Status status;
      
      char empty = 0;
      
      if(rank == root) {
        // Only the root will generate the tasks
        Generate_tasks(tasks);
        
        // Keep track of which workers are working
        std::vector<int> finished;
        for(int i = 0; i < nnodes; ++i) {
          finished.push_back(0);
        }
        finished[root] = 1;  // master task does no scoring
        
        std::vector<Pair> pairs;
        
        // The root waits for the workers to be ready for processing
        // until all workers are done
        while([&](){ 
      for(auto i : finished) { if(!i) return 1; } 
      return 0; }()) {
          
          MPI_Recv(buff, MAX_BUFF, MPI_CHAR, MPI_ANY_SOURCE, MPI_ANY_TAG, 
            MPI_COMM_WORLD, &status);
          switch(status.MPI_TAG) {

          case GET_TASK:
      // Send the next task to be processed
      if(tasks.empty()) {
        MPI_Send((void*)&empty, 1, MPI_CHAR, status.MPI_SOURCE, ACK, 
          MPI_COMM_WORLD);
        
        // Mark the worker as finished
        finished[status.MPI_SOURCE] = 1;
      } else {
        MPI_Send((void*)tasks.front().c_str(), tasks.front().size() + 1, 
          MPI_CHAR, status.MPI_SOURCE, ACK, MPI_COMM_WORLD);
        tasks.pop();
      }
      break;

          case TASK_RESULT: {
      std::string buffstr(buff);
      std::stringstream stream(buffstr);
      std::string task;
      int score;
      
      stream >> task;
      stream >> score;
      pairs.push_back(Pair(score, task));
      if (VERBOSE) 
        std::cout << rank << ": " << task << " --> " << score << 
          " (received from " << status.MPI_SOURCE << ")" << std::endl;

          }
      break;

          default:
      break;
          }
        }
        
        // All tasks are done
        Sort(pairs);
        
        int next = 0;
        while(next < pairs.size()) {
          std::string values("");
          int key = pairs[next].key;
          next = Reduce(key, pairs, next, values);
          Pair p(key, values);
          results.push_back(Pair(key, values));
        }

      } else {
        // code for workers
        while(1) {
          
          // Receive the next task
          MPI_Send((void*)&empty, 1, MPI_CHAR, root, GET_TASK, MPI_COMM_WORLD);
          MPI_Recv(buff, MAX_BUFF, MPI_CHAR, root, ACK, MPI_COMM_WORLD, &status);
          
          if(!buff[0]) {
      // No more tasks to process
      break;
          } else {
      // Process the task
      std::string task(buff);
      int score = Help::score(task.c_str(), protein.c_str());
      if (VERBOSE) 
        std::cout << rank << ": score(" << task.c_str() << 
          ", ...) --> " << score << std::endl;
      
      // Send back to root, serialized as a stringstream
      std::stringstream stream;
      stream << task << " " << score;
      MPI_Send((void*)stream.str().c_str(), stream.str().size() + 1, MPI_CHAR, root, TASK_RESULT, MPI_COMM_WORLD);
          }
        }
      }
      
      return results;
    }

    void MR::Generate_tasks(std::queue<std::string> &q) {
      for (int i = 0;  i < nligands;  i++) {
        q.push(Help::get_ligand(max_ligand));
      }
    }


    void MR::Sort(std::vector<Pair>& vec) {
      std::sort(vec.begin(), vec.end(), [](const Pair& a, const Pair& b) {
          return a.key > b.key;
        });
    }

    int MR::Reduce(int key, const std::vector<Pair>& pairs, int index, std::string& values) {
      while(index < pairs.size() && pairs[index].key == key) {
        values += pairs[index++].val + " ";
      }
      
      return index;
    }

    std::string Help::get_ligand(int max_ligand) {
      int len = 1 + rand()%max_ligand;
      std::string ret(len, '?');
      for (int i = 0;	i < len;	i++)
        ret[i] = 'a' + rand() % 26;	
      return ret;
    }


    int Help::score(const char *str1, const char *str2) {
      if (*str1 == '\0' || *str2 == '\0')
        return 0;
      // both argument strings non-empty
      if (*str1 == *str2)
        return 1 + score(str1 + 1, str2 + 1);
      else // first characters do not match
        return std::max(score(str1, str2 + 1), score(str1 + 1, str2));
    }
