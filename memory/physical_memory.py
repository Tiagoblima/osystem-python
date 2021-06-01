import random
import time
import uuid


# Printing random id using uuid1()


class Partition:

    def __init__(self, name, size):
        self.id = uuid.uuid1()
        self.name = name
        self.initial_capacity = size
        self.available_capacity = size
        self.slot = []

    def show_fragmentation_status(self):
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

    def free_up(self):
        self.available_capacity = self.initial_capacity
        return self.slot.pop()

    def is_available(self):
        return self.initial_capacity == self.available_capacity

    def push_item(self, item):
        if item.size <= self.available_capacity:
            self.slot.append(item)
            self.available_capacity -= item.size
            self.show_fragmentation_status()
            return True
        else:
            return False


SWAP = []


class PhysicalMemory:

    def __init__(self, name="Queue", memory_size=1000, partition_size=10):
        assert memory_size >= partition_size, f"Memory size cannot be smaller than the partition size. " \
                                              f"Got memory_size={memory_size}, partition_size={partition_size}"
        self.name = name
        self.n_partitions = int(memory_size / partition_size)
        self.total_capacity = Partition("test", partition_size).initial_capacity * self.n_partitions
        self.partitions = [Partition(f"p{i}", partition_size) for i in range(self.n_partitions)]
        self.available_capacity = Partition("test", partition_size).initial_capacity * self.n_partitions
        self.partitions_status = self.partitions
        self.n_available_partitions = self.n_partitions
        self.total_partitions = self.n_partitions

    def swap_out(self):

        random_partition = random.randint(0, self.n_partitions-1)
        process_to_swap = self.partitions[random_partition].free_up()
        print(f"Removing the process {process_to_swap} from the partition {self.partitions[random_partition].name}")
        time.sleep(3)
        print(f"Placing the process {process_to_swap} in the SWAP Memory")
        time.sleep(3)
        SWAP.append(process_to_swap)
        return random_partition

    def allocate(self, process_):
        fails = 0
        print()
        print('-'*20, end='')
        print("STARTING ALLOCATION", end='')
        print('-' * 20)
        print(f'Inserindo o processo {process_.name} na Memória')

        if process_.size > int(self.total_capacity/self.n_partitions):
            raise Warning("Cannot allocate process bigger than the partition size.")

        for p in self.partitions:

            if p.is_available():
                if p.push_item(process_):
                    print(f"Process {process_.name} allocated at partition {p.name}")
                    time.sleep(3)
                    return True
            else:
                fails += 1

        if fails is self.n_partitions:
            print(f"Process {process_} not added, no partition available. "
                  f"The process size is {process_.size}MBs")
            print("Removing a process and placing it to the SWAP Memory.")
            time.sleep(3)
            random_partition = self.swap_out()
            print(f"Pushing the new process {process_} in the partition {self.partitions[random_partition].name}.")
            self.partitions[random_partition].push_item(process_)
            time.sleep(3)
        print()
        print('-'*20, end='')
        print("END ALLOCATION", end='')
        print('-' * 20)
        return False

    def get_item(self):
        return self.partitions.pop(0)

    def reset(self):
        self.partitions = [Partition(f"p{i}", int(self.total_capacity/self.n_partitions))
                           for i in range(self.n_partitions)]

    def get_partitions(self):
        self.partitions_status = [(p.name, f"Availability {(p.available_capacity / p.initial_capacity) * 100}%") for p
                                  in
                                  self.partitions
                                  ]
        return self.partitions_status

    def get_n_available_partitions(self):
        return len(self.get_partitions())

    def memory_status(self):
        self.available_capacity = [p.available_capacity for p in self.partitions]

        print("Memory Total Capacity: ", self.total_capacity)
        print(f"Partitions Available Capacity: "
              f"{sum(self.available_capacity)}MBs - {(sum(self.available_capacity) * 100) / self.total_capacity}%", )
        print("Partitions:  ", self.get_partitions())
        print(f"Total Memory Available: {sum(self.available_capacity)}MBs")
        print(F"SWAP MEMORY: {SWAP}")
        time.sleep(3)

    def size(self):
        return self.total_capacity
