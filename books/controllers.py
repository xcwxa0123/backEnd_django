from .services import UpdateService, EpisodeService
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
            resData = UpdateService.update_detail(book_id, {})
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
