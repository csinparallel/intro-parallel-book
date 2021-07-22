from multiprocessing import Process

def sayHi(id):
    print("Hello from {}!".format(id))

def main():
    numProcesses = 20
    for i in range(numProcesses):
        p = Process(target=sayHi, args=(i, ))
        p.start()

if __name__ == '__main__':
    main()
