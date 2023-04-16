import json
from .models import Book, Author, Episode
from .serializers import BookSerializer, AuthorSerializer, EpisodeSerializer
from rest_framework import viewsets, mixins
# from rest_framework import permissions
from rest_framework.decorators import action

from rest_framework.response import Response
from django.http import HttpResponse
from .controllers import PageDealController, GetPageDetailController, GetEpisodeTextController, UpdateHotlistController

class AuthorViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer(queryset, many=True)

class BookViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer(queryset, many=True)

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
    

class EpisodeViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer(queryset, many=True)
        
    # episode/text
    @action(detail=False, methods=['get'])
    def get_episode_text(self, request, *args, **kwargs):
        page_href = request.query_params.get('pageHref', None)
        res = GetEpisodeTextController().getEpisodeText(page_href)
        return HttpResponse(json.dumps(res, ensure_ascii=False))