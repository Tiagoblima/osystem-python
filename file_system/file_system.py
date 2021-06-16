import os
import json
import uuid


def name_exists(dir_, element_info):
    for element in dir_:
        print(element)
        if dir_[element]["name"] == element_info["name"]:
            return True
    return False


class FileSystem:
    TOTAL_CAPACITY = 100
    ROOT_DIR = 'usr'

    def __init__(self):
        self.memory = []
        inode = str(uuid.uuid1())
        self.inode_map = {
            "usr/system.txt": inode
        }
        self.directores = {

            self.ROOT_DIR: {
                "nome": self.ROOT_DIR, "size": 20,
                "archives":
                    {
                        inode: {
                            "size": 10,
                            "name": "system.txt"
                        },
                        "sys":
                            {
                                "size": 10,
                                "name": "sys",
                                "archives": {}
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
                        search_dir[path_part]["archives"][inode] = element_info
                        self.inode_map[path_to_element] = inode

                    else:
                        raise Warning("Name already exists file or director not created!")
                    break
                else:

                    search_dir = search_dir[path_part]["archives"]
            search_dir = self.directores
            for part_path in path[:-1]:
                search_dir[part_path]["size"] += element_info["size"]
                search_dir = search_dir[part_path]["archives"]
    def show_allocation(self):
        your_json = json.dumps(self.directores)

        parsed = json.loads(your_json)
        print(json.dumps(parsed, indent=4, sort_keys=True))


def main():
    file_sys = FileSystem()
    file_sys.show_allocation()
    file_sys.allocate("usr/myfile.txt", {"name": "myfile.txt", "size": 10})
    # file_sys.show_allocation()
    file_sys.allocate("usr/sys/myfile.txt", {"name": "myfile.txt", "size": 10})
    file_sys.show_allocation()
    # file_sys.allocate("usr/myfile.txt", {"name": "myfile.txt", "size": 10})
    # file_sys.show_allocation()


if __name__ == '__main__':
    main()
