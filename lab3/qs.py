import random
from multiprocessing import Pool, current_process

# import time

array = [i for i in range(100)]
random.shuffle(array)


def partition(A, start, end):
    pivot = A[end]
    i = start - 1

    for j in range(start, end):
        if A[j] <= pivot:
            i = i + 1
            A[j], A[i] = A[i], A[j]

    A[i + 1], A[end] = A[end], A[i + 1]
    return i + 1


def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    p = Pool(2, initializer=init_process)
    pivot = partition(arr, 0, len(arr) - 1)

    ar = p.map(quick_sort, [arr[:pivot], arr[pivot:]])
    return ar[0] + ar[1]


def init_process():
    current_process().daemon = False


print(quick_sort(array))
