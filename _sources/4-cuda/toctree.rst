CHAPTER 4: GPU Computing Basics with CUDA C
:::::::::::::::::::::::::::::::::::::::::::

**Author:** Libby Shoop, Macalester College

**To Cite:**

Shoop, Libby. "GPU Computing Basics with CUDA C". *PDC for Beginners*, edited by CSinParallel. 
2022. Available Online.

Computing using GPUs is often reffered to as massively parallel computing, because we use Graphical Processing Unit devices that contain thousands of cores. 

Manycore computing is and exciting technology that drives a great deal of cutting edge computing in Artificial Intelligence (inparticalur Deep Learning in generative AI), Robotics, and a variety of scientific research, such as weather forcasting, biofinformatics, genomics, proteomics, modeling of various physical and chemical systems.

For NVIDA GPU cards, one software system to code in is CUDA (Compute Unified Device Architecture), which has compilers for C, C++, and Fortran. 

.. ?? Point students toward NVIDIA's interactive CUDA course or Udacity's tensorflow course. ??

*Language used for these examples:* C, with special additions for compiling for executing on a GPU, referred to as CUDA C.

.. toctree::
    :maxdepth: 2

    .. gpu.rst

    1-gpu-device.rst
    2-cuda-model-dim3.rst
    3-cuda-thread-mapping.rst
    4-VectorAdd.rst
    5-VectorAddUM.rst
    6-VectorAddTiming.rst

