import threading
# Printing random id using uuid1()
import time
import uuid
from time import sleep


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
