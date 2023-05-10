from django.test import TestCase
from books.services import EpisodeService
from books.tools import extract_text
import os
# Create your tests here.
# /works/16816700429263197780/episodes/16817330656452046849
content = EpisodeService.get_episode_text(book_id='16816700429263197780', episode_id='16817330656452046849')
print(f'content=======>{ content }')



# STORAGE_PATH = os.getenv('STORAGE_PATH')
# result = extract_text.find_dir(name='testName', path=STORAGE_PATH)
# print(f'result=====>{result}')
# print(f'STORAGE_PATH==========>{STORAGE_PATH}')


# print(os.getcwd())