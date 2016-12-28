import threading
import time

class DummyThread():
    def __init__(self):
        self.counter = 0     
    def run(self):
        for _idx in range(10):
            time.sleep(1)

    def test(self):
        def increment():
            for _idx in range(10):
                self.counter += 1

        thread = threading.Thread(target=increment)
        thread.start()
            
# thread0 = DummyThread("Thread 0")
# thread0.start()

# thread1 = DummyThread("Thread 1")
# thread1.start()

# # Enumerate all active threads
# # If run from notebook, this will print some daemon threads used by Jupyter
# for _thread in threading.enumerate():
#     print("Name: {}, daemon: {}".format(_thread.name, _thread.daemon))


a = DummyThread()
a.test()
time.sleep(10)
print(a.counter)

