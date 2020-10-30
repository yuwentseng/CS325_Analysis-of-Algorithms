from timeit import timeit
from random import randint
from align import *

lengths = [500, 1000, 2000, 4000, 5000]
alphabet = ['A', 'G', 'T', 'C']


def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped


def build_sequence_pairs(length_x, length_y, num_pairs=10):
    pairs = []
    for rep in range(0, num_pairs):
        sequence1 = ""
        sequence2 = ""

        for x in range(0, length_x):
            sequence1 += alphabet[randint(0, len(alphabet) - 1)]
        for y in range(0, length_y):
            sequence2 += alphabet[randint(0, len(alphabet) - 1)]

        pairs.append(sequence1 + ',' + sequence2 + '\n')

    return pairs


def align_sequence(d_cost, sequence):
    A, B = sequence.split(',')
    B = B[:-1]  # B will have a trailing newline, which needs to be removed

    # Generate the edit distance array and use that to build our aligned strings
    a_edit_dist, backtrace = edit_distance(d_cost, A, B)

    align(A, B, backtrace)


if __name__ == "__main__":
    f_cost = open("imp2cost.txt", 'r')
    d_cost = file_2_dict(f_cost)

    for length_x in lengths:
        for length_y in lengths:
            time = 0
            for pair in build_sequence_pairs(length_x, length_y):
                wrapped = wrapper(align_sequence, d_cost, pair)
                time += timeit(wrapped, number=1)

            print "Averaged", time/10, "seconds for " + str(length_x) + "x" + str(length_y)