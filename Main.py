from lagrange_interlopation import *
import read_and_split_file
from sympy import nextprime
from modulo_int import MD

READ_FILE_PATH = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\R.txt"
WRITE_FILE_PATH = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\W.txt"


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
    DATA_UPPER_LIMIT = 10000  # 10 kb
    RATIO_BETWEEN_DATA_AND_N = 200

    if n > 3:
        return False, "n must be larger than 3"
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

def Data_to_files(data, n, k, name):
    import time
    start_time = time.time()
    P = data_to_points(n, k, data)
    path = r"C:\Users\itama\PycharmProjects\ProjREALNOWPLEASWORK\FILES"
    for i in P:
        info = str(P[i][0]) + "," + str(P[i][1])
        name_of_file = path + f"\\name-{i}-{n}"
        with open()


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
