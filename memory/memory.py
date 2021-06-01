class Memory:

    def __init__(self, name="Memory", memory_size=1000):
        self.name = name
        self.memory_size = memory_size

    # TO Override
    def allocate(self, process_):
        print()
        print('-' * 20, end='')
        print("STARTING ALLOCATION", end='')
        print('-' * 20)
        print(f'Inserindo o processo {process_.name} na Memória')

        print()
        print('-' * 20, end='')
        print("END ALLOCATION", end='')
        print('-' * 20)

    def reset(self):
        pass

    def memory_status(self):
       pass

    def size(self):
        return self.memory_size
