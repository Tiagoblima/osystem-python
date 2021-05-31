import argparse
import random
import time

from memory.physical_memory import Memory
from memory.virtual_memory import VirtualMemory
from process.process import Process
from round_robin import Dispatcher

simulations = ["round_robin", 'physical_memory', "virtual_memory"]
parser = argparse.ArgumentParser()
parser.add_argument('--mode', type=int, required=True)
args = parser.parse_args()

PATH_TO_CONFIG = 'init.config'


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
    phy_mem = Memory("READY QUEUE")
    for process_ in process_list:
        print(f'Inserindo o processo {process_.name} na Memória')
        phy_mem.allocate(process_)
    phy_mem.memory_status()

elif args.mode == 3:

    vi_mem = VirtualMemory("READY QUEUE")
    for process_ in process_list:
        print(f'Inserindo o processo {process_.name} na Memória')
        vi_mem.allocate(process_)

    vi_mem.memory_status()
