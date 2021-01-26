4.1 MapReduce
---------------

Modern Internet search engines must process truly enormous amounts of data.  For example, Google search gathers information from hundreds of billions of web pages, and produces an index of every word that appears on every web page, requiring `over 100,000,000,000,000,000 (10^17) bytes of data <https://www.google.com/search/howsearchworks/crawling-indexing/>`_! How is it possible to perform such a huge computation in a reasonable amount of time?  

Distributed computing using a MapReduce strategy is a common approach to performing such “big data” computations.  By using 
Map-Reduce on clusters of thousands of powerful networked  computers, the work can be divided up among those  computers in order to complete in hours what would take a  single computer years to perform. Those computers are typically part of a cloud computing service provided by companies such as Amazon, Google, or Microsoft.  The open-source MapReduce framework Hadoop, used by over half of Fortune 500 companies, is designed for reliability, making it possible to continue a computation  with minimal delay even if computers or networks crash during the job.  

In this section, we will describe the MapReduce programming model and explore how to create programs capable of true big-data computations. 

4.1.1 The MapReduce programming strategy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A MapReduce framework such as Hadoop provides most of the details of data handling, such as dividing enormous data sets up into *splits* that are small enough for one computer to process, managing the low-level input and output operations, replicating the data to prevent data loss if one or more computers or networks crash, and automatically recovering from such crashes during a big-data computation.  Thus, an application programmer never writes the "main program" for a MapReduce computation, which is unlike other programs in this book.  Instead, the programmer writes two functions that determine how the framework should process the data, called the mapper and the reducer.  

- The *mapper* function operates on the input data and generates *key-value pairs* that represent some information of interest from that input. 

  For example, if we are interested in finding all occurrences of words in a data set of web pages, a mapper function might operate on one line of a web page and produce a key-value pair for each word in that line, where the key is that word and the value is the name of that web page, e.g., ``("the", "mysite/index.html")``.    

- The *reducer* function acts on all key-value pairs produced by mappers *that have the same key* and produces other key-value pairs that distill or summarize the interesting information in those input pairs.  

  For example, if we're interested in how frequently each word appears in each web page, and the input key-value pairs have the form ``("the", "mysite/index.html")``, then a reducer might produce key-value pairs of the form ``("the mysite/index.html", "28")`` where 28 is the count of input pairs matching that web-page value.  

Figure 1 shows the effects of calling mappers on each line of each split of input data, then calling reducers on the various key-value pairs produced by those mappers.  

.. figure:: mapreduce_Figure1.jpg
    :width: 720px
    :align: center
    :height: 540px
    :alt: alternate text
    :figclass: align-center

    Figure 1: Illustration of calling a mapper function named ``map()`` many times in parallel and passing the results of those calls to calls of a reducer function named ``reduce()``.

As Figure 1 shows, each reducer call handles all the key-value pairs for a particular key.  For instance, in our example above of counting the frequencies of words within web pages, if the key K1 in the diagram is the word ``"the"`` and the values v1, v2, and v3 are the names of three different web pages such as ``"mysite/index.html"`` and two others, then the top reducer would handle all three of those pairs (plus any other unshown pairs that have the key ``"the"``).

By writing the mapper and reducer functions for a MapReduce framework, a programmer specifies what computation should be performed on a potentially gigantic data set.  This modest two-function programming strategy provides a surprising amount of algorithmic control for big-data computations.  Here are some examples, starting with the word-frequency example above:

#. Goal
     Count frequencies of all words in all web pages in a data set of web pages
   mapper.
     Read one line of input from a web page *``wpname``*, and produce a key-value pair ``(`` *"w"* ``,`` *"wpname"* ``)`` for each word *w* that appears on that line
   reducer
     Receive all key-value pairs ``(`` *"w"* ``,`` *"wpname"* ``)`` for a given word *w*, and produce one key-value pair ``(`` *"w wpname"* ``,`` *"ct"* ``)`` for each web page *wpname*, where *ct* is the number of input pairs with value *wpanme*.
#. Goal
     For every word found in a data set of web pages, produce a list of all line numbers of web pages containing that word.
   mapper
     Read one line of input from a web page *wpname*, and produce a key-value pair ``(`` *"w"*, *"ln wpname"* ``)`` for each word *w* that appears on that line, where *ln* is the line number within *wpname* that was read
   reducer
     Receive all key-value pairs ``(`` *"w"* ``,`` *"ln wpname"* ``)`` for a given word ``*w*``, and produce one key-value pair ``(`` *"w wpname"* ``,`` *"ln1 ln2 ln3 ..."* ``)`` for each web page *wpname*, where *lnN*`` is the *N*th value of *ln* among input pairs with values *ln wpname*.
#. Goal
     Find the average rating for each movie in a data set of movie ratings.
   mapper
     Read one movie rating, consisting of an integer movie id *mid*, an integer rating *r* from 0 to 5, and other information such as reviewer and date.  Produce a pair ``(`` *"mid"* ``,`` *"r"* ``)``
   reducer
     Receive all key-value pairs ``(`` *"mid"* ``,`` *"r"* ``)`` for a given movie id *mid*, and produce a pair ``(`` *"mid"* ``,`` ``*"ave"* ``)`` where *ave* is the average value of *r* among all those input pairs.  

Besides providing the mapper and reducer, a MapReduce programmer must also provide configuration options for the framework, e.g., specifying where to find the data set, what type of data that data set contains, where to store the results, perhaps indicating how to split the data set, etc. 

Note that a MapReduce framework also provides an automated sorting of all key-value pairs produced by all mapper calls, after all mapper calls and before any reducer calls.  The framework needs this automated sorting operation, called the *shuffle*, in order to gather all key-value pairs having the same key for calls of the reducer.  For big data jobs requiring thousands of networked computers, shuffling may be a complex intensive computation of its own - another reusable service that a MapReduce framework provides - and that we don't need to program ourselves!

Finally, a MapReduce framework also implements crucial performance features.  For example, retrieving data from a local disk is much faster than retrieving that data over a network, so a framework insures that mapper calls occur on a computer whose local disks contain their splits, and that reducer calls likewise occur on computers that contain their input data locally.  Only shuffling requires global movement of data over a network, as illustrated in Figure 2.  

.. figure:: mapreduce_Figure2.png
    :width: 230px
    :align: center
    :height: 150px
    :alt: alternate text
    :figclass: align-center

    Figure 2: How each computer in a cluster breaks up the work and runs
    mappers locally, then shuffles the key-value pair results by key and
    sends the results for each key to other computers who run reducers.

xxxxx

Talk about web-search in particular, and introduce the notion of the cloud.

Give students an overview of the MapReduce paradigm, and then explain how they can access/play with it. 

Talk about WebMapReduce, and give them a link to play with. 

Also talk about Amazon EC2 clusters, and how they can run their own MapReduce jobs on those.
