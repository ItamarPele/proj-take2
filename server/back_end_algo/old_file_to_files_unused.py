"""


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


def data_to_files(data, n, k, name, files_directory):
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



    def data_points_to_data(list_of_data_points):
    list_of_points = []
    num_of_orig_comps = 0
    for data_point in list_of_data_points:
        dp = str(data_point).split(",")
        print("dpp")
        print(dp)
        x, y, num_of_orig_comps, len_of_file = int(dp[0]), int(dp[1]), int(dp[2]), int(dp[3])
        chunk_size = read_and_split_file.CalcChunkSize(num_of_orig_comps, len_of_file)
        read_and_split_file.SetChunkSize(chunk_size)
        largest_number_possible = int(power_of_two(read_and_split_file.GetChunkSize() * 8) - 1)
        m = int(nextprime(largest_number_possible))
        MD.modulus = m
        list_of_points.append(Data(x, y))
    print("LIST OF POINTS")
    print(list_of_points)
    d = points_to_data(num_of_orig_comps, list_of_points)
    return d


    def data_to_data_points(data, n, k):
    is_data_ok, error_message = CheckData(data, n, k, )


    print(n)
    if not is_data_ok:
        print(error_message)
        return None
    P = data_to_points(n, k, data)
    info_list = []
    for i in range(len(P)):
        info = str((P[i]).x) + "," + str((P[i]).y) + "," + str(n) + "," + str(len(data))
        info_list.append(info)
    return info_list
"""