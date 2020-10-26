import fileinput
from tqdm import tqdm
from collections import Counter
from multiprocessing import Pool


def mapper(row):
    pass


def reducer(data):
    pass


if __name__ == "__main__":

    # Create multiprocessing pool
    pool = Pool()

    # Map
    print("Map Stage...")
    with open("web1t.baby") as f:
        baby1t = f.read().splitlines()
    skipgram_count = [row for row in pool.map(mapper, baby1t) if row]
    skipgram_count.sort(key=lambda x: x[0])
    # skipgram_count:
    # [
    #   ... ,
    #   (('of the', 1), 12345678),
    #   (('of the', 1), 123),
    #   (('at the', 2), 456),
    #   ...
    # ]

    # Reduce
    print("Reduce Stage...")
    reducer(skipgram_count)
