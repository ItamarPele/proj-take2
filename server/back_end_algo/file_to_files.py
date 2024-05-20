from sympy import nextprime
from server.back_end_algo.lagrange_interlopation import *
from server.back_end_algo.lagrange_interlopation import MD
from server.back_end_algo import read_and_split_file
import os


def power_of_two(b):
    result = 1
    for _ in range(b):
        result *= 2

    return result


def CheckData(data, n, k):
    """
    .
    :param data: data read from file
    :param n: splits to file
    :param k: additional parts to add to file parts
    :return: are all params ok, string message of error
    """
    N_UPPER_LIMIT = 40
    K_UPPER_LIMIT = N_UPPER_LIMIT * 2
    DATA_UPPER_LIMIT = 20000  # 10 kb
    RATIO_BETWEEN_DATA_AND_N = 300

    if n < 3:
        return False, "n must be larger or equal to 3"
    if len(data) < n:
        return False, "data must be larger or equal to n"
    if k < 0:
        return False, "k must be larger than 0"
    if k > K_UPPER_LIMIT:
        return False, f"k must be smaller or equal to {K_UPPER_LIMIT}"
    if n > N_UPPER_LIMIT:
        return False, f"k must be smaller or equal to {N_UPPER_LIMIT}"
    if len(data) > DATA_UPPER_LIMIT:
        return False, f"data must be smaller or equal to {DATA_UPPER_LIMIT} bytes"
    if len(data) // RATIO_BETWEEN_DATA_AND_N > n:
        return False, f"len of data / {RATIO_BETWEEN_DATA_AND_N} must be larger than n"
    return True, "OK"


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


def points_to_data(n, point_list_str, len_of_file):
    chunk_size = read_and_split_file.CalcChunkSize(n, len_of_file)
    read_and_split_file.SetChunkSize(chunk_size)

    largest_number_possible = int(power_of_two(read_and_split_file.GetChunkSize() * 8) - 1)
    m = int(nextprime(largest_number_possible))
    MD.modulus = m

    if len(point_list_str) < n:
        raise Exception("not enough data")
    print(point_list_str)

    point_list = []
    for str_point in point_list_str:
        point = Data.from_repr(str_point)
        point_list.append(point)
    print(point_list)

    list_of_data = []
    for i in range(n):
        list_of_data.append((i, interpolate(point_list, MD(i), MD(n)).value))

    original_numbers = []
    for a in list_of_data:
        original_numbers.append(a[1])

    new_data = read_and_split_file.IntListToData(original_numbers)
    return new_data
