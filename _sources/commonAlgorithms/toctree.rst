CHAPTER 3: Common Algorithmic Patterns
::::::::::::::::::::::::::::::::::::::

Several of the sample problems we have discussed this far have been embarassingly parallel. 

Computations are largely independent of each other. 

Introduce the notion of a dependency, and how dependenecies can limit the amount of parallelism inherent in a program. 

In this chapter, we cover common algorithmic patterns and their parallel implementations to show readers what 
strategies to use when parallelizing more complex tasks. 


.. toctree::
    :maxdepth: 2

    sorting.rst
    selection.rst
    sieve.rst
    sharedq.rst
    matmul.rst
