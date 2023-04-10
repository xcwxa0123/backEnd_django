import json
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets, mixins
# from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.decorators import api_view
# from quickstart.serializers import UserSerializer, GroupSerializer

from rest_framework.response import Response
from django.http import HttpResponse
from .controllers import PageDealController, GetPageDetailController, GetEpisodeTextController



# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
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
    
    # episode/text
    @action(detail=False, methods=['get'])
    def get_episode_text(self, request, *args, **kwargs):
        page_href = request.query_params.get('pageHref', None)
        res = GetEpisodeTextController().getEpisodeText(page_href)
        return HttpResponse(json.dumps(res, ensure_ascii=False))
    
    # @action(detail=False, methods=['get'])
    # def get_all_users(self, request):
    #     """
    #     自定义的 list() 方法，返回所有用户列表。
    #     """
    #     serializer = self.get_serializer(self.queryset, many=True)
    #     return Response(serializer.data)

    # @action(detail=False, methods=['post'])
    # def create_new_user(self, request):
    #     """
    #     自定义的 create() 方法，用于创建新用户。
    #     """
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data)