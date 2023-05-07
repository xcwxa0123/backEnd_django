import os
from bs4 import BeautifulSoup
from .trans_params import KAKUYOMU_PARAMS as PARAMS_DATA
# from trans_params import SHOUSETSUNAROU_PARAMS as PARAMS_DATA
# import name_change as nc
# import threading

# r = threading.Lock()
# HTML文件转为txt
# path=要读的文件的全路径; name=文件名; write_path=写入路径
# def trans_text(path, name, write_path, params_data):
def trans_text(soup, params_data=PARAMS_DATA):
    js_episode_body = soup.find_all('div', class_=params_data.get('TARGET_DOM_CLASS'))
    big_strings = ''
    for body_item in js_episode_body:
        big_strings = big_strings + ''.join(list(body_item.strings))
    return big_strings

def set_file(text, file_addr):
    # file_addr = '{0}/{1}.txt'.format(write_path, name)
    with open(file_addr, mode='w', encoding='utf-8') as transe_file:
        try:
            transe_file.write(text)
        except Exception as e:
            print(f'write { file_addr } error { e }')
            return None
        else:
            print(f'write { file_addr } success!')
            return file_addr
    return 
# 找一下文件夹在不在目标目录下，不在就创建
def find_dir(path, name):
    # def _mk_target_dir():
    #     # os.mkdir(params_data.get('WRITE_DIR_NAME'))
    #     # os.mkdir(os.path.join(path, params_data.get('WRITE_DIR_NAME')))
    #     return os.path.join(path, params_data.get('WRITE_DIR_NAME'))
    target_path = os.path.join(path, name)
    if not os.path.isdir(target_path):
        try:
            os.makedirs(target_path, exist_ok=True)
        except OSError:
            print(f"Creation of the directory {target_path} failed")
        else:
            print(f"Directory {target_path} created successfully")
            return target_path
    else:
        return target_path

    # try:
    #     temp_dir_list = os.path.isdir(path)
    #     print(f'temp_dir_list=======>{temp_dir_list}')
    # except FileNotFoundError as e:
    #     os.makedirs(os.path.join(path, name), exist_ok=True)
    # else:
    #     if name not in temp_dir_list:
    #         os.makedirs(os.path.join(path, name), exist_ok=True)

def transe_start(params_data):
    # 创建目标目录
    target = find_dir(params_data.get('WRITE_DIR_NAME'), params_data, params_data.get('TARGET_CREATE_PATH'))
    target() if target else None
    # 开始转写
    file_list = os.listdir(params_data.get('TEXTFILE_PATH'))
    for file_name in file_list:
        trans_text('{0}/{1}'.format(params_data.get('TEXTFILE_PATH'), file_name), file_name, '{0}/{1}'.format(params_data.get('TARGET_CREATE_PATH'), params_data.get('WRITE_DIR_NAME')), params_data)

# def start():
#     r.acquire()
#     nc.transe_name(PARAMS_DATA)
#     transe_start(PARAMS_DATA)
#     r.release()

# start()