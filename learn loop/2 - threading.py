import threading
from random import randint
def say_hello(arg):
    # print(arg)
    for i in range(arg):
        print('Hello', i)

t1 = threading.Thread(target=say_hello, args=[randint(1,5)])
t2 = threading.Thread(target=say_hello, args=[randint(1,5)])
t3 = threading.Thread(target=say_hello, args=[randint(1,5)])

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()