
CHAPTER 1: Shared Memory
:::::::::::::::::::::::::

Programmers can utilize several languages and libraries to program shared-memory multiprocessors. In this chapter, we will discuss **OpenMP** (or Open Muliti-Processing), a standard API for multithreading that has existed for over 25 years. A key advantage of OpenMP over other API and libraries is its use of **pragmas**, or compiler directives that indicate where in a program parallelism should occur. The actual task of 
creating and destroying teams of threads is done automatically and silently by the compiler, abstracting away many details that make writing 
multithreaded applications difficult. In addition, OpenMP makes it possible for programmers to *incrementally* add parallelism to their programs. 


.. Use analogy or unplugged activity to remind users how shared memory computations work (e.g. Jigsaw Analogy)

.. toctree::
    :maxdepth: 2

    preliminaries.rst
    firststeps.rst
    racecond.rst
    reduction.rst
    drugdesign.rst
