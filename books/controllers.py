from .services import GetPageDetailService, PageDealService, GetEpisodeTextService
from .models import Author, Book, Episode
# 获取详情
class GetPageDetailController:
    def getPageDetail(self, page_href):
        resData = {}
        if not page_href:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
        # 这里数据格式有问题
            resData = GetPageDetailService.get_page_detail(page_href)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }

# 获取列表
class PageDealController:
    def pageDeal(self, page_index):
        resData = {}
        if not page_index:
            page_index = 0
        try:
        # 这里数据格式有问题
            resData = PageDealService.get_book_msg(page_index)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }

# 获取章节内容
class GetEpisodeTextController:
    def getEpisodeText(self, page_href):
        resData = {}
        if not page_href:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            
            resData = GetEpisodeTextService.get_episode_text(page_href)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
class AuthorCURDController:
    # 创建或更新
    def create_author(self, **kwargs):
        new_author = Author(**kwargs)
        new_author.full_clean()
        new_author.save()

    def get_author(self, author_id):
        try:
            return Author.objects.get(author_id=author_id)
        except Author.DoesNotExist:
            return None
    
    def update_author(self, **kwargs):
        author_id = kwargs.get('author_id')
        author_obj = self.get_author(author_id)
        if author_obj:
            kwargs.pop('author_id')
            for key, value in kwargs.items():
                author_obj[key] = value
            author_obj.save()
        else:
            self.create_author(**kwargs)

class BookCURDController:
    # 创建或更新
    def create_book(self, **kwargs):
        new_book = Book(**kwargs)
        new_book.full_clean()
        new_book.save()

    def get_book(self, book_id):
        try:
            return Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return None
        
    def update_book(self, **kwargs):
        book_id = kwargs.get('book_id')
        book_obj = self.get_book(book_id)
        if book_obj:
            kwargs.pop('book_id')
            for key, value in kwargs.items():
                book_obj[key] = value
            book_obj.save()
        else:
            self.create_book(**kwargs)

class EpisodeCURDController:
    # 创建或更新
    def create_episode(self, **kwargs):
        new_episode = Episode(**kwargs)
        new_episode.full_clean()
        new_episode.save()

    def get_episode(self, episode_id):
        try:
            return Episode.objects.get(episode_id=episode_id)
        except Episode.DoesNotExist:
            return None
        
    def update_episode(self, **kwargs):
        episode_id = kwargs.get('episode_id')
        episode_obj = self.get_episode(episode_id)
        if episode_obj:
            kwargs.pop('episode_id')
            for key, value in kwargs.items():
                episode_obj[key] = value
            episode_obj.save()
        else:
            self.create_episode(**kwargs)