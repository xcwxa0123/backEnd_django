from django.db import models

class Book(models.Model):
    title = models.TextField(blank=False, null=False)
    author = models.CharField(max_length=100)
    desc = models.TextField(blank=False, null=False)
    main_id = models.CharField(max_length=100)
    def __str__(self):
        return self.title