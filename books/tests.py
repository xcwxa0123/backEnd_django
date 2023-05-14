from django.test import TestCase
from books.services import EpisodeService, SearchService
from books.tools import extract_text
from books.models import Episode, Book
from books.serializers import EpisodeSerializer
from django.db.models import Q
import pdb
import os
# Create your tests here.
# /works/16816700429263197780/episodes/16817330656452046849
# content = EpisodeService.get_episode_text(book_id='16816700429263197780', episode_id='16817330656452046849')
# print(f'content=======>{ content }')



# STORAGE_PATH = os.getenv('STORAGE_PATH')
# result = extract_text.find_dir(name='testName', path=STORAGE_PATH)
# print(f'result=====>{result}')
# print(f'STORAGE_PATH==========>{STORAGE_PATH}')


# print(os.getcwd())


# pdb.set_trace()
# SearchService.get_searched_list(search_name='13', page_index=1)

book_id = '16816927859824398859'
book_obj = Book.objects.get(book_id=book_id)
# Book.objects.delete(book_id=book_id)
book_obj.delete()


# episode_list = Episode.objects.filter(book=book_id)
# serializer = EpisodeSerializer(episode_list, many=True)
# print(serializer.data)


# print(serializer.is_valid())
# if serializer.is_valid():
#     print(serializer.data)
# else:
#     print(serializer.errors)

# book_list = Book.objects.filter(Q(hot_rank__gt=0) & Q(hot_rank__lt=51))
# book_list.update(hot_rank=999)
# print(len(book_list))