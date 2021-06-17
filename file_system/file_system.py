import argparse
import math
import os
import json
import random
import time
import uuid


def name_exists(dir_, element_info):
    for element in dir_:
        print(element)
        if dir_[element]["name"] == element_info["name"]:
            return True
    return False


class Block:
    CAPACITY = 10  # KB

    def __init__(self, id_):
        self.id = id_

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

    def block_status(self):
        return self.id, f"Availability {(self.size / self.CAPACITY) * 100}%"

    def block_info(self):
        return {"block_id": self.id, "space_available": self.size}


class FileSystem:
    TOTAL_CAPACITY = 100000  # MB
    ROOT_DIR = 'usr'

    def __init__(self):
        self.memory = []
        inode = str(uuid.uuid1())
        self.inode_map = {
            "usr/system.txt": inode
        }
        block1 = Block(random.randint(0, 10000))
        block2 = Block(random.randint(0, 10000))
        block1.push_item(10)
        block2.push_item(10)

        root_blocks = [block1.block_info(), block2.block_info()]

        self.memory.extend(root_blocks)
        block1 = Block(random.randint(0, 10000))
        block2 = Block(random.randint(0, 10000))
        block1.push_item(10)
        block2.push_item(10)

        self.memory.append(block1)
        self.memory.append(block2)

        self.directores = {

            self.ROOT_DIR: {
                "nome": self.ROOT_DIR, "size": 20, "block": root_blocks,
                "archives":
                    {
                        inode: {
                            "size": 10,
                            "name": "system.txt",
                            "block": [block1.block_info()]
                        },
                        "sys":
                            {
                                "size": 10,
                                "name": "sys",
                                "archives": {},
                                "block": [block2.block_info()]
                            }
                    }
            }
        }
        self.current_dir = self.ROOT_DIR

    def allocate(self, path_to_element, element_info, is_dir=False):
        path = path_to_element.split('/')

        if len(path) == 1:
            self.directores[self.current_dir][path[0]] = element_info
        elif not is_dir:
            search_dir = self.directores
            for i, path_part in enumerate(path):

                if i == len(path) - 2:
                    inode = str(uuid.uuid1())

                    if not name_exists(search_dir[path_part]["archives"], element_info):
                        element_info["block"] = []
                        space_required = element_info["size"]
                        for elem in range(math.ceil(element_info["size"] / Block.CAPACITY)):
                            block = Block(random.randint(0, 1000))
                            block.push_item(space_required)
                            element_info["block"].append(block.block_info())
                            space_required -= block.CAPACITY
                            self.memory.append(block)
                        search_dir[path_part]["archives"][inode] = element_info
                        self.inode_map[path_to_element] = inode

                    else:
                        raise Warning("Name already exists file or director not created!")
                    break
                else:

                    search_dir = search_dir[path_part]["archives"]
            search_dir = self.directores
            time.sleep(3)
            for part_path in path[:-1]:
                search_dir[part_path]["size"] += element_info["size"]
                search_dir = search_dir[part_path]["archives"]

        else:
            for i, path_part in enumerate(path):
                search_dir = self.directores
                if i == len(path) - 2:

                    if not name_exists(search_dir[path_part]["archives"], element_info):
                        search_dir[path_part]["archives"][path[-1]] = element_info
                        self.inode_map[path_to_element] = path[-1]

                    else:
                        raise Warning("Name already exists file or director not created!")
                    break

    def show_allocation(self):
        your_json = json.dumps(self.directores)

        parsed = json.loads(your_json)
        print(json.dumps(parsed, indent=4, sort_keys=True))

    def show_status(self):
        consumed_capacity = len(self.memory) * Block.CAPACITY
        print(f"Consumed capacity: {consumed_capacity / self.TOTAL_CAPACITY}%")
        print(f"Number of blocks allocated: {len(self.memory)}")


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, required=True, help="The path to the file or folder.")
parser.add_argument('--name', type=str, required=True, help="The name of the file or folder.")

parser.add_argument('--add_file', action="store_true")
parser.add_argument('--add_folder', type=str)

parser.add_argument('--size', type=int, help="The size of"
                                             "the file is required"
                                             "when you want to allocate a file ")
args = parser.parse_args()


def demo():
    file_sys = FileSystem()
    # file_sys.show_allocation()
    file_sys.allocate("usr/sys/myfile.txt", {"name": "myfile.txt", "size": 10})
    file_sys.allocate("usr/sys/myfile1.txt", {"name": "myfile1.txt", "size": 25})
    # file_sys.show_allocation()
    file_sys.allocate("usr/myfile", {"name": "myfile", "size": 10, "archives": {}}, is_dir=True)
    file_sys.show_allocation()
    file_sys.show_status()


def main():
    file_sys = FileSystem()
    # file_sys.show_allocation()

    if args.add_file:
        file_sys.allocate(args.path, {"name": args.name, "size": args.size})

    if args.add_folder:
        file_sys.allocate(args.path, {"name": args.name, "size": 10, "archives": {}}, is_dir=True)

    file_sys.show_allocation()
    file_sys.show_status()


if __name__ == '__main__':
    main()
