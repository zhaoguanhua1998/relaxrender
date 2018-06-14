from relaxrender import linear_motion_blur
from matplotlib import pyplot as plt
import imageio
from PIL import Image
import numpy as np
import math

img = Image.open('./picture_test.jpg')  # shape of img is (682,1023,3)
area = (40, 681, 217, 766)
# img_origin = linear_motion_blur.LinearMotionBlur_random(img)
img_blur = linear_motion_blur.LinearMotionBlur(img, dim=20, angle=135, area=area)
# img_blur_withoutarea = linear_motion_blur.LinearMotionBlur(img, dim=20, angle=135)
plt.figure("img_blur")  # 图像窗口名称
# plt.imshow(img_origin)
plt.imshow(img_blur)
plt.axis('on')  # 开启坐标轴
plt.title('img_blur')  # 图像题目
plt.show()
