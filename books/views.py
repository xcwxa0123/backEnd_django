import json
from .models import Book, Author, Episode
from .serializers import BookSerializer, AuthorSerializer, EpisodeSerializer
from rest_framework import viewsets, mixins
from django_filters import rest_framework as filters
from rest_framework.decorators import action

from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from .controllers import PageDealController, GetPageDetailController, GetEpisodeTextController, UpdateHotlistController, GetEpisodeListController
from .tools.page_nation import BookPageNation
from .tools.episode_filter import EpisodeListFilter

class AuthorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPageNation
    ordering_fields = ['hot_rank']
    ordering = '-hot_rank'

    # books/list
    @action(detail=False, methods=['get'])
    def get_books_byhot(self, request, *args, **kwargs):
        page_index = request.query_params.get('pageIndex', None)
        res = PageDealController().pageDeal(page_index)
        return HttpResponse(json.dumps(res, ensure_ascii=False))

    # books/detail
    @action(detail=False, methods=['get'])
    def get_page_detail(self, request, *args, **kwargs):
        page_href = request.query_params.get('pageHref', None)
        res = GetPageDetailController().getPageDetail(page_href)
        return HttpResponse(json.dumps(res, ensure_ascii=False))
    
    # update
    @action(detail=False, methods=['get'])
    def update_hotlist(self, request, *args, **kwargs):
        pageIndex = request.query_params.get('pageIndex', None)
        res = UpdateHotlistController().update_hotlist(pageIndex)
        return HttpResponse(json.dumps(res, ensure_ascii=False))
    

class EpisodeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = EpisodeListFilter
    # pagination_class = BookPageNation
        
    # episode/text
    @action(detail=False, methods=['get'])
    def get_episode_text(self, request, *args, **kwargs):
        page_href = request.query_params.get('pageHref', None)
        res = GetEpisodeTextController().getEpisodeText(page_href)
        return HttpResponse(json.dumps(res, ensure_ascii=False))
    
    # episode/list
    @action(detail=False, methods=['get'])
    def get_episode_list(self, request, *args, **kwargs):
        bookId = request.query_params.get('bookId', None)
        res = GetEpisodeListController().getEpisodeList(bookId, self)
        # print(f'res=================>{res}')
        # return HttpResponse(json.dumps(res, ensure_ascii=False))
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False})