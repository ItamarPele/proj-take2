from lagrange_interlopation import *
import read_and_split_file
from sympy import nextprime
from modulo_int import MD
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
    DATA_UPPER_LIMIT = 10000  # 10 kb
    RATIO_BETWEEN_DATA_AND_N = 200

    if n < 3:
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
    print(point_list)

    list_of_data = []
    for i in range(original_comps):
        list_of_data.append((i, interpolate(point_list, MD(i), MD(original_comps)).value))

    original_numbers = []
    for a in list_of_data:
        original_numbers.append(a[1])

    new_data = read_and_split_file.IntListToData(original_numbers)
    return new_data


def data_to_files(data, n, k, name,files_directory):
    is_data_ok, error_message = CheckData(data, n, k, )
    print(n)
    if not is_data_ok:
        print(error_message)
        return None
    P = data_to_points(n, k, data)
    path = files_directory
    for i in range(len(P)):
        info = str((P[i]).x) + "," + str((P[i]).y) + "," + str(n) + "," + str(len(data))
        name_of_file = path + f"\\{name}-{i}"
        with open(name_of_file, "w") as file:
            file.write(info)


def files_to_data(files_directory):
    list_of_points = []
    for name in os.listdir(files_directory):
        with open(os.path.join(files_directory, name), 'r') as file:
            nums = file.read().split(',')
            x, y, num_of_orig_comps, len_of_file = int(nums[0]), int(nums[1]), int(nums[2]), int(nums[3])
            chunk_size = read_and_split_file.CalcChunkSize(num_of_orig_comps, len_of_file)
            read_and_split_file.SetChunkSize(chunk_size)

            largest_number_possible = int(power_of_two(read_and_split_file.GetChunkSize() * 8) - 1)
            m = int(nextprime(largest_number_possible))

            MD.modulus = m

            list_of_points.append(Data(x, y))
    d = points_to_data(num_of_orig_comps, list_of_points)
    return d

if __name__ == "__main__":
    print("main")

# renewed_data = points_to_data(NUM_OF_ORIGINAL_COMPUTERS, P)
# with open(WRITE_FILE_PATH, 'wb') as write_file:
#    write_file.write(renewed_data)
# print(renewed_data)
