import time
import cv2
import numpy as np
from PIL import Image
import datetime
import os
from easyocr import Reader


# 定义一个装饰器函数，可以统计函数的执行时间，输出函数名称和执行耗时
def decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('{} cost {} ms'.format(func.__name__, (end_time - start_time) * 1000))
        return result  # 返回函数的执行结果

    return wrapper


def three_histogram_similarity(template, target):
    # 通过得到RGB每个通道的直方图来计算相似度
    def classify_hist_with_split(image1, image2, size=(256, 256)):
        # 将图像resize后，分离为RGB三个通道，再计算每个通道的相似值
        image1 = cv2.resize(image1, size)
        image2 = cv2.resize(image2, size)
        sub_image1 = cv2.split(image1)
        sub_image2 = cv2.split(image2)
        sub_data = 0
        for im1, im2 in zip(sub_image1, sub_image2):
            sub_data += calculate(im1, im2)
        sub_data = sub_data / 3
        return sub_data

    # 计算单通道的直方图的相似值
    def calculate(image1, image2):
        hist1 = cv2.calcHist([image1], [0], None, [256], [0.0, 255.0])
        hist2 = cv2.calcHist([image2], [0], None, [256], [0.0, 255.0])
        # 计算直方图的重合度
        degree = 0
        for i in range(len(hist1)):
            if hist1[i] != hist2[i]:
                degree = degree + (1 - abs(hist1[i] - hist2[i]) / max(hist1[i], hist2[i]))
            else:
                degree = degree + 1
        degree = degree / len(hist1)
        return degree

    img1 = cv2.imread(template)
    img2 = cv2.imread(target)
    n = classify_hist_with_split(img1, img2)
    return round(n[0], 3)


def find_icon(image_path, icon_path):
    # 读取图片和图标
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    icon = cv2.imread(icon_path, cv2.IMREAD_UNCHANGED)

    # 使用OpenCV的matchTemplate函数进行模板匹配
    result = cv2.matchTemplate(image, icon, cv2.TM_CCOEFF_NORMED)

    # 设定阈值，如果匹配度大于阈值，则认为找到了图标
    threshold = 0.8
    loc = np.where(result >= threshold)
    # print(loc[0])

    # 如果找到了图标，返回True，否则返回False
    if len(loc[0]) > 0:
        return sum(loc[0])
    else:
        return 0


def crop_image(source_file, left_top, right_bottom_or_width, height=None, out=None):
    out = 'cropped_image.jpg' if not out else out
    # 打开源文件
    img = Image.open(source_file).convert('RGB')

    # 获取图片的宽度和高度
    img_width, img_height = img.size

    # 如果第三个参数是一个元组，则它表示右下角坐标
    if isinstance(right_bottom_or_width, tuple):
        right_bottom = right_bottom_or_width
    # 否则，第三个参数和第四个参数表示截取的宽度和高度
    else:
        right_bottom = (min(left_top[0] + right_bottom_or_width, img_width), min(left_top[1] + height, img_height))

    # 截取图片
    cropped_img = img.crop((*left_top, *right_bottom))
    # 保存截取的图片
    cropped_img.save(out)


def get_current_time():
    # 获取当前时间
    now = datetime.datetime.now()

    # 格式化时间为字符串
    time_str = now.strftime('%Y%m%d-%H%M%S')

    return time_str


def rename_files(path, prefix, start_num):
    # 获取路径下所有文件的文件名
    files = os.listdir(path)

    # 遍历每个文件
    for i, file in enumerate(files):
        # 获取文件扩展名
        extension = os.path.splitext(file)[1]

        # 构建新的文件名
        new_name = prefix + '-' + str(start_num + i) + extension

        # 重命名文件
        os.rename(os.path.join(path, file), os.path.join(path, new_name))

    # 输入路径、字符串和数字


def recognize_text(image_path, use_gpu=False):
    try:
        # 初始化EasyOCR模型
        ocr = Reader(['ch_sim', 'en'], gpu=use_gpu, model_storage_directory='./model/',
                     user_network_directory='./model/')
        # 读取图片并进行识别
        result = ocr.readtext(image_path, detail=0)
        # 如果识别结果为空，返回空字符串
        if not result:
            return ''
            # 否则，返回识别结果
        return result
    except Exception as e:
        # 如果出现异常，打印错误消息并返回空字符串
        print(f"Error occurred while trying to recognize text from image: {e}")
        return ''


def check_adb_connection():
    result = os.popen('adb devices').read()
    lines = result.strip().split('\n')

    if len(lines) <= 1 or not lines[-1].endswith('device'):
        raise Exception('没有设备连接到adb')
