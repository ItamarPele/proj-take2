from lagrange_interlopation import *
import read_and_split_file
from sympy import nextprime
from modulo_int import MD
import os
#s
READ_FILE_PATH = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\R.txt"
WRITE_FILE_PATH = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\W.txt"


def power_of_two(b):
    result = 1
    for _ in range(b):
        result *= 2

    return result


def data_to_points(original_comps, new_comps, data):
    chunk_size = read_and_split_file.CalcChunkSize(original_comps, len(data))
    read_and_split_file.SetChunkSize(chunk_size)

    int_list = read_and_split_file.DataToIntList(data)

    largest_number_possible = int(power_of_two(read_and_split_file.GetChunkSize() * 8) - 1)
    m = int(nextprime(largest_number_possible))

    MD.modulus = m

    indexed_bytes = list(enumerate(int_list))

    p_list = []
    for p in indexed_bytes:
        p_list.append(Data(p[0], p[1]))

    new_points_list = []
    # here I want to add a thread Optimization
    for i in range(original_comps + new_comps):
        new_points_list.append(Data(i, interpolate(p_list, MD(i), MD(len(p_list))).value))

    return new_points_list


def points_to_data(original_comps, point_list):
    if len(point_list) < original_comps:
        raise Exception("not enough data")

    list_of_data = []
    # here I want to add a thread Optimization
    for i in range(original_comps):
        list_of_data.append((i, interpolate(point_list, MD(i), MD(original_comps)).value))

    original_numbers = []
    for a in list_of_data:
        original_numbers.append(a[1])

    new_data = read_and_split_file.IntListToData(original_numbers)
    return new_data


if __name__ == "__main__":
    import time

    start_time = time.time()

    for j in range(1):
        NUM_OF_ORIGINAL_COMPUTERS = 40
        NUM_OF_NEW_COMPS = 80

        data_from_file = read_and_split_file.GetDataFromFile(READ_FILE_PATH)
        P = data_to_points(NUM_OF_ORIGINAL_COMPUTERS, NUM_OF_NEW_COMPS, data_from_file)

        print(len(P))
        print(P)

        renewed_data = points_to_data(NUM_OF_ORIGINAL_COMPUTERS, P)
        with open(WRITE_FILE_PATH, 'wb') as write_file:
            write_file.write(renewed_data)
        # print(renewed_data)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("elapsed_time")
    print(elapsed_time)
