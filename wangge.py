# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from pylab import mpl

xmajorLocator = MultipleLocator(24 * 3)  # 将x轴主刻度标签设置为24 * 3的倍数
ymajorLocator = MultipleLocator(100 * 2)  # 将y轴主刻度标签设置为100 * 2的倍数

# 设置中文字体
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 导入文件数据
data = np.loadtxt('H:/dataset/爸爸去哪儿/统计数据_每小时_ba.csv', delimiter=',', dtype=int)

# 截取数组数据
x = data[:, 0]
y = data[:, 1]

plt.figure(num=1, figsize=(8, 6))

ax = plt.subplot(111)
ax.xaxis.set_major_locator(xmajorLocator)
ax.yaxis.set_major_locator(ymajorLocator)
ax.xaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度
ax.yaxis.grid(True, which='major')  # x坐标轴的网格使用主刻度

plt.xlabel('时间索引')
plt.ylabel('活动频数')
plt.title('折线图')
plt.xlim(0, 1152)
plt.ylim(0, 2200)
# plt.plot(x, y, 'rs-')
line1 = ax.plot(x, y, 'b.-')
ax.legend(line1, ('微博'))
plt.show()