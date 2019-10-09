# -*- coding: utf-8 -*-
# File  : data1.py
# Author: water
# Date  : 2019/7/31

import numpy as np
from PIL import Image

#图片转换成矩阵
image = Image.open("./mj.jpeg")
image_np = np.array(image)

print(image_np)
print(image_np.shape)

image = Image.fromarray(255-image_np)
image.save('./mj_reverse.jpeg')
#矩阵成图片
