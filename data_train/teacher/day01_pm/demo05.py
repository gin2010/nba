import numpy as np
# 处理图形图像的库
from PIL import Image

image = Image.open("../data/timg.jpg")
print(image,type(image))
image = np.array(image)
print(image,type(image),image.shape)
image = 255 - image
# 把矩阵重新转化为图片
image = Image.fromarray(image)
image.save("../data/timg2.jpg")
