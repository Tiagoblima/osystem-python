import time
import uuid

import numpy as np

SWAP = []


class Page:
    CAPACITY = 4  # KB

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        self.available_capacity = self.CAPACITY
        self.available = True

    def is_available(self):
        return self.available

    def fragmentation_status(self):
        print()
        print("FRAGMENTATION STATUS", end='')
        print('-' * 20)
        if self.available_capacity > 0:
            print("\tInternal Fragmentation")
            print(f"\tMemory Available Now: {self.available_capacity}MBs")
        else:
            print("\tNo Internal Fragmentation")
            print(f"\tMemory Available Now: {self.available_capacity}MBs")
        print("END FRAGMENTATION STATUS", end='')
        print('-' * 20)
        print()

    def push_item(self, space_required):
        if space_required > self.available_capacity:
            space_available = self.available_capacity
            self.available_capacity = 0
            self.fragmentation_status()
            return space_required - space_available

        elif space_required <= self.available_capacity:
            self.available_capacity -= space_required
            self.fragmentation_status()
            return 0

    def page_status(self):
        return self.name, f"Availability {(self.available_capacity / self.CAPACITY) * 100}%"


class VirtualMemory:

    def __init__(self, maximum_memory_size, page_size):

        self.n_pages = int(maximum_memory_size/page_size)
        self.total_capacity = Page("test").available_capacity * self.n_pages
        self.pages = [Page(f"p{i}") for i in range(self.n_pages)]
        self.available_capacity = Page("test").CAPACITY * self.n_pages

        self.pages_status = [p.page_status() for p in self.pages]

        self.n_available_pages = self.n_pages
        self.total_pages = self.n_pages

        self.reference_table = {**dict.fromkeys(self.pages, 0)}
        print(self.reference_table)
        self.page_map = {}
        self.process_map = {}

    def replace_page(self):

        less_recent_used = None
        minor_reference = np.Inf
        for page in self.reference_table.keys():
            if self.reference_table[page] < minor_reference:
                minor_reference = self.reference_table[page]
                less_recent_used = self.page_map[page]
        pages_used = self.process_map[less_recent_used]

        SWAP.append([(p.name, p) for p in pages_used])

        for page in pages_used:
            page.available_capacity = Page(page.name).CAPACITY
            self.pages[self.pages.index(page)] = page

    def allocate(self, process_):
        self.process_map[process_] = []

        process_space = process_.size  # The necessary space to allocate the process
        if process_space > self.get_available_capacity():
            print(f"Process {process_} not added, no partition available. "
                  f"The process size is {process_.size}MBs")
            print("Removing a process and placing it to the SWAP Memory.")
            print('-' * 40)
            time.sleep(3)

        for i, p in enumerate(self.pages):

            if p.is_available():
                process_space = p.push_item(process_space)
                print(f"Size to allocate: {process_space}MBs")

                self.page_map[p] = process_
                self.process_map[process_].append(p)
                self.reference_table[p] += 1
                print(f"Process {process_.name} allocated at page {p.name}")
                time.sleep(3)

            if process_space > 0:
                continue
            else:
                break

        if process_space == 0:
            print(f"Process {process_.name} allocated successfully!")
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
              f"{self.get_available_capacity()}MBs - {(self.available_capacity * 100) / self.total_capacity}%", )
        print("Pages Available:  ", self.get_n_available_pages())
        print(F"SWAP MEMORY: {SWAP}")
        time.sleep(3)

    def size(self):
        return self.total_capacity


print(F"SWAP MEMORY: {SWAP}")
