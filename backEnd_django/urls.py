
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import BookViewSet, EpisodeViewSet

router = routers.DefaultRouter()
router.register(r'implapi/books/list', BookViewSet, basename='books')
router.register(r'implapi/episode/viewlist', EpisodeViewSet, basename='episode')

urlpatterns = [
    path('', include(router.urls)),
    # path('implapi/books/list', BookViewSet.as_view({'get': 'list'}), name='book-list'),
    # path('implapi/books/detail', BookViewSet.as_view({'get': 'get_page_detail'}), name='book-detail'),
    # path('implapi/episode/list', EpisodeViewSet.as_view({'get': 'get_episode_list'}), name='episode-list'),
    path('implapi/episode/text', EpisodeViewSet.as_view({'get': 'get_episode_text'}), name='episode-text'),
    path('implapi/episode/getFile', EpisodeViewSet.as_view({'get': 'get_episode_file'}), name='episode-file'),
    path('implapi/books/updateList', BookViewSet.as_view({'get': 'update_hotlist'}), name='update-hotlist'),
    path('admin/', admin.site.urls),
]
