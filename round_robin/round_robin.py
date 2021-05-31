import threading
import time
# Printing random id using uuid1()
from time import sleep


class Queue:
    def __init__(self, name="Queue"):
        self.queue = []
        self.name = name

    def push_item(self, item):
        self.queue.append(item)

    def get_item(self):
        return self.queue.pop(0)

    def reset(self):
        self.queue = []

    def inspect_queue(self):
        print(f"QUEUE {self.name}: ", self.queue)

    def inspect_next_item(self):
        print(f"{self.name} NEXT ITEM", self.queue[0])

    def size(self):
        return len(self.queue)


class PriorityQueue:
    def __init__(self, name="PriorityQueue"):
        self.queue = []
        self.name = name

    def push_item(self, item):
        self.queue.append(item)
        self.queue = sorted(self.queue, key=lambda tup: tup[1])

    def get_item(self):
        return self.queue.pop(0)

    def reset(self):
        self.queue = []

    def inspect_queue(self):
        print(f"PriorityQueue {self.name}: ", self.queue)

    def inspect_next_item(self):
        print(f"{self.name} NEXT ITEM", self.queue[0])

    def size(self):
        return len(self.queue)


class Stack:

    def __init__(self, name="stack"):
        self.stack = []
        self.name = name

    def push_item(self, item):
        self.stack.append(item)

    def get_item(self):
        return self.stack.pop(-1)

    def reset(self):
        self.stack = []

    def inspect_next_item(self):
        print(f"{self.name} NEXT ITEM: ", self.stack[-1])

    def inspect_stack(self):
        print(f"STACK {self.name}: ", self.stack)

    def size(self):
        return len(self.stack)


thread_exit_Flag = 0
buffer = Stack("Shared Buffer1")

BUFFER_MAX_SIZE = 5

crLock = threading.Lock()

queue = Queue("Shared Queue")


def critical_region(new_item):
    start_time = time.time()
    crLock.acquire()
    buffer.push_item(new_item)
    if buffer.size() > BUFFER_MAX_SIZE:
        used_item = buffer.get_item()
        queue.push_item(used_item)
        print(f"The item {used_item} was used.")
    crLock.release()
    sleep(0.3)
    print(f'Turnround time {time.time() - start_time}')
    sleep(0.1)


class Dispatcher:

    def __init__(self):

        self.ready_queue = PriorityQueue("READY QUEUE")

    def execute(self):
        while self.ready_queue.size() > 0:
            process_, priority = self.ready_queue.get_item()
            print(f"The process {process_.name} is using the critical region and "
                  f"it has {process_.remaining()} remaining items.")
            sleep(2)  # Fins the visualização
            try:
                process_.start()
            except RuntimeError:
                pass

            if not process_.finished():
                self.ready_queue.push_item((process_, priority + 1))
            else:
                print(f"The process: {process_.name} finished!")
                print(f"Processes in the")
                self.ready_queue.inspect_queue()
                sleep(10)  # Fins de visualização

    def add_process_list(self, process_list):
        for process in process_list:
            self.ready_queue.push_item((process, process.priority))

    def get_queue(self):
        return self.ready_queue

    @staticmethod
    def watch():
        thread_exit_Flag = 1
        buffer.inspect_stack()
        queue.inspect_queue()


print("Exit Main Thread")
"tempo médio de espera de todos os processos"
