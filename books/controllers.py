from .services import GetPageDetailService, PageDealService, GetEpisodeTextService
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
        

class UpdateHotlistController:
    def update_hotlist(self, page_index):
        resData = {}
        if not page_index:
            page_index = 0
        try:
            
            resData = PageDealService.update_hotlist(page_index)
        except Exception as e:
            return { 'data': {}, 'code': 500, 'msg': e }
        else:
            return { 'data': resData, 'code': 200, 'msg': 'success' }
        
