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
        book_msg_list = None
        msg = ''
        code = 0
        data = None
        if not page_index:
            page_index = 0
        try:
            book_msg_list = PageDealService.get_book_msg(page_index)
        except Exception as e:
            print(e)
            code = 500
            msg = e
            data = None
        else:
            code = 200
            msg = 'success'
            data = book_msg_list
        res = {
            'code': code,
            'msg': msg,
            'data': data
        }
        return res
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