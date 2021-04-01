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

In addition to restructured text, runestone chapters contain Runestone 
Directives (see the 
[Runestone Author Guide](https://runestone.academy/runestone/static/authorguide/index.html) 
for details). Runestone Directives allow the integration of many interactive 
content, such as videos, multiple choice questions, parson problems and others. 


The follow example illustrates how a particular section may be set up using 
restructured text and Runestone directives:

```
3.x This is a section heading
----------------------------------------

Section content would go here. Notice how the number of hyphens/dashes extend 
past the section heading. The number of hyphens must be at least as long as 
the section title itself.

Here is an example of **bold** text. Here is an example of *italicized* text. 
This (:math:`a^2 + b^2 = c^2`) is an example of an in-lined LaTeX math equation.

The following is an example of an standalone math equation:

.. math::
   
   \sum_{i=0}^n i \equiv \frac{n \times (n + 1}{2}



3.x.1: This is a subsection heading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Notice how the carats (^) must be at least as long as the subsection heading 
text. 

Here is an example of a URL: `CSinParallel <csinparallel.org>`_

Here is how a video may be included (from the Runestone documentation):

.. video:: video-ex1
   :controls:
   :thumb: /_images/whileloop.png

   http://media.interactivepython.org/thinkcsVideos/whileloop.mov

```

## Previewing your work

There are two main commands that an author needs to know in order to preview 
their work locally. 

### runestone build

Use the `runestone build` command to locally compile your changes. Most 
warnings can be ignored. If the project does not build for whatever reason, 
contact CSinParallel at csinparallel@stolaf.edu. 

### runestone serve

Use the `runestone serve` command to launch the server (typically at 
https://localhost:8000). We recommend having the local server open at at all 
times and having a separate window to do your compiling. You will need to 
reload your browser to see any new changes.

### Trouble shooting tips

Here are some helpful tips if you find yourself getting stuck

* If `runestone build` does not work, check your Runestone version. If it 
  is 5.6.0 or later, open up `conf.py` and ensure line 21 reads
  `from runestone import runestone_static_dirs, runestone_extensions, setup`
  (notice the addition of `, setup` at the end of the command). 


* Make sure that your runestone objects have unique keys. If you reuse keys, 
  there will be build errors. 

* The video format has to be in `mov` format for Runestone to interpret it. 
  Annoying, yes, but a tool like `ffmpeg` can automatically do the conversion 
  for you. A command like the following usually works (for mp4 to mov):
  `ffmpeg -i video.mp4 -f mov video.mov`. If you don't have access to the 
  command line or having difficulties with ffmpeg, send a link to your mp4 
  video to csinparallel@stolaf.edu and we will convert it for you. 

## Merging changes back in

*PDC For Beginners* uses the [fork and pull model](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)
for collaborative development. 

When you are ready to share your changes, please create a
[Git Pull Request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). 
GitHub also has specific documentation on how to [create a pull request from 
a fork](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork)

After we review your work, it will be merged into the main branch of the 
repository. We will rebuild the book on our sever soon after!


## Questions

If you have any questions or concerns, please contact the CSinParallel team at 
csinparallel@stolaf.edu


