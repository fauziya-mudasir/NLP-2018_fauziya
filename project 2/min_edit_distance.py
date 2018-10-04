import sys
import numpy as np


def delCost(source):
    return 1


def subCost(source, target):
    if source == target:
        return 0
    else:
        return 2


def insCost(target):
    return 1


def minEdit(source, target):
    n = len(source)
    m = len(target)
    matrix = np.zeros(shape=[n + 1, m + 1])

    for i in range(1, n + 1):
        matrix[i, 0] = matrix[i - 1, 0] + delCost(source[i - 1])
    for j in range(1, m + 1):
        matrix[0, j] = matrix[0, j - 1] + insCost(target[j - 1])

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            matrix[i, j] = min(matrix[i - 1, j] + delCost(source[i - 1]),
                               matrix[i - 1, j - 1] + subCost(source[i - 1], target[j - 1]),
                               matrix[i, j - 1] + insCost(target[j - 1]))
    print("the matrix is :\n\n{}\n".format(matrix))

    return matrix[n, m]


result = sys.argv
output = minEdit(str(result[1]), str(result[2]))
print("The cost of editing between {} and {} is {}.".format(str(result[1]), str(result[2]), output))
