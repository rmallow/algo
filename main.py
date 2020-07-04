from algo.start import start
import multiprocessing as mp

def main():

    start()
    


if __name__ == '__main__':
    mp.set_start_method("spawn")
    main()