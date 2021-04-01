## Information for Contributing Authors

If you are interested in contributing to *PDC For Beginners*, please 
reach out to CSinParallel at csinparallel@stolaf.edu

## Setting up the local authoring environment
Thanks for contributing to *PDC For Beginners*! To set up the local authoring 
environment, please complete the following steps:

## Installing Runestone

*PDC For Beginners* is built using the Runestone environment. While you don't 
need to understand the internals of Runestone, you will need a local instance 
of Runestone to preview your section. Please visit the [Runestone Quickstart 
Installation Guide](https://pypi.org/project/runestone/) for details. In 
general, it's recommended that you run Runestone in a virtual environment 
(like virtualenv). You will need at least Python 3.7 and pip (or pip3) 
installed on your system.

The following set of commands work for most users (taken from the Runestone 
Installation Guide): 

```
$ sudo pip install virtualenv
$ virtualenv /path/to/home/MyEnv
$ source /path/to/home/MyEnv/bin/activate
```

Within the virtual environment, use `pip` (or `pip3`) to install runestone:

```
pip install runestone
```

Note that if you have separate instances of Python 2.* and Python 3.* on your
system, you may need to use `pip3` instead. 

## Fork the PDC For Beginners GitHub repository

Fork the *PDC For Beginners* GitHub repository by visiting 
[this link](https://github.com/csinparallel/intro-parallel-book) and 
clicking on the "Fork" icon in the top right-hand corner. 

Chapter content is added to the `_sources/` directory. For example, if you are 
a chapter 3 section author, your section will be located under 
`_sources/commonAlgorithms` as a separate .rst file.

## Writing content

*PDC for Beginners* is written using Runestone components and restructured 
text (reST). The following [cheat sheet](http://openalea.gforge.inria.fr/doc/openalea/doc/_build/html/source/sphinx/rest_syntax.html)
is a useful guide for the different markup components needed to write a document 
using restructured text.

A section contribution may have the following outline:

```
3.x This is a section heading
----------------------------------------

Section content would go here. Here is an example of **bold** text. Here 
is an example of *italicized* text. This (:math:`a^2 + b^2 = c^2`) is an 
example of an in-lined LaTex math equation.

The following is an example of an standalone math equation:

.. math::
   
   \sum_{i=0}^n i \equiv \frac{n \times (n + 1}{2}



3.x.1: This is a subsection heading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Notice how the carats (^) must be at least as long as the subsection heading 
text. 

Here is an example of a URL: `CSinParallel <csinparallel.org>`_

```


