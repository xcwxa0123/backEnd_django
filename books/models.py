from django.db import models

class Author(models.Model):
    # 主键作者ID
    author_id = models.TextField(blank=False, null=False, primary_key=True)
    # 作者名字
    author_name = models.TextField(blank=False, null=False)
    
class Book(models.Model):
    # 主键书ID
    book_id = models.CharField(max_length=100, primary_key=True)
    # 作者ID,外键关联
    author_id = models.ForeignKey(Author, to_field='author_id', on_delete=models.CASCADE, related_name='books')
    # 书名
    book_title = models.TextField(blank=False, null=False)
    # 简介
    book_desc = models.TextField(blank=False, null=False)
    # 状态 0-停更 1-连载中
    publish_state = models.CharField(max_length=10)
    # 上次更新时间
    last_time = models.TextField(blank=False, null=False)
    # 总话数
    number_of_episode = models.CharField(max_length=10)
    # 热度
    hot_rank = models.IntegerField(blank=False)

class Episode(models.Model):
    # 主键章节ID
    episode_id = models.CharField(max_length=100, primary_key=True)
    # 外键书ID
    book_id = models.ForeignKey(Book, to_field='book_id', on_delete=models.CASCADE, related_name='episodes')
    # 大章节标题
    main_title = models.TextField(blank=False, null=False)
    # 小章节标题
    sub_title = models.TextField(blank=False, null=False)
    # 章节上一次更新时间
    refresh_time = models.TextField(blank=False, null=False)
    # 该章节是否需要更新，0-不需要，1-需要
    isupdated = models.CharField(max_length=10, default=1)
    # 该章节在服务器上储存地址
    server_address = models.TextField(blank=True, null=False, default='')
