import argparse
import random
import time

from memory.physical_memory import PhysicalMemory
from memory.virtual_memory import VirtualMemory
from process.process import Process
from round_robin import Dispatcher

simulations = ["round_robin", 'physical_memory', "virtual_memory"]
parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=int, required=True)
args = parser.parse_args()

PATH_TO_CONFIG = 'init.config'
PARTITION_SIZE = 20  # MB
MEMORY_SIZE = 200  # MB

MAXIMUM_PHYSICAL_MEMORY = 200  # MBs
MAXIMUM_VIRTUAL_MEMORY = 350  # MBs
PAGE_SIZE = 50  # MB


def load_processes(config_file):
    processes = []
    file = open(config_file)
    split = lambda config: config.split('=')
    for string_config in file.readlines()[1:]:
        config_dict = dict(list(map(split, string_config.split())))
        process = Process(name=config_dict['NAME'],
                          priority=int(config_dict['PRIORITY']),
                          cpu_bound=bool(config_dict['IO_BOUND']),
                          quantum=random.randint(5, 10),
                          size=int(config_dict['SIZE']))
        processes.append(process)
    return processes


process_list = load_processes(PATH_TO_CONFIG)

if args.mode == 1:
    start = time.time()
    dispatcher = Dispatcher()  # Executa os processos
    dispatcher.add_process_list(process_list)
    dispatcher.execute()

    total = time.time() - start
    for thread in process_list:
        print(f"Waiting time for {thread.name} is {total - thread.cpu_time}")

    dispatcher.watch()

elif args.mode == 2:
    phy_mem = PhysicalMemory("Physical Memory",
                             memory_size=MEMORY_SIZE,
                             partition_size=PARTITION_SIZE)
    counter = 0
    while True:
        process = Process(name=f"Thread-{counter}",
                          priority=random.randint(-10, 10),
                          cpu_bound=bool(random.randint(0, 1)),
                          quantum=random.randint(5, 10),
                          size=random.randint(5, PARTITION_SIZE))
        phy_mem.allocate(process)

        if counter % 5 == 0:
            phy_mem.memory_status()
        counter += 1
elif args.mode == 3:

    while True:
        vi_mem = VirtualMemory(MAXIMUM_PHYSICAL_MEMORY,MAXIMUM_VIRTUAL_MEMORY, PAGE_SIZE)
        for process_ in process_list:
            vi_mem.allocate(process_)
        print("LOADING PROCESS", end='')
        print("-"*40)
        for process_ in process_list:
            print(f'Loading the process {process_.name} from the Memory')
            vi_mem.get_process(process_.id)
        vi_mem.memory_status()
