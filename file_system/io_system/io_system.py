import argparse
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
        block_access = []
        seek_time_list = []
        for i, _ in ordered:
            block = block_list[i]

            if i != 0:
                last_block = block_list[i - 1]
                req_time = abs(block - last_block) * UT
            else:
                req_time = UT

            print(f"BLOCK: {block} Request Time: {req_time}s")
            seek_time_list.append(req_time)
            self.disk.index(block)
            block_access.append(block)
        print("Access sequence (sequência de acesso): ", block_access)
        print(f"Total time spend: {UT * sum(seek_time_list)}s")


def demo():
    sys_io = System()

    block_seq = [random.randrange(MIN_BLOCK, MAX_BLOCK) for i in range(10)]
    sys_io.seek_blocks(block_seq)


# demo()
#parser = argparse.ArgumentParser()
#parser.add_argument('--blocks', metavar='N', type=int, nargs='+',
                  #  help='an integer for the accumulator')
#args = parser.parse_args()


#def main():
  #  sys_io = System()
  #  sys_io.seek_blocks(args.blocks)


#if __name__ == '__main__':
   # main()
