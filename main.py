import time
import uuid
import argparse
import threading
# Printing random id using uuid1()
from time import sleep
import random

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', type=str)
args = parser.parse_args()


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
        print(f"STACK {self.name}: ", self.queue)

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

ready_queue = PriorityQueue("READY QUEUE")


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
    print(f'Turnround time {time.time()-start_time}')
    sleep(0.1)


def dispatcher():
    while ready_queue.size() > 0:
        process_, priority = ready_queue.get_item()
        print(f"The process {process_.name} is using the critical region and "
              f"it has {process_.remaining()} remaining items.")
        sleep(2)  # Fins the visualização
        try:
            process_.start()
        except RuntimeError:
            pass

        if not process_.finished():
            ready_queue.push_item((process_, priority + 1))
        else:
            print(f"The process: {process_.name} finished!")
            print(f"Processes in the")
            ready_queue.inspect_queue()
            sleep(10)  # Fins de visualização


"tempo médio de espera de todos os processos"


class Process(threading.Thread):
    states = ("READY", "EXECUTING", "BLOCKED")

    def __init__(self,
                 name,
                 priority,
                 cpu_bound,
                 quantum):
        threading.Thread.__init__(self)
        self.id = uuid.uuid1()
        self.name = name
        self.cpu_bound = cpu_bound
        self.io_bound = not cpu_bound
        self.priority = priority
        self.quantum = quantum
        self.items = [(self.name, item) for item in range(1, 5)]
        self.cur_state = self.states[0]
        self.cpu_time = 0
        print(f"{self.name} - {self.cur_state}")

    def run(self):
        self.cur_state = self.states[1]
        print(f"{self.name} - ", self.cur_state)
        start_time = time.time()

        while time.time() - start_time <= self.quantum and len(self.items) > 0:
            critical_region(self.items.pop(0))
            self.cpu_time += self.quantum
            sleep(1)

    def remaining(self):
        return len(self.items)

    def finished(self):
        return len(self.items) <= 0

    def inspect(self):
        info = "-" * 20 + "+PROCESS INFORMATION+" + "-" * 20 + \
               f"\n+NAME={self.name}\t+ID={self.id}\n" \
               f"+CPU_BOUND={self.cpu_bound}\t+IO_BOUND={self.io_bound}\n" \
               f"+PRIORITY={self.priority}\t+QUANTUM={self.quantum}\n" \
               '-' * 60

        return info


file = open(args.config_file)

split = lambda config: config.split('=')
processes = []
for string_config in file.readlines()[1:]:
    config_dict = dict(list(map(split, string_config.split())))
    thread = Process(name=config_dict['NAME'],
                     priority=int(config_dict['PRIORITY']),
                     cpu_bound=bool(config_dict['IO_BOUND']),
                     quantum=random.randint(5, 10))
    print(f'Inserindo o processo {thread.name} na fila')

    ready_queue.push_item((thread, thread.priority))
    processes.append(thread)

# Notify threads it's time to exit
start = time.time()
dispatcher()  # Executa os processos
total = time.time()-start
for thread in processes:
    print(f"Waiting time for {thread.name} is {total-thread.cpu_time}")

thread_exit_Flag = 1
buffer.inspect_stack()
queue.inspect_queue()

print("Exit Main Thread")
