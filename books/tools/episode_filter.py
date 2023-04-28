from django_filters import rest_framework as filters
from books.models import Episode
class EpisodeListFilter(filters.FilterSet):
    book = filters.NumberFilter(field_name='book_id__book_id')
    class Meta:
        model = Episode
        fields = ['book']