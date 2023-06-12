import math
import multiprocessing as mp
import random
from multiprocessing import Pool
import time


def merge(arr):
    arr1, arr2 = arr[0], arr[1]
    new_arr = []
    arr1_counter = 0
    arr2_counter = 0
    while arr1_counter != len(arr1) and arr2_counter != len(arr2):
        if arr1[arr1_counter] <= arr2[arr2_counter]:
            new_arr.append(arr1[arr1_counter])
            arr1_counter += 1
        else:
            new_arr.append(arr2[arr2_counter])
            arr2_counter += 1
    while arr1_counter != len(arr1):
        new_arr.append(arr1[arr1_counter])
        arr1_counter += 1
    while arr2_counter != len(arr2):
        new_arr.append(arr2[arr2_counter])
        arr2_counter += 1
    return new_arr


def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]
        merge_sort(L)
        merge_sort(R)
        i = j = k = 0
        while i < len(L) and j < len(R):
            if L[i] <= R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr


def divide(arr, cpu_no):
    new_arr = []
    chunk = math.ceil(len(arr) / cpu_no)
    for c in range(cpu_no):
        if c == cpu_no - 1:
            new_arr.append(arr[c * chunk:])
        else:
            new_arr.append(arr[c * chunk:(c + 1) * chunk])
    return new_arr


def join_sub_arrays(arr):
    new_arr = []
    arr_counter = 0
    while arr_counter < len(arr) - 1:
        new_arr.append([arr[arr_counter], arr[arr_counter + 1]])
        arr_counter += 2
    if arr_counter < len(arr):
        new_arr.append([arr[arr_counter], []])
    return new_arr


def print_array(arr):
    if isinstance(arr[0], int):
        print(arr)
    else:
        for i in arr:
            print(i)


def check(arr):
    print(arr == sorted(arr))


N = 1_000_000

if __name__ == '__main__':
    time_tmp = time.time()

    cpu_no = mp.cpu_count()
    print("Number of processors: ", cpu_no)

    array = [i for i in range(N)]
    random.shuffle(array)

    # print("Given array is", end="\n")
    # print_array(array)

    array = divide(array, cpu_no)

    # print("Divided array is", end="\n")
    # print_array(array)

    p = Pool(cpu_no)
    array = p.map(merge_sort, array)
    p.close()
    p.join()

    # print("Sorted divided array is:", end="\n")
    # print_array(array)

    for i in range(int(math.log2(cpu_no))):
        array = join_sub_arrays(array)
        p = Pool(cpu_no)
        array = p.map(merge, array)
        p.close()
        p.join()

        # print(f"Sorted merged {i + 1} time array is:", end="\n")
        # print_array(array)

    # print("Sorting done, now checking: ", end="")
    # check(array)
    print(time.time() - time_tmp)

    time_tmp = time.time()
    array = [i for i in range(N)]
    random.shuffle(array)
    merge_sort(array)
    print(time.time() - time_tmp)
