import _thread
import time
count = 0
while count < 10:
    def func1(q):
        print("q = {}".format(q))


    def func2(q):
        for x in range(5):
            q.append(x)
            func1(q)

            print("afer appeend queue = {}".format(q))


    q = []
    _thread.start_new_thread(func2, (q, ))
    #_thread.start_new_thread(func1, (q, ))

    while 1:
        print("hereA")
        pass
    print("here")
