from rest_framework import serializers
from .models import Book, Author, Episode

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    class Meta:
        model = Book
        fields = '__all__'
        # exclude = ['hot_rank']

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        # fields = '__all__'
        exclude = ['isupdated', 'server_address']
