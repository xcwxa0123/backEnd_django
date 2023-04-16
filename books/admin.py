from django.contrib import admin

# Register your models here.
from .models import Author, Book, Episode

admin.site.register((Author, Book, Episode))