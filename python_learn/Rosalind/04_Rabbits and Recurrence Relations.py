"""
Author: zhangyifan1
Date: 2024-06-07 15:43:08
LastEditors: zhangyifan1 zhangyifan1@genomics.cn
LastEditTime: 2024-06-07 19:57:02
FilePath: //Rosalind//04_Rabbits and Recurrence Relations.py
Description: 

"""


# k=1时
# k=1时就是经典的斐波那契数列，1,1,2,3,5,8...依次类推，我们现根据这个找到规律，在此基础上往后延伸
# 从n=3开始，就会和前两项相关，所以我们当前项的计算中一定会涉及之前项的计算
# 递归
def fibonacci_digui(month):
    if month == 1 or month == 2:
        return 1
    else:
        return fibonacci_digui(month - 1) + fibonacci_digui(month - 2)


# 迭代
def fibonacci_diedai(month):
    a, b = 0, 1
    for _ in range(month - 1):
        a, b = b, a + b
    return b


def rabbit_born_digui(month, produce):
    if month == 1 or month == 2:
        return 1
    else:
        return (rabbit_born_digui(month - 1, produce)) + (
            rabbit_born_digui(month - 2, produce) * produce
        )


def rabbit_born_diedai(month, produce):
    a, b = 0, 1
    for _ in range(month - 1):
        a, b = b * produce, a + b
    return b


def main():
    month = 1
    produce = 4
    num = fibonacci_digui(month)
    print(num)
    num = fibonacci_diedai(month)
    print(num)
    num = rabbit_born_digui(month, produce)
    print(num)
    num = rabbit_born_diedai(month, produce)
    print(num)


if __name__ == "__main__":
    main()
