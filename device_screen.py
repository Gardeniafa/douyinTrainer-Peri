import os
import time
import utils
from PIL import Image
from utils import decorator
from func_timeout import func_set_timeout
import func_timeout
import xml.etree.ElementTree as ElTree


# 图片压缩比例
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0


@decorator
def get_dou_yin_img(index, path, config: dict):
    # 截图
    os.system("adb shell /system/bin/screencap -p /sdcard/screenshot.jpg")
    os.system(f"adb pull /sdcard/screenshot.jpg {path}/face-{index}.jpg")
    os.system("adb shell rm /sdcard/screenshot.jpg")
    # cut picture
    utils.crop_image(f"{path}/face-{index}.jpg", (config['from']['x'], config['from']['y']),
                     (config['to']['x'], config['to']['y']), out=f"{path}/face-{index}_cut.jpg")
    # 压缩图片
    img = Image.open(f"{path}/face-{index}_cut.jpg").convert('RGB')
    scale = SIZE_small
    w, h = img.size
    img.thumbnail((int(w / scale), int(h / scale)))
    img.save(f'{path}/face-{index}_compressed.jpg')


class Layout:
    def __init__(self):
        @func_set_timeout(2)
        def dump_ui():
            si = time.time()
            print('try to get uiautomator dump file.')
            os.system('adb shell "uiautomator dump /sdcard/ui111.xml 2>/dev/null"')
            ti = time.time()
            print('dump time cost {} ms'.format((ti - si) * 1000))
        counter = 0
        while not False:
            try:
                counter += 1
                dump_ui()
            except func_timeout.exceptions.FunctionTimedOut:
                print(f'dump failed, try again({counter})...')
                time.sleep(0.9)
                pass
            else:
                break
        s = time.time()
        # 将UI层次结构文件从设备拉取到本地
        os.system('adb pull /sdcard/ui111.xml')
        os.system('adb shell rm /sdcard/ui111.xml')
        t = time.time()
        print('pull time cost {} ms'.format((t - s) * 1000))
        # 使用XML解析器打开UI层次结构文件
        s = time.time()
        tree = ElTree.parse('./ui111.xml')
        os.remove('./ui111.xml')
        t = time.time()
        print('parse time cost {} ms'.format((t - s) * 1000))
        self.root = tree.getroot()

    def find_element_by_id(self, element_id: str):
        # 遍历XML查找指定控件ID
        for element in self.root.iter():
            if 'resource-id' in element.attrib and element.attrib['resource-id'].endswith(f':id/{element_id}'):
                return True
        return False

    def find_element_str_by_id(self, element_id):
        # 遍历XML查找指定控件ID
        for element in self.root.iter():
            if 'resource-id' in element.attrib and element.attrib['resource-id'].endswith(f':id/{element_id}'):
                return element.attrib['text']
        return ''
# mcd 点击进入直播间
# qja 广告 汽水音乐
# hmv +关注
# gzo
# z5b 直播
# title 用户名
