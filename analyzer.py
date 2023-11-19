from utils import decorator


@decorator
def analyze(faces: list, config) -> dict or None:
    after_filtering = []
    for face in faces:
        if face['location']["height"] < config["global_config"]["size"]["height"]["min"] or \
                face['location']['width'] < config['global_config']['size']['width']['min']:
            print(f'face {face["face_token"]} is too small, skip it...')
            continue
        if face['gender']['type'] != 'female' or face['gender']['probability'] < 0.39:
            print(f'face {face["face_token"]} seemingly not be female (probability low than 39 percentage), skip it...')
            continue
        if config['age_range']['lovely_daughter']['age']['min'] <= face['age'] <= \
                config['age_range']['lovely_daughter']['age']['max']:
            after_filtering.append({
                'describe': '一只可爱的女儿！',
                'age': face['age'],
                'score': face['beauty']
            })
        if config['age_range']['young_beauty']['age']['min'] <= face['age'] <= \
                config['age_range']['young_beauty']['age']['max']:
            after_filtering.append({
                'describe': '可爱的！',
                'age': face['age'],
                'score': face['beauty']
            })
    after_filtering.sort(key=lambda item: item.get('score'))
    if len(after_filtering) == 0:
        print('没有一个符合设置值的哦~')
        return None
    return after_filtering[0]
