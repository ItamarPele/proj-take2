import os
import math

ChunkSize = 0  # 2 bytes


def CalcChunkSize(num_of_comps, len_of_data):
    num_of_comps -= 2
    return math.floor(len_of_data / num_of_comps)


def SetChunkSize(newChunkSize):
    global ChunkSize
    ChunkSize = newChunkSize


def GetChunkSize():
    return ChunkSize


def GetDataFromFile(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def WriteBinaryToFile(file_path, data):
    with open(file_path, 'wb') as file:
        return file.write(data)



def binary_list_to_ints(binary_list):
    return [int.from_bytes(chunk, byteorder='big') for chunk in binary_list]


def ints_to_binary_list(int_list):
    return [int_list[i].to_bytes((int_list[i].bit_length() + 7) // 8, byteorder='big') for i in range(len(int_list))]



def DataToIntList(data):
    global ChunkSize

    num_of_bytes = len(data)

    num_of_last_bytes = num_of_bytes % ChunkSize


    additional_bytes_to_add = ChunkSize - num_of_last_bytes


    endf = (0).to_bytes(additional_bytes_to_add, 'little', signed=False)
    header = additional_bytes_to_add.to_bytes(ChunkSize, 'little', signed=False)
    data = header + data + endf
    assert len(data) % ChunkSize == 0

    int_ls = []
    for i in range(len(data) // ChunkSize):
        byte_chunk = data[i * ChunkSize:(i + 1) * ChunkSize]
        int_ls += [int.from_bytes(byte_chunk, 'little', signed=False)]
    return int_ls


def IntListToData(int_ls):
    global ChunkSize
    additional_bytes = int_ls[0]
    data = bytes()
    for i in range(1, len(int_ls)):
        b = int_ls[i]
        b = b.to_bytes(ChunkSize, 'little', signed=False)
        data += b
    data = data[:(len(data) - additional_bytes)]
    return data


