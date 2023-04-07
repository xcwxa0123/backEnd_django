
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from books.views import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('implapi/books/list', BookViewSet.as_view({'get': 'get_books_byhot'}), name='book-list'),
    path('implapi/books/detail', BookViewSet.as_view({'get': 'get_page_detail'}), name='book-detail'),
    # path('admin/', admin.site.urls),
]
