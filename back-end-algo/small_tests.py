import threading

def longmath(number):
    #(long math function that takes time)
    #this is not the actual function just the explanation
    return number

lst = [1, 5, 8, 77, -82, 0, 824]
lst2 = []

# Define a function to process elements of lst in parallel
def process_element(index):
    result = longmath(lst[index])
    lst2[index] = result

# Create a list to store thread objects
threads = []

# Create threads for each element in lst
for i in range(len(lst)):
    lst2.append(None)  # Add a placeholder for the result
    thread = threading.Thread(target=process_element, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to finish
for thread in threads:
    thread.join()

print(lst2)


