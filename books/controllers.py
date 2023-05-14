from .services import UpdateService, EpisodeService, SearchService
# episode相关接口控制器
class EpisodeController:
    def getEpisodeText(self, book_id, episode_id):
        resData = {}
        if not book_id or not episode_id:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            
            resData = EpisodeService.get_episode_text(book_id, episode_id)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
    def getEpisodeFile(self, book_id, episode_id):
        resData = {}
        if not book_id or not episode_id:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            
            resData = EpisodeService.get_episode_file(book_id, episode_id)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }

# 更新相关的接口控制器
class UpdateController:
    def update_hotlist(self, page_index):
        resData = {}
        if not page_index:
            page_index = 0
        try:
            resData = UpdateService.update_hotlist(page_index)
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
    def update_episodelist(self, book_id):
        resData = {}
        if not book_id:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            resData = UpdateService.refresh_episode(book_id)
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
class SearchController:
    def get_searched_list(self, search_name, page_index):
        resData = {}
        if not page_index:
            page_index = 0
        if not search_name:
            search_name = ''
        try:
            resData = SearchService.get_searched_list(search_name, page_index)
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'search success' }
        
    def get_searched_book(self, book_data):
        resData = {}
        if not book_data:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            resData = SearchService.get_searched_book(book_data)
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }

        
