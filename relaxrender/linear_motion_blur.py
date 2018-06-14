import math
import numpy as np
from PIL import Image
from scipy.signal import convolve2d

from relaxrender.LineDictionary import LineDictionary  # 导入角度-？字典

lineLengths = [3, 5, 7, 9, 20]  # 线性长度
lineTypes = ["full", "right", "left"]  # 控制模糊内核是全部应用还是仅应用于其左/右一半。

lineDict = LineDictionary()


def LinearMotionBlur_random(img):
    """
    随机选择模式进行模糊
    """
    lineLengthIdx = np.random.randint(0, len(lineLengths))
    lineTypeIdx = np.random.randint(0, len(lineTypes))
    lineLength = lineLengths[lineLengthIdx]
    lineType = lineTypes[lineTypeIdx]
    lineAngle = randomAngle(lineLength)
    return LinearMotionBlur(img, lineLength, lineAngle, lineType)


def LinearMotionBlur(img, dim, angle, linetype):
    imgarray = np.array(img, dtype="float32")  # 将图片转换为数组
    kernel = LineKernel(dim, angle, linetype)  # 获得线性核
    imgs = []
    for d in range(3):
        # 对图像的RGB三个通道做循环处理
        img_conv_d = convolve2d(imgarray[:, :, d], kernel, mode='same', boundary='symm')
        imgs.append(img_conv_d)
    img_conv = np.stack(imgs, axis=2).astype("uint8")
    img = Image.fromarray(img_conv)  # 将数组转换回图片
    return img


def LineKernel(dim, angle, linetype):
    """
    线性核
    """
    kernelwidth = dim  # 核的宽度
    kernelCenter = int(math.floor(dim / 2))  # 核的中心
    angle = SanitizeAngleValue(kernelCenter, angle)  # 运动线的角度。将被定位到与给定内核大小相关的最近的一个。
    kernel=lineDict.Createkernel(dim,angle)
    normalizationFactor = np.count_nonzero(kernel)  # 返回kernel中非0元素的个数
    kernel = kernel / normalizationFactor  # 归一化
    return kernel


def SanitizeAngleValue(kernelCenter, angle):
    """
    输入角度规范化
    """
    numDistinctLines = kernelCenter * 4
    angle = math.fmod(angle, 180.0)  # angle对180度取模
    validLineAngles = np.linspace(0, 180, numDistinctLines,
                                  endpoint=False)  # 把[0,180]区间等分为numDistinctLines份，如kerneldim=9时，分为16份
    angle = nearestValue(angle, validLineAngles)  # 找与输入角度最接近的角度
    return angle


def nearestValue(theta, validAngles):
    """
    获取与输入角度最接近的角度
    """
    idx = (np.abs(validAngles - theta)).argmin()
    return validAngles[idx]  # 返回角度值


def randomAngle(kerneldim):
    """
    随机获取角度
    """
    kernelCenter = int(math.floor(kerneldim / 2))
    numDistinctLines = kernelCenter * 4
    validLineAngles = np.linspace(0, 180, numDistinctLines,
                                  endpoint=False)  # 把[0,180]区间等分为numDistinctLines份，如kerneldim=9时，分为16份
    angleIdx = np.random.randint(0, len(validLineAngles))  # 角度的索引号(随机获得)
    return int(validLineAngles[angleIdx])  # 返回随机获取的角度
