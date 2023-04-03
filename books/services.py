import requests
from bs4 import BeautifulSoup
class BaseService:
    @classmethod
    def get_soup(self, url):
        res = requests.get(url)
        con = res.content.decode('utf-8')
        soup = BeautifulSoup(con, 'html.parser')
        return soup
    

class GetPageDetailService(BaseService):
    @classmethod
    def get_page_detail(cls, page_href):
        soup = cls().get_soup("https://kakuyomu.jp{}".format(page_href))
        # author name
        author_name = soup.select('#workAuthor-activityName a')[0]
        # state number
        [number_of_episode, publish_state] = soup.select('.widget-toc-workStatus span')
        # last refresh time
        last_time = soup.select('.widget-toc-date time span')[0]
        # episode data
        epi_data = soup.select('.widget-toc-items.test-toc-items li')
        epi_list = cls().get_epilist(epi_data)
        return {
            'author_name': author_name.text,
            'number_of_episode': number_of_episode.text,
            'publish_state': publish_state.text,
            'last_time': last_time.text,
            'episode_data': epi_list,
        }


    def get_epilist(self, lst):
        result = {}
        current_key = None
        for index, item in enumerate(lst):
            if 'widget-toc-chapter' in item.attrs['class']:
                current_key = index
                result[current_key] = {
                    'mian_title': item.find('span').text,
                    'episode_list': []
                }
            elif current_key is not None:
                result[current_key]['episode_list'].append({
                    'episode_title': item.find('span').text,
                    'refresh_time': item.find('time').text,
                    'href': item.find('a')['href']
                })
        return [value for _, value in result.items()]


# GetPageDetailService.get_page_detail('/works/1177354054894027232')

class PageDealService(BaseService):
    @classmethod
    def get_book_msg(cls, page_index):
        soup = cls().get_soup("https://kakuyomu.jp/tags/%E7%99%BE%E5%90%88?page={}".format(page_index))
        # 大模块
        moudle_list = soup.find_all('div', class_='widget-work float-parent')
        book_list = []
        for moudle in moudle_list:
            book_title = ''
            boot_auther = ''
            book_desc = ''
            book_href = ''
            # left_moudle = len(moudle.select('.float-left')) ? moudle.select('.float-left')[0] : None
            left_moudle = None if not len(moudle.select('.float-left')) else moudle.select('.float-left')[0]
            # print(left_moudle)
            if left_moudle:
                book_title = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title').text
                boot_auther = left_moudle.find('a', class_='widget-workCard-authorLabel').text
                book_desc = left_moudle.select('.widget-workCard-introduction a')[0].text
                book_href = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title')['href']
                boot_dist = {
                    'book_title': book_title,
                    'boot_auther': boot_auther,
                    'book_desc': book_desc,
                    'book_href': book_href 
                }
                book_list.append(boot_dist)
        return book_list