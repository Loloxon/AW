import math
from multiprocessing import Pool


# 1) wyznaczamy indeksy na których zmienia się monotoniczność
# 2) ciąg dzielimy na osobne podciągi monotoniczne
# 3) co drugi ciąg monotoniczny obracamy współbieżnie (każdy równocześnie)
# 4) powstałą tablicę ciągów rosnących łączymy współbieżnie "po dwa" (1 z 2, 3 z 4 itp.) - współbieżnie
# 5) powtarzamy log(n) razy uzyskując w pełni posortowaną tablicę

# algorym sortuje rosnącu lub malejąco, zależnie od kolejności monotoniczności w początkowej
# tablicy jako że w treści nie było sprecyzowane jak ma sortować


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


def revert(arr):
    new_arr = []
    for i in range(len(arr) - 1, -1, -1):
        new_arr.append(arr[i])
    return new_arr


def divide(arr):
    divided_T = []
    for i in range(0, len(arr) - 1, 2):
        divided_T.append([arr[i], arr[i + 1]])
    if len(arr) % 2 == 1:
        divided_T.append([arr[-1], []])
    return divided_T


def sort(T, k):
    p = Pool(k)
    changed_mono_idx = [0]
    for i in range(1, len(T) - 1):
        if T[i - 1] < T[i] and T[i] > T[i + 1] or T[i - 1] > T[i] and T[i] < T[i + 1]:
            changed_mono_idx.append(i)

    mono_T = []
    for i in range(k - 1):
        mono_T.append(T[changed_mono_idx[i]:changed_mono_idx[i + 1]])
    mono_T.append(T[changed_mono_idx[-1]:])

    to_revert = []
    for i in range(0, len(mono_T) - 1, 2):
        to_revert.append(mono_T[i + 1])
    to_revert = p.map(revert, to_revert)

    for i in range(len(to_revert) - 1):
        mono_T[i * 2 + 1] = to_revert[i]

    for i in range(math.ceil(math.log2(k))):
        divided_t = divide(mono_T)
        mono_T = p.map(merge, divided_t)
    return mono_T[0]


T = [10, 20, 30, 11, 8, 7, 12, 13, 5, 9, 44, 55]
k = 5

print(sort(T, k))
