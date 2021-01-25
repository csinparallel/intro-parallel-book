4.1 MapReduce
---------------

Modern Internet search engines must process truly enormous amounts of data.  For example, Google search gathers information from hundreds of billions of web pages, and produces an index of every word that appears on every web page, requiring `over 100,000,000,000,000,000 (10^17) bytes of data <https://www.google.com/search/howsearchworks/crawling-indexing/>`_! How is it possible to perform such a huge computation in a reasonable amount of time?  

Distributed computing using a Map-Reduce strategy is a common approach to performing such “big data” computations.  By using 
Map-Reduce on clusters of thousands of powerful networked  computers, the work can be divided up among those  computers in order to complete in hours what would take a  single computer years to perform. Those computers are typically part of a cloud computing service provided by companies such as Amazon, Google, or Microsoft.  The open-source Map-Reduce systems Hadoop, used by over half of Fortune 500 companies, is designed for reliability, making it possible to continue a computation  with minimal delay even if computers or networks crash during the job.  

In this section, we will describe the Map-Reduce model and explore how to create programs capable of true big-data computations. 

4.1.1 The Map-Reduce programming strategy
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Talk about web-search in particular, and introduce the notion of the cloud.

Give students an overview of the MapReduce paradigm, and then explain how they can access/play with it. 

Talk about WebMapReduce, and give them a link to play with. 

Also talk about Amazon EC2 clusters, and how they can run their own MapReduce jobs on those.
