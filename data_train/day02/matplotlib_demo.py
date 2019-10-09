import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

#  修改默认字体，否则会有中文乱码问题
mpl.rcParams['font.sans-serif'] = ['SimHei']

print('-' * 20, '年份与GDP的折线图', '-' * 20)
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010]
gdp = [300.2, 543.3, 1075.9, 2862.5, 5979.6, 10289.7, 14958.3]
# 颜色、线条样式、宽度、标记
plt.plot(years, gdp, color='#00FF00', linestyle='--', linewidth=1, marker='D')
plt.show()

print('-' * 20, '柱状图相关演示', '-' * 20)
data = [23, 85, 72, 43, 52]
plt.bar(range(len(data)), data, color='#ff0000', alpha=0.7)
for a, b in zip(range(len(data)), data):
    plt.text(a, b, b, ha='center', va='bottom', fontsize=12)
# grid函数用于绘制网格
plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y', alpha=0.6)
plt.show()

print('-' * 20, '层叠柱状图', '-' * 20)
data1 = [23, 85, 72, 43, 52]
data2 = [42, 35, 21, 16, 9]
plt.bar(range(len(data1)), data1)
# bar函数的bottom指定底部的起始值
plt.bar(range(len(data2)), data2, bottom=data1)
plt.show()

print('-' * 20, '水平柱状图', '-' * 20)
data = [23, 85, 72, 43, 52]
plt.barh(range(len(data)), data)
plt.show()

print('-' * 20, '刻度与标签', '-' * 20)
data = [23, 85, 72, 43, 52]
labels = ['A', 'B', 'C', 'D', 'E']
# 设置刻度和标签
plt.xticks(range(len(data)), labels)
# xlabel和ylabel给x轴与y轴添加标签
plt.xlabel('Class')
plt.ylabel('Amounts')
# 通过title方法为图表添加标题
plt.title('Example')
plt.bar(range(len(data)), data)
plt.show()

print('-' * 20, '散点图', '-' * 20)
x = np.random.randn(100)
y = np.random.randn(100)
plt.scatter(x, y)
plt.show()

print('-' * 20, '散点图与保存图片', '-' * 20)
data = {
    '南京': (60, '#7199cf'),
    '上海': (45, '#4fc4aa'),
    '北京': (120, '#ffff10'),
}
# 设置绘图对象的大小
cities = data.keys()
values = [x[0] for x in data.values()]
colors = [x[1] for x in data.values()]
# 填充数据,生成的图表保存到本地中
plt.pie(x=values, labels=data.keys(), colors=colors,autopct='%4.2f%%')
plt.savefig('./pie.jpg')
plt.show()
