import random

UT = 1  # unit time (S)

MIN_BLOCK = 0
MAX_BLOCK = 1000


class System:

    def __init__(self):
        self.disk = list(range(MIN_BLOCK, MAX_BLOCK))  # blocos

    def seek_blocks(self, block_list):
        first = block_list[0]

        ordered = [(i, abs(first - block)) for i, block in enumerate(block_list)]
        ordered = sorted(ordered, key=lambda tup: tup[1])

        seek_time_list = []
        for i, _ in ordered:
            block = block_list[i]
            req_time = random.randrange(UT, 5)
            print(f"BLOCK: {block} Request Time: ", req_time)
            seek_time_list.append(req_time)
            self.disk.index(block)

        print("Access order (index, block_id): ", ordered)
        print(f"Total time spend: {UT * sum(seek_time_list)}s")


def demo():
    sys_io = System()

    block_seq = [random.randrange(MIN_BLOCK, MAX_BLOCK) for i in range(10)]
    sys_io.seek_blocks(block_seq)


demo()
