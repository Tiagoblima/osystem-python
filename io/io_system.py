import random

UT = 1  # unit time (S)

MIN_BLOCK = 0
MAX_BLOCK = 1000


class IO:

    def __init__(self):
        self.disk = list(range(MIN_BLOCK, MAX_BLOCK))  # blocos

    def seek_blocks(self, block_list):
        block_list = sorted(block_list)
        for block in block_list:
            self.disk.index(block)

        print("Access order: ", block_list)
        print("Total time spend: ", UT * len(block_list))
