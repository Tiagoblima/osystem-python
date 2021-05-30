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


class Partition:
    CAPACITY = 10000  # MB

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        self.available_capacity = self.CAPACITY
        self.slot = []

    def push_item(self, item):
        if self.available_capacity >= item.size:
            self.slot.append(item)
            self.available_capacity -= item.size

            if self.available_capacity > 0:
                print("Fragmentação Interna")
                print(f"Memory Available: {self.available_capacity}")
            return True
        else:
            return False


class Memory:

    def __init__(self, name="Queue", n_partitions=10):

        self.name = name
        self.n_partitions = n_partitions
        self.total_capacity = Partition("test").available_capacity * self.n_partitions
        self.partitions = [Partition(f"p{i}") for i in range(n_partitions)]
        self.available_capacity = Partition("test").CAPACITY * self.n_partitions
        self.available_partitions = self.partitions
        self.n_available_partitions = self.n_partitions
        self.total_partitions = self.n_partitions

    def first_fit(self, item):
        fails = 0
        for p in self.partitions:

            if p.push_item(item):
                print(f"Process {item.name} allocated at partition {p.name}")
                break
            else:
                fails += 1
        if fails is self.n_partitions:
            self.memory_status()
            raise Warning("Item not added, memory is full.")

    def get_item(self):
        return self.partitions.pop(0)

    def reset(self):
        self.partitions = [Partition(f"p{i}") for i in range(self.n_partitions)]

    def get_available_partitions(self):
        self.available_partitions = [p.slot for p in self.partitions
                                     if p.available_capacity != 0]
        return self.available_partitions

    def get_n_available_partitions(self):
        return len(self.get_available_partitions())

    def memory_status(self):
        self.available_capacity = [p.available_capacity for p in self.partitions]

        print("Memory Total Capacity: ", self.total_capacity)
        print("Memory Available Capacity: ", self.available_capacity)
        print("Available partitions:  ", self.get_available_partitions())

    def size(self):
        return self.total_capacity


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
        self.items = [(self.name, item) for item in range(0, random.randint(1000, 10000))]
        self.size = len(self.items)
        self.cur_state = self.states[0]
        self.cpu_time = 0
        print(f"{self.name} - {self.cur_state}")

    def run(self):
        self.cur_state = self.states[1]
        print(f"{self.name} - ", self.cur_state)
        start_time = time.time()

        while time.time() - start_time <= self.quantum and len(self.items) > 0:
            self.items.pop(0)
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
mem = Memory("READY QUEUE")
split = lambda config: config.split('=')
processes = []
for string_config in file.readlines()[1:]:
    config_dict = dict(list(map(split, string_config.split())))
    process = Process(name=config_dict['NAME'],
                      priority=int(config_dict['PRIORITY']),
                      cpu_bound=bool(config_dict['IO_BOUND']),
                      quantum=random.randint(5, 10))
    print(f'Inserindo o processo {process.name} na Memória')
    mem.first_fit(process)
    processes.append(process)
    print("-"*40)
    print()
mem.memory_status()
