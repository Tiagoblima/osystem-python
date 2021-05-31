import time
import uuid


# Printing random id using uuid1()


class Partition:
    CAPACITY = 20  # MB

    def __init__(self, name):
        self.id = uuid.uuid1()
        self.name = name
        self.available_capacity = self.CAPACITY
        self.slot = []

    def show_fragmentation_status(self):
        print('-' * 40)
        if self.available_capacity > 0:
            print("Internal Fragmentation")
            print(f"Memory Available Now: {self.available_capacity}MBs")
        else:
            print("No Internal Fragmentation")
            print(f"Memory Available Now: {self.available_capacity}MBs")
        print('-' * 40)

    def push_item(self, item):
        if self.available_capacity >= item.size:
            self.slot.append(item)
            self.available_capacity -= item.size

            self.show_fragmentation_status()
            return True
        else:
            return False


SWAP = []


class Memory:

    def __init__(self, name="Queue", n_partitions=10):

        self.name = name
        self.n_partitions = n_partitions
        self.total_capacity = Partition("test").available_capacity * self.n_partitions
        self.partitions = [Partition(f"p{i}") for i in range(n_partitions)]
        self.available_capacity = Partition("test").CAPACITY * self.n_partitions
        self.partitions_status = self.partitions
        self.n_available_partitions = self.n_partitions
        self.total_partitions = self.n_partitions

    def allocate(self, process_):
        fails = 0
        for p in self.partitions:

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
            for p_ in self.partitions:
                # For every process in the slot of the partition if the process size has the size of the current process
                # Remove it and place it in the SWAP memory.
                for pr in p_.slot:
                    if pr.size >= process_.size:
                        print(f"Removing the process {pr} from the partition {p_.name}")
                        time.sleep(3)
                        p_.slot.remove(pr)
                        print(f"Placing the process {pr} in the SWAP Memory")
                        time.sleep(3)
                        SWAP.append(pr)
                        print(f"Pushing the new process {process_} in the partition {p_.name}.")
                        time.sleep(3)
                        p_.push_item(process_)
                        return True
        return False

    def get_item(self):
        return self.partitions.pop(0)

    def reset(self):
        self.partitions = [Partition(f"p{i}") for i in range(self.n_partitions)]

    def get_partitions(self):
        self.partitions_status = [(p.name, f"Availability {(p.available_capacity / p.CAPACITY) * 100}%") for p in
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
