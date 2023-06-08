4.5 Vector Addition example with CUDA Unified Memory
-----------------------------------------------------

NVIDIA GPUS are now capable of making it easier to manage the memory copying for us with a feature called **unifed memory**. Recently, this is often referred to as **CUDA managed data**, to signify that the data in memory and its movement (if needed) is managed for the programmer.

Unified Memory works on any NVIDIA GPU with SM architecture, or compute capability, of 3.0 or higher. Recall when we first examined a device's information, the first line of output from the device_info program gives us  information like this:

     with Compute 8.6 capability

Your GPU may be different, but as long as it is above 3.0, you should be able to run the code given here.

.. note::

  If you have a smaller NVIDIA Jetson single-board computer, you should use unified memory, aka CUDA managed data, because the hardware is suited for this.

This method is now preferred
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We provided the previous example with the original explicit data copying primarily because you will encounter many CUDA examples on the Web that still show this way of writing CUDA code. However, it is our experience that the device cards that you will encounter today have the capability of handling CUDA managed memory very well, and you should use it.

In the previous example, the description of the steps was as follows:

1. Allocate 2 arrays, x and y, on the **host** and initialize them with data.
2. Allocate 2 arrays d_x, and d_y, on the GPU **device**.
3. Copy each of the arrays from the host to the device.
4. Perform the addition on the device using a kernel function, keeping result in d_y.
5. Ensure that the device is finished with the computation.
6. Copy the resulting array d_y from the device to the host, back into array y.
7. Check that the computation ran correctly.
8. Free memory on the device and the host.

When using managed memory, the program steps are:

1. Allocate 2 arrays, x and y, as managed data arrays used on the **host** and the **device**. Initialize them with data.
2. Perform the addition on the device using a kernel function, keeping result in y.
3. Ensure that the device is finished with the computation.
4. Check that the computation ran correctly.
5. Free the unified data memory

Fewer steps and simpler code- what's not to like?

The main program
^^^^^^^^^^^^^^^^^^^^

The kernel function for vector addition and the helper functions are exactly the same as the previous example. It is helpful to just look at how the main() function has changed. Note the numbers of the steps in English given above are in comments in the code.

Filename: *3-UMVectorAdd/vectorAdd.cu*

.. literalinclude:: code/cuda/3-UMVectorAdd/vectorAdd.cu
  :language: c
  :caption: Vector Addition CUDA Program (version 2 with managed data)
  :lines: 56-108

.. note::
  The most important point about this example is that the data copying hasn't changed from the previous manual example: it's just being done for us.


Build and run
^^^^^^^^^^^^^^^^

You can use the make command on your own machine or compile the code like this:

.. code-block:: bash

   nvcc -arch=native  -o vectorAdd vectorAdd.cu

Remember that you will need to use a different -arch flag if native does not work for you. (See note at end of section 4.1.)

You can execute this code like this:

.. code-block:: bash

   ./vectorAdd

The result should be the same as the previous example.

.. code-block:: bash

  Vector addition using managed memory.
  size (N) of 1D arrays are: 33554432

  add vectors on device using grid with 131072 blocks of 256 threads each.
  Max error: 0
  execution complete

Note the default block size (threads per block) used in the code. You can try increasing it or decreasing it by adding the block size as an argument, like this:

.. code-block:: bash

   ./vectorAdd 128

What you know now is that this can be changed and the code still runs correctly. In the next section we will introduce how to time our code so that we can determine if changes like this have any affect on the code's performance.


An Exercise
^^^^^^^^^^^

For paractice writing a kernel function, you could try computing something different using each element of the arrays. For example, multiply each element in x by a constant and add another constant, placing the new computed value into array y at that element. Or you could get more sophisticated by using other math library functions, such as sqrt. Remember that you will need to verify whether the result is correct by updating the function that does this.


