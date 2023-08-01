import copy
import random

from scipy.optimize import linprog

def Linear_Program():
    obj = [-1, -2]
    lhs_ineq = [[2, 1], [-4, 5], [1, -2]]  # Yellow constraint left side
    rhs_ineq = [20, 10, 2]  # Yellow constraint right side
    rhs_eq = [15]  # Green constraint right side
    lhs_eq = [[-1, 5]]  # Green constraint left side
    bnd = [(0, float("inf")), (0, float("inf"))]  # Bounds of y

    opt = linprog(c=obj, A_ub=lhs_ineq, b_ub=rhs_ineq, A_eq=lhs_eq, b_eq=rhs_eq, bounds=bnd, method="revised simplex")
    print(opt)

class test:
    def __int__(self, num):
        self.num = num

    def abc(self):
        pass
class A:
    name = ''
    def demo(self, num):
        print(self) #代表当前实例化类的对象
        print(id(self))
class Card:
    def __init__(self,rank,suit):
        self.suit = suit
        self.rank = rank
        # self.hard, self.soft = self._points()

if __name__ == '__main__':

    arr = [1, 1, 1, 2, 2, 3, 3, 3]
    arr_b = [1, 2, 3, 4, 5, 6, 7, 8]

    result = []
    result_b = []
    result_c = []
    current_subarray = [arr[0]]
    current_subarray_b = [arr_b[0]]
    for i in range(1, len(arr)):
        if arr[i] == arr[i - 1]:
            current_subarray.append(arr[i])
            current_subarray_b.append(arr_b[i])
        else:
            result.append(current_subarray)
            result_b.append(current_subarray_b)
            current_subarray = [arr[i]]
            current_subarray_b = [arr_b[i]]

    # Append the last subarray
    result.append(current_subarray)
    result_b.append(current_subarray_b)

    for i in range(len(result_b)-1):
        item = []
        item = result_b[i]
        item.append(result_b[i+1][0])
        result_c.append(item)

    last_result_b = result_b[-1]
    result_c.append(result_b[-1])


    print(result, result_b, result_c)
    print([1, 2][-2])

    a = [1, 2, 3, 4, 5, 6, 7, 8]
    # temp = copy.deepcopy(a[4:])
    # temp.extend(a[:4])
    # a = temp
    print(a[1:])
    # print(a[len(a)-1])
    b1 = Card(1, 2)
    b2 = Card(1, 2)
    a = [b1, b1, b2]
    print(a)
    a.remove(b1)
    a.remove(b1)
    print(a)

