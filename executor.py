import time
import utils
import os
import math


def exe(face_arg: dict or None, config, index, path):
    manipulate_config = config['device_manipulate']
    global_config = config['settings']['global_config']
    if face_arg:
        f = open(f'{path}/log.inf', 'a')
        f.write(f'Index {index}\n')
        # layout = device_screen.Layout()
        # normal_video = layout.find_element_by_id('gzo')
        # can_follow = layout.find_element_by_id('hmv')
        # name = layout.find_element_str_by_id('title')
        print('face arg:', face_arg)
        f.write(f'      | {face_arg}\n')
        normal_video = is_normal_video(index, path)
        can_follow = can_follow_now(index, path)
        if can_follow:
            f.write(f'      | follow btn hit at image follow-{can_follow["hit-number"]}.jpg\n')
            print('follow: ', can_follow)
        is_ad = fuck_ad(index, path)
        print(f'have ad: {"No" if not is_ad else is_ad}')
        f.write(f'      | have ad: {is_ad if not is_ad else is_ad}\n')
        print('normal video: ', normal_video, ', can follow: ', can_follow)
        f.write(f"      | normal video: {normal_video}\n")
        f.write(f"      | can follow: {can_follow}\n")
        score = face_arg['score']
        # if score >= global_config['beauty']['amazing']:
        #     if can_follow:
        #         follow(manipulate_config)
        if not normal_video:
            f.write(f'      - not manipulate...\n')
            face_arg = None
            print('不合适操作，下一个')
        else:
            # print(f"id：{name}")
            if not is_ad:
                f.write(f'      | page content: {is_ad}\n')
                if score >= global_config['beauty']['excellent']:
                    if can_follow:
                        follow(can_follow['pos'], manipulate_config)
                        f.write(f'      | do follow\n')
                if score >= global_config['beauty']['greet']:
                    like(manipulate_config)
                    f.write(f'      | do like\n')
            else:
                f.write(f'      | is ad, so do not like and follow\n')
                face_arg = None
            if score > global_config['beauty']['good']:
                share(manipulate_config)
                f.write(f'      - do share\n\n')
        f.close()
    remove_cropped_image(f'{path}/face-{index}.jpg')
    face_arg = {'score': 0} if face_arg is None else face_arg
    next_video(manipulate_config, face_arg['score'])


def remove_cropped_image(path, really_do_this=False):
    if really_do_this:
        os.remove(path)


def is_normal_video(idx, path):
    utils.crop_image(f'{path}/face-{idx}.jpg', (938, 1153), (1038, 1945), out=f'{path}/face-{idx}-crop_nor.jpg')
    counter = 0
    sv = 0
    for symbol in ('like', 'comment', 'star', 'transmit'):
        v = utils.find_icon(f'{path}/face-{idx}-crop_nor.jpg', f'./symbol/{symbol}.jpg')
        if v:
            counter += 1
            sv += v
        if counter > 1:
            remove_cropped_image(f'{path}/face-{idx}-crop_nor.jpg')
            return sv
    remove_cropped_image(f'{path}/face-{idx}-crop_nor.jpg')
    return False


@utils.decorator
def fuck_ad(idx, path):
    # 0, 1650 -> 1080, 2180
    # 购物 广告 福利
    utils.crop_image(f'{path}/face-{idx}.jpg', (0, 1650), (1080, 2180), out=f'{path}/face-{idx}-crop_ad_scan.jpg')
    text = utils.recognize_text(f'{path}/face-{idx}-crop_ad_scan.jpg')
    print('ad fucker recognize: ', text)
    remove_cropped_image(f'{path}/face-{idx}-crop_ad_scan.jpg')
    ads = ['购物', '广告', '福利', '商品', '企业', '公司', '基金', '理财', '银行', '星巴克', '迪丽热巴', '期货', '电竞', '热卖',
           '店铺', '口腔', '创业', '成人', '考研', '专升本', '律师']
    for text_spices in text:
        for ad in ads:
            if ad in text_spices:
                return ', '.join(text)
    return ''


@utils.decorator
def can_follow_now(idx, path):
    follows_len = 94
    utils.crop_image(f'{path}/face-{idx}.jpg', (958, 1163), (1018, 1223), out=f'{path}/face-{idx}-crop_fol_1.jpg')
    for i in range(follows_len):
        if utils.find_icon(f'{path}/face-{idx}-crop_fol_1.jpg', f'./symbol/follows/follow-{i}.jpg'):
            remove_cropped_image(f'{path}/face-{idx}-crop_fol_1.jpg')
            return {'pos': 'high', 'hit-number': i}
    utils.crop_image(f'{path}/face-{idx}.jpg', (958, 1042), (1018, 1102), out=f'{path}/face-{idx}-crop_fol_2.jpg')
    for i in range(follows_len):
        if utils.find_icon(f'{path}/face-{idx}-crop_fol_2.jpg', f'./symbol/follows/follow-{i}.jpg'):
            remove_cropped_image(f'{path}/face-{idx}-crop_fol_2.jpg')
            return {'pos': 'low', 'hit-number': i}
    remove_cropped_image(f'{path}/face-{idx}-crop_fol_2.jpg')
    return False


def next_video(config: dict, score):
    if score > 30:
        x = score
        x = (x - 30) / (70 - 30)
        # 使用指数函数，使得结果在0.1-3之间，且x越大，结果变化越快
        result = 0.1 + (3 - 0.1) * math.exp(x) / (1 + math.exp(x))
        time.sleep(result)
    os.system(f'adb shell input swipe {config["swipe"]["next"]["from"]["x"]} {config["swipe"]["next"]["from"]["y"]} '
              f'{config["swipe"]["next"]["to"]["x"]} {config["swipe"]["next"]["to"]["y"]} '
              f'{config["swipe"]["next"]["time"]}')
    time.sleep(0.6)
    print("下一个")


def follow(pos: str, config: dict):
    os.system(f'adb shell input tap {config["click"]["follow"][pos]["x"]} {config["click"]["follow"][pos]["y"]}')
    time.sleep(0.3)
    print('惊为天人，关注！')


def like(config: dict):
    # 800 1269
    os.system(f'adb shell input tap {config["click"]["like"]["x"]} {config["click"]["like"]["y"]}')
    time.sleep(0.013)
    os.system(f'adb shell input tap {config["click"]["like"]["x"]} {config["click"]["like"]["y"]}')
    time.sleep(1.3)
    print('不赖，点个小心心')


def share(config):
    os.system(f'adb shell input tap {config["click"]["share"]["btn"]["x"]} {config["click"]["share"]["btn"]["y"]}')
    time.sleep(0.6)
    os.system(f'adb shell input tap {config["click"]["share"]["friend"]["x"]} '
              f'{config["click"]["share"]["friend"]["y"]}')
    time.sleep(0.6)
    os.system(f'adb shell input tap {config["click"]["share"]["ensure"]["x"]} '
              f'{config["click"]["share"]["ensure"]["y"]}')
    time.sleep(0.9)
    print('分享一下~')
