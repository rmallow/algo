import multiprocessing as mp

if __name__ == '__main__':
    mp.freeze_support()
    from algo.start import start

    # mp.set_start_method("spawn")
    start()
