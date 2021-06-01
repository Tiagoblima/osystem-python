import math
import random
import time
import uuid

import numpy as np

from memory.physical_memory import PhysicalMemory

SWAP = []


class Page:
    CAPACITY = 4  # KB

    def __init__(self, name, id_):
        self.id = id_
        self.name = name
        self.size = self.CAPACITY
        self.available = True

    def is_available(self):
        return self.available

    def fragmentation_status(self):
        print()
        print(f"PAGE-{self.id} FRAGMENTATION STATUS", end='')
        print('-' * 20)
        if self.size > 0:
            print("\tInternal Fragmentation")
            print(f"\tMemory Available Now: {self.size}MBs")
        else:
            print("\tNo Internal Fragmentation")
            print(f"\tMemory Available Now: {self.size}MBs")
        print("END FRAGMENTATION STATUS", end='')
        print('-' * 20)
        print()

    def push_item(self, space_required):
        remaining_size = 0
        if space_required >= self.size:
            remaining_size = space_required - self.size
            self.size = 0
            self.available = False

        elif space_required < self.size:
            self.size -= space_required

        self.fragmentation_status()
        return remaining_size

    def page_status(self):
        return self.name, f"Availability {(self.size / self.CAPACITY) * 100}%"


class VirtualMemory:

    def __init__(self, maximum_physical_size, maximum_virtual_size, page_size):

        self.n_pages = int(maximum_virtual_size / page_size)
        self.initial_size = maximum_virtual_size
        self.available_size = maximum_virtual_size
        self.page_map = {}
        self.process_map = {}
        self.page_size = page_size
        self.total_pages = math.ceil(maximum_virtual_size / page_size)
        self.physical_memory = PhysicalMemory(maximum_physical_size)
        self.active_pages = 0
        self.total_used_pages = 0
        self.on_memory_pages = []
        self.page_misses = 0

    def test_physical_allocation(self, process_size):
        return self.calculate_pages(process_size) * self.page_size < self.physical_memory.available_capacity

    def test_virtual_allocation(self, process_size):
        return self.total_pages >= self.active_pages + self.calculate_pages(process_size)

    def calculate_pages(self, process_size):
        return math.ceil(process_size / self.page_size)

    def push_pages_to_memory(self, process_size):
        pages_allocated = []

        for p_id in range(self.total_used_pages, self.total_used_pages + self.calculate_pages(process_size)):
            print(f"Creating page: {p_id}")
            page = Page(f"page_{p_id}", p_id)
            process_size = page.push_item(process_size)
            self.physical_memory.allocate(page)
            self.page_map[page] = process_size
            self.on_memory_pages.append(page)
            pages_allocated.append(page)

        return pages_allocated

    def replace_page(self, process_size):
        pages_to_swap = self.calculate_pages(process_size)

        for i in range(pages_to_swap):
            page = self.on_memory_pages.pop(i)
            print(f"Swapping the page {page.name} out..")
            SWAP.append(page)
            new_page = Page(f"page_{self.total_used_pages + i}", self.total_used_pages + i)
            print(f"Created new page {new_page.name}")
            self.on_memory_pages.append(new_page)
            self.active_pages -= 1

        time.sleep(3)

    def get_process(self, process_id):

        for page in self.process_map[process_id]:

            if page not in self.on_memory_pages:
                self.page_misses += 1
            else:
                self.on_memory_pages.remove(page)
        return self.process_map.pop(process_id)

    def get_available_pages(self):
        return self.total_pages - self.active_pages

    def allocate(self, process):
        process_size = process.size
        print()
        print('-' * 20, end='')
        print("STARTING VIRTUAL MEMORY ALLOCATION", end='')
        print('-' * 20)
        print(f'Inserting the process {process.name} at Memory.')
        print(f'Size to allocate {process_size}')

        if self.test_virtual_allocation(process_size):

            self.process_map[process.id] = self.push_pages_to_memory(process_size)
            self.active_pages += len(self.process_map[process.id])
            self.total_used_pages += len(self.process_map[process.id])

            print(f"Pages on memory: {self.active_pages}")
            print(f"Available Pages: {self.get_available_pages()}")
            time.sleep(3)
        else:
            print("No memory available")
            print("Placing the pages in the SWAP Memory.")
            time.sleep(3)
            self.replace_page(process_size)
            self.allocate(process)

    def memory_status(self):
        print('-' * 20, end='')
        print("VIRTUAL MEMORY STATUS", end='')
        print('-' * 20)
        print(f"Total Capacity: {self.initial_size}MBs")
        print(f"Total Initial Pages {self.total_pages}")
        print(f"Pages on Memory {self.active_pages}")
        print(f"Total on SWAP {len(SWAP)}")
        print(f"Total pages {self.active_pages + len(SWAP)}")
        print(f"Total page miss {self.page_misses}")
        print('-' * 20, end='')
        print("END VIRTUAL MEMORY STATUS", end='')
        print('-' * 20)


print(F"SWAP MEMORY: {SWAP}")
