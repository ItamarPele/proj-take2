# this is the testing file for the algorithm:
from os import urandom
# generates a random bytearray
from random import randint
from file_to_files import data_to_points, points_to_data
if __name__ == "__main__":
    for i in range(2000):
        print(i)
        len_of_data = randint(100, 1000)
        data = urandom(len_of_data)
        n = randint(3, 7)
        k = randint(1, 5)
        data_points = (data_to_points(n, k, data))
        str_data_points = [str(data_point) for data_point in data_points]
        # turn to str so later can be written into file
        for j in range(k):
            str_data_points.pop()
            # remove some parts and still the data will remain
        new_data = points_to_data(n, str_data_points, len_of_data)
        assert new_data == data
    print("all good!!! (: ")
