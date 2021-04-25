import multiprocessing as mp
import sys
from algo.start import start

if __name__ == '__main__':
    mp.freeze_support()
    # mp.set_start_method("spawn")
    start(sys.argv)
