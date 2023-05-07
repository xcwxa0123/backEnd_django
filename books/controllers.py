from .services import GetPageDetailService, PageDealService, GetEpisodeTextService, GetEpisodeListService
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
class GetEpisodeFileController:
    def getEpisodeFile(self, book_id, episode_id):
        resData = {}
        if not book_id or not episode_id:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            
            resData = GetEpisodeTextService.get_episode_file(book_id, episode_id)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }

class GetEpisodeListController:    
    def getEpisodeList(self, book_id, cls):
        resData = None
        if not book_id:
            return { 'data': {}, 'code': 500, 'msg': '主键id有误' }
        try:
            
            resData = GetEpisodeListService.get_episode_list(book_id, cls)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        

class UpdateHotlistController:
    def update_hotlist(self, page_index):
        resData = {}
        if not page_index:
            page_index = 0
        try:
            
            resData = PageDealService.update_hotlist(page_index)
        except Exception as e:
            print(f'e================>{e}')
            return { 'data': {}, 'code': 500, 'msg': str(e) }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
