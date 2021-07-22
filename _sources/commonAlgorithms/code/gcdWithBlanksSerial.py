NUM_BLOCKS = 50
PAIRS_PER_BLOCK = 20000
MIN_VALUE = 1000
MAX_VALUE = 10000000000000000
NUM_WORKERS = 1
VERBOSE = False

def gcd(a, b):
    while a != 0:
        a, b = b%a, a
    return b

from multiprocessing import Process, Queue
import timeit
import random
random.seed(99)

def buildInputs(inputQ):
    for i in range(_______________): #a
        block = []
        for i in range(_______________): #b
            block.append([random.randint(MIN_VALUE, MAX_VALUE), random.randint(MIN_VALUE, MAX_VALUE)])
        inputQ.put(block)

    # use sentinels to avoid possible race condition (multiple checks for not empty, then one gets, other hangs on get)
    for i in range(_______________): #c
        inputQ.put("DONE")

def computeGCDs(id, inputQ, outputQ):
    block = _______________ #d
    while(block != _______________): #e
        blockOutput = []
        for i in range(_______________): #f
            pair = block[i]
            blockOutput.append([id, pair[0], pair[1], gcd(pair[0], pair[1])])
        outputQ.put(blockOutput)
        block = _______________ #d

def processOutputs(outputQ):
    for i in range(NUM_BLOCKS):
        blockOutput = outputQ.get()
        for i in range(PAIRS_PER_BLOCK):
            result = blockOutput[i]
            if (VERBOSE):
                print("i={} p{}: gcd({}, {}) = {}".format(i, result[0], result[1], result[2], result[3]))
    print("All requested GCD's computed.")

def gcdSequential():
    print("----------\ngcdSequential")
    inputQ = Queue()
    outputQ = Queue()

    buildInputs(inputQ)
    startTime = timeit.default_timer()
    computeGCDs(0, inputQ, outputQ)
    processOutputs(outputQ)
    elapsedTime = timeit.default_timer() - startTime
    print("Elapsed time (s):", elapsedTime)
    return elapsedTime

def main():
    print("NUM_BLOCKS: {}\nPAIRS_PER_BLOCK: {}\nMIN_VALUE: {}\nMAX_VALUE: {}\nNUM_WORKERS: {}".format(NUM_BLOCKS, PAIRS_PER_BLOCK, MIN_VALUE, MAX_VALUE, NUM_WORKERS))
    seqTime = gcdSequential()

if __name__ == '__main__':
    main()
