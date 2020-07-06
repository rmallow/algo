from algo.start import start
from algo.test import test
import multiprocessing as mp

def main():

    start()
    


if __name__ == '__main__':
    mp.set_start_method("spawn")
    main()