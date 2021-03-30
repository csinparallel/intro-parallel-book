3.3 Sieve of Eratosthenes
--------------------------

Author: Marc Smith, Vassar College

.. E-mail: mlsmith@smith.edu

.. Another array operation is finding a list of primes. Has a lot of dependencies. 



3.3.1 Introduction
^^^^^^^^^^^^^^^^^^^

The Sieve of Eratosthenes is an ancient algorithm for finding prime numbers.
Attributed to the Greek Mathematician Eratosthenes of Cyrene, it uses the
metaphor of a sieve, which separates wanted elements from unwanted elements.
In this case, the wanted elements are the prime numbers, and the unwanted
elements are the rest of the natural numbers.

What are prime numbers, anyway? Prime numbers are natural numbers
that are divisible only by themselves and one. The number 2 is the first prime
number, and the only even prime. The sieve algorithm removes all the remaining
natural numbers that are divisible by 2, effectively eliminating half the natural
numbers, which can’t be prime since they are divisible by 2. The next remaining
number after 2, then, is 3, so 3 is prime. Next the sieve removes all the remaining
multiples of 3, and so on.

Why all this fuss over prime numbers? It turns out that prime numbers play
an important role in encryption, and security. But our interest in generating
prime numbers is also for the pure excitement and challenge of doing so! There
is no known efficient mathematical formula for generating prime numbers, but
we do have algorithms we can implement for this purpose, and the Sieve of
Eratosthenes is the algorithm we will describe and implement in this chapter.

3.3.2 The Algorithm Unplugged
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To understand how the Sieve of Eratosthenes works, let's go through an unplugged 
example together. The following video explains how the sieve works. You can try 
this out yourself using pen and paper!

.. video:: video-ex1
   :controls:
   :thumb: /_images/whileloop.png

   http://media.interactivepython.org/thinkcsVideos/whileloop.mov

3.3.3 OpenMP Implementation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

An implementation of the algorithm in OpenMP

3.3.4 MPI Implementation 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
An implementation of the algorithm in MPI


3.3.5 Another Strategy - Using Go
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Short summary of what Go is; present a new algorithm

Implemetation of the new algorithm in Go
