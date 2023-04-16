from .models import Author, Book, Episode
import pdb
import copy

class AuthorCURDController:
    # 创建或更新
    def create_author(self, author_data):
        new_author = Author(author_id=author_data['author_id'], author_name=author_data['author_name'])
        new_author.full_clean()
        new_author.save()

    def get_author(self, author_id):
        try:
            return Author.objects.get(author_id=author_id)
        except Author.DoesNotExist:
            return None
    
    def update_author(self, author_data):
        copy_data = copy.deepcopy(author_data)
        author_id = copy_data.get('author_id')
        author_obj = self.get_author(author_id)
        if author_obj:
            copy_data.pop('author_id')
            update_key = 0
            for key, value in copy_data.items():
                if getattr(author_obj, key) != value:
                    setattr(author_obj, key, value)
                    update_key = 1
            if update_key:
                author_obj.save()
        else:
            self.create_author(copy_data)

class BookCURDController:
    # 创建或更新
    def create_book(self, book_data):
        author = AuthorCURDController().get_author(book_data['author_id'])
        new_book = Book(
            book_id=book_data['book_id'],
            # author_id=book_data['author_id'],
            author_id=author,
            book_title=book_data['book_title'],
            book_desc=book_data['book_desc'],
            publish_state=book_data['publish_state'],
            last_time=book_data['last_time'],
            number_of_episode=book_data['number_of_episode'],
        )
        new_book.full_clean()
        new_book.save()

    def get_book(self, book_id):
        try:
            return Book.objects.get(book_id=book_id)
        except Book.DoesNotExist:
            return None
        
    def update_book(self, book_data):
        copy_data = copy.deepcopy(book_data)
        book_id = copy_data.get('book_id')
        book_obj = self.get_book(book_id)
        if book_obj:
            copy_data.pop('book_id')
            copy_data.pop('author_id')
            update_key = 0
            for key, value in copy_data.items():
                if getattr(book_obj, key) != value:
                    setattr(book_obj, key, value)
                    update_key = 1
                # book_obj[key] = value
            if update_key:
                book_obj.save()
        else:
            self.create_book(copy_data)

class EpisodeCURDController:
    # 创建或更新
    def create_episode(self, episode_data):
        book = BookCURDController().get_book(episode_data['book_id'])
        new_episode = Episode(
            episode_id=episode_data['episode_id'],
            # book_id=episode_data['book_id'],
            book_id=book,
            main_title=episode_data['main_title'],
            sub_title=episode_data['sub_title'],
            refresh_time=episode_data['refresh_time'],
            isupdated=episode_data['isupdated'],
            server_address=episode_data['server_address'],
        )
        new_episode.full_clean()
        new_episode.save()

    def get_episode(self, episode_id):
        try:
            return Episode.objects.get(episode_id=episode_id)
        except Episode.DoesNotExist:
            return None
        
    def update_episode(self, episode_data):
        copy_data = copy.deepcopy(episode_data)
        episode_id = copy_data.get('episode_id')
        episode_obj = self.get_episode(episode_id)
        if episode_obj:
            copy_data.pop('episode_id')
            copy_data.pop('book_id')
            update_key = 0
            for key, value in copy_data.items():
                if getattr(episode_obj, key) != value:
                    setattr(episode_obj, key, value)
                    update_key = 1
            if update_key:
                episode_obj.save()
        else:
            self.create_episode(copy_data)