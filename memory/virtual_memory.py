import time
import uuid
import argparse
import threading
# Printing random id using uuid1()
from time import sleep
import random

import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', type=str)
args = parser.parse_args()

SWAP = []


class Page:
    CAPACITY = 4  # KB

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        self.available_capacity = self.CAPACITY
        self.available = True

    def is_available(self):
        return self.available_capacity > 0

    def fragmentation_status(self):
        if self.is_available():
            print("Internal Fragmentation")
            print(f"Memory Available Now: {self.available_capacity}KBs")
        else:
            print("No Internal Fragmentation")
            print(f"Memory Available Now: {self.available_capacity}KBs")

    def push_item(self, space_required):
        if space_required > self.available_capacity:
            self.available_capacity = 0
            self.fragmentation_status()
            return space_required - self.available_capacity

        elif space_required <= self.available_capacity:
            self.available_capacity -= space_required
            self.fragmentation_status()
            return 0

    def page_status(self):
        return self.name, f"Availability {(self.available_capacity / self.CAPACITY) * 100}%"


class VirtualMemory:
    MAXIMUM_MEMORY = 400000  # KBs

    def __init__(self, n_pages=10000):

        self.n_pages = n_pages
        self.total_capacity = Page("test").available_capacity * self.n_pages
        self.pages = [Page(f"p{i}") for i in range(n_pages)]
        self.available_capacity = Page("test").CAPACITY * self.n_pages

        self.pages_status = [p.page_status() for p in self.pages]

        self.n_available_pages = self.n_pages
        self.total_pages = self.n_pages

        self.page_map = {}
        self.reference_table = {}

    def replace_page(self):

        less_recent_used = None
        minor_reference = np.Inf
        for process_ in self.page_map.keys():
            if self.reference_table[process_] < minor_reference:
                minor_reference = self.reference_table[process_]
                less_recent_used = self.page_map[process_]
        process_, pages = self.page_map.pop(less_recent_used)
        self.available_capacity += sum([p.size for p in pages])
        SWAP.append((process_, pages))

    def allocate(self, process_):
        self.page_map[process_] = []
        fails = 0
        process_space = process_.size  # The necessary space to allocate the process
        if process_space > self.get_available_capacity():
            print(f"Process {process_} not added, no partition available. "
                  f"The process size is {process_.size}MBs")
            print("Removing a process and placing it to the SWAP Memory.")
            time.sleep(3)

        for p in self.pages:
            process_space = p.push_item(process_space)
            if process_space > 0:
                self.page_map[process_].append(p.name)
                print(f"Process {process_.name} allocated at page {p.name}")
                time.sleep(3)
                continue
            else:
                fails += 1
        if process_space == 0:
            self.reference_table[process_] = 1
        else:
            self.replace_page()
            self.allocate(process_)

        return False

    def get_item(self):
        return self.pages.pop(0)

    def reset(self):
        self.pages = [Page(f"p{i}") for i in range(self.n_pages)]

    def get_pages_available(self):
        return [p for p in self.pages if p.available_capacity > 0]

    def get_available_capacity(self):
        self.available_capacity = sum([p.available_capacity for p in self.get_pages_available()])
        return self.available_capacity

    def get_n_available_pages(self):
        return len(self.get_pages_available())

    def memory_status(self):

        print("Memory Total Capacity: ", self.total_capacity)
        print(f"Total Memory Available: "
              f"{self.get_available_capacity()}KBs - {(self.available_capacity * 100) / self.total_capacity}%", )
        print("Pages Available:  ", self.get_n_available_pages())

        time.sleep(3)

    def size(self):
        return self.total_capacity


class Process(threading.Thread):
    states = ("READY", "EXECUTING", "BLOCKED")

    def __init__(self,
                 name,
                 priority,
                 cpu_bound,
                 quantum,
                 size):
        threading.Thread.__init__(self)
        self.id = uuid.uuid1()

        self.name = name
        self.cpu_bound = cpu_bound
        self.io_bound = not cpu_bound
        self.priority = priority
        self.quantum = quantum
        self.items = [(self.name, item) for item in range(0, size)]
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
                      quantum=random.randint(5, 10),
                      size=int(config_dict['SIZE']))
    print(f'Inserindo o processo {process.name} na Memória')
    mem.first_fit(process)
    processes.append(process)
    print("-" * 40)
    print()
mem.memory_status()
print(F"SWAP MEMORY: {SWAP}")
