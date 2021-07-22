from multiprocessing import Process, Queue
import time

def parrotSpeak(id, q):
    msg = q.get()
    while(msg != "DONE"):
        print("Parrot {} says: *squawk* *whistle* {} *squawk*".format(id, msg))
        time.sleep(0.1)
        msg = q.get()

def main():
    print("START")
    numProcesses = 2
    q = Queue()
    messages = ["Time for a cracker!",
                "I need a vacation.",
                "This perch is comfy!",
                "Time for dinner!",
                "What'd you say?",
                "Where did you go today?",
                "Did you bring me any treats?",
                "I wonder what the other birds are doing right now.",
                "DONE",
                "DONE"]

    p1 = Process(target=parrotSpeak, args=(1, q))
    p2 = Process(target=parrotSpeak, args=(2, q))
    p1.start()
    p2.start()

    print("Main process will now sleep, to show that the child processes block on q.get()...")
    time.sleep(3)
    print("Main process is done sleeping. Ready to put messages on the queue!")
    for i in range(len(messages)):
        q.put(messages[i])

if __name__ == '__main__':
    main()
