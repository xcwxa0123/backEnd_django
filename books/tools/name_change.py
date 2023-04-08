#coding=Shift_JIS
import os
import re
from bs4 import BeautifulSoup
from trans_params import SHOUSETSUNAROU_PARAMS as PARAMS_DATA

def transe_name(data_params):
    for file_name in os.listdir(data_params.get('TEXTFILE_PATH')):
        if re.search(r'\d+', file_name):
            start, end = re.search(r'\d+', file_name).span()
            new_name = file_name[start:end:]
            os.rename('{0}/{1}'.format(data_params.get('TEXTFILE_PATH'), file_name), '{0}/{1}'.format(data_params.get('TEXTFILE_PATH'), new_name))
        else: 
            new_name = ''
            with open('{0}/{1}'.format(data_params.get('TEXTFILE_PATH'), file_name), encoding='utf-8', errors='ignore') as temp_file:
                content = temp_file.read()
                soup = BeautifulSoup(content, 'html.parser')
                content_body = soup.find_all(data_params.get('CHAPTER_NUM_DOM_TYPE'), class_=data_params.get('CHAPTER_NUM_CLASS'))
                title_text = ''.join(list(content_body[0].strings))
                if re.search(r'\d+', title_text):
                    start, end = re.search(r'\d+', title_text).span()
                    new_name = title_text[start:end:]
            os.rename('{0}/{1}'.format(data_params.get('TEXTFILE_PATH'), file_name), '{0}/{1}'.format(data_params.get('TEXTFILE_PATH'), new_name))