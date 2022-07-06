# -*- coding = utf-8 -*-
# @Time : 2022/7/1 下午 1:58
# @Author : 何智
# @File : Fourier.py
# @Software : PyCharm

from fun_readsmp import fun_readsmp


def createArray(time, eqp) -> list:  # time:格式 2022-04-29_17-06-22 eqp:检测设备数量
    Array = []
    data = []
    for j in range(eqp):

        # data = []
        if j + 1 < 10:
            data.append(fun_readsmp(rf".\异常波形\{time}\BMS_0{j + 1}_{time}.smp"))
        else:
            data.append(fun_readsmp(rf".\异常波形\{time}\BMS_{j + 1}_{time}.smp"))

    for j in range(eqp):
        Array.append([[i + 1, data[j][i]] for i in range(len(data[j]))])

    return Array


def createlist(time, eqp):  # time:格式 2022-04-29_17-06-22 eqp:检测设备数量

    data = []
    for j in range(eqp):

        # data = []
        if j + 1 < 10:
            data.append(fun_readsmp(rf".\异常波形\{time}\BMS_0{j + 1}_{time}.smp"))
        else:
            data.append(fun_readsmp(rf".\异常波形\{time}\BMS_{j + 1}_{time}.smp"))

    return data


def correlation_by_np(lst):
    res = {}
    val = []
    import numpy as np
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            # a = np.array(Array[j])
            # b = np.array(Array[i])
            a = np.array(lst[i])
            b = np.array(lst[j])
            val = np.corrcoef(a, b)
            # print(val)
            res[f'{i + 1}, {j + 1} ='] = val[0][1]

    return res


# res1 = createlist("2022-04-29_17-06-22", 16)
# print(res1[0])

# print(correlation_by_np(res1))
