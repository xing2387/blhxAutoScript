# -*- coding: utf-8 -*-

from __future__ import print_function
# 调用模块
# 调用数组模块
import numpy as np
# 实现插值的模块
from scipy import interpolate
# 画图的模块
import matplotlib.pyplot as plt
# 生成随机数的模块
import random

# random.randint(0, 10) 生成0-10范围内的一个整型数
# y是一个数组里面有10个随机数，表示y轴的值
y = np.array([random.randint(0, 20) for _ in range(20)])
# x是一个数组，表示x轴的值
x = np.array([num for num in range(20)])

# 插值法之后的x轴值，表示从0到10间距为0.5的20个数
xnew = np.arange(0, max(x), 0.1)

print(xnew)
print(x)
print(y)
"""
kind方法：
nearest、zero、slinear、quadratic、cubic
实现函数func
"""
func = interpolate.interp1d(x, y, kind='cubic')
# 利用xnew和func函数生成ynew，xnew的数量等于ynew数量
ynew = func(xnew)

ynew = np.around(ynew,decimals=3)
print(ynew)

x = [207.0, 327.0, 386.93, 387]
y = [1038.0, 949.0, 925.55, 925.55]
xnew = np.arange(min(x), max(x), 0.1)
func = interpolate.interp1d(x, y, kind='cubic')
ynew = func(xnew)

# ynew = np.around(ynew,decimals=3)
# 画图部分
# 原图
plt.plot(x, y, 'ro-')
# 拟合之后的平滑曲线图
plt.plot(xnew, ynew)
plt.show()