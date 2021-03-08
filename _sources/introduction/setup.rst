0.6 Getting Access to a Parallel System
----------------------------------------

Most computers today have processors that can support parallel execution of programs. Since almost all machines these days contain *multicore processors*, you can use those multiple cores to locally run many of the examples in this book. Since our book already supports interactive multi-threaded execution, you can 
run some of our smaller examples directly on the browser. 

The message passing examples in our book are not yet interactive. Therefore, you will need access to a computer that supports message pasing to run them. 
Note that message passing examples can be run on multicore systems. However, accessing a *cluster* of computers is often a better illustrates the power 
of message passing to communicate between computers.  

Installing these libraries on different operating systems is specific to each OS. There are quite a few references available for doing this.

The code for the examples
^^^^^^^^^^^^^^^^^^^^^^^^^^

ZZZ Tarball of patternlets of just mpi4py examples here. Note that prepared raspberry pi images contain this code.

This book presents each of the examples found in this code file archive. You should read about each one and then try it on your system where you have the above mentioned software packages installed.

On the system where you have the code installed, you should use a terminal to navigate to the folder called patternlets/mpi4py. On the Raspberry Pi cluster based on the images created by the CSinParallel group, the command is:

.. code:: bash

  cd CSinParallel/patternlets/mpi4py


Using a Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^
If you don't have a quad-core laptop or multicore machine that you can readily connect to, a potentially inexpensive option is to use a Raspberry Pi single 
board computer. The Raspberry Pi is a credit-card sized single board computer that costs under $50.00 with all components. You can run all the shared memory code
directly on a Raspberry Pi Computer. If you have multiple Raspberry Pis, you can also build a cluster to locally run the distributed computing examples in this 
book.

The Raspberry Pi cluster images provided by the CSinParallel group already have everything you need installed, including the following code examples that we describe in detail in the following chapters.

**Remote Desktop Setup Instructions**:
While you can connect peripherals (such as mouse, keyboard and monitor) directly to the Raspberry Pi, and alternative is to hook the Pi up to a laptop and use 
Virtual Network Client (VNC) to remote desktop into your pi. The instructions here helpfully illustrate how to connect a remote Desktop environment between 
a Raspberry Pi and a laptop.

**Raspberry Pi Cluster Setup Instructions**:

There are many tutorials on-line on how to create a Raspberry Pi cluster. Here are some useful resources for building your own Raspberry Pi cluster.


Using Cloud Resources
---------------------

Another way to get access to multicore and distributed systems is through cloud access. Include directions for access cloud resources here. 

