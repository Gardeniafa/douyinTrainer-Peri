import time
import yaml
import baidu_ai
import device_screen
import analyzer
import executor
import utils
from utils import get_current_time
import os
import random

if __name__ == '__main__':
    try:
        utils.check_adb_connection()
        with open('./config.yaml', 'r') as f:
            config = yaml.safe_load(f)
            host = f'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials' \
                   f'&client_id={config["application"]["token"]}&client_secret={config["application"]["secret"]}'
            token = baidu_ai.get_token(host)
            counter = 0
            log_folder = f'./log/{get_current_time()}'
            os.makedirs(log_folder)
            while not False:
                counter += 1
                print(f"----------------------The NO.{counter} video---------------------------")
                print('watching about 1 seconds...')
                time.sleep(1.5 + random.choice([-1, 0, 1, -0.5, 0.5]))
                device_screen.get_dou_yin_img(counter, log_folder)
                if not executor.is_normal_video(counter, log_folder):
                    print('not normal video, skip...')
                    with open(f'{log_folder}/log.inf', 'a') as t:
                        t.write(f'Index {counter}\n')
                        t.write(f'      | not normal video, skip...\n\n')
                    result = None
                else:
                    device_screen.precaution_upload_to_api(counter, log_folder, config['settings']['global_config']['cut'])
                    faces = baidu_ai.get_baidu_face_tech(f'{log_folder}/face-{counter}_compressed.jpg', token)
                    result = analyzer.analyze(faces, config["settings"])
                executor.exe(result, config, counter, log_folder)
    except Exception as ex:
        print(ex)
        print('program exit...')
