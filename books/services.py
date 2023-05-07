import requests
from bs4 import BeautifulSoup
from .tools import extract_text
from .curd_controllers import AuthorCURDController, BookCURDController, EpisodeCURDController
from books.models import Author, Book, Episode
import time, os, json
class BaseService:
    @classmethod
    def get_soup(self, url):
        res = requests.get(url)
        con = res.content.decode('utf-8')
        soup = BeautifulSoup(con, 'html.parser')
        return soup
    



# GetPageDetailService.get_page_detail('/works/1177354054894027232')
# 列表接口
class PageDealService(BaseService):
    @classmethod
    def get_book_msg(cls, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
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
                author_href = left_moudle.find('a', class_='widget-workCard-authorLabel')['href']
                book_desc = left_moudle.select('.widget-workCard-introduction a')[0].text
                book_href = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title')['href']
                boot_dist = {
                    'book_title': book_title,
                    'boot_auther': boot_auther,
                    'author_href': author_href,
                    'book_desc': book_desc,
                    'book_href': book_href 
                }
                book_list.append(boot_dist)
        return book_list
    
    # 进表操作
    @classmethod
    def update_hotlist(cls, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls().get_soup("https://kakuyomu.jp/tags/%E7%99%BE%E5%90%88?page={}".format(page_index))
        # 大模块
        moudle_list = soup.find_all('div', class_='widget-work float-parent')
        for index, moudle in enumerate(moudle_list):
            # left_moudle = len(moudle.select('.float-left')) ? moudle.select('.float-left')[0] : None
            left_moudle = None if not len(moudle.select('.float-left')) else moudle.select('.float-left')[0]
            # print(left_moudle)
            if left_moudle:
                book_title = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title').text
                author_name = left_moudle.find('a', class_='widget-workCard-authorLabel').text
                author_href = left_moudle.find('a', class_='widget-workCard-authorLabel')['href']
                book_desc = left_moudle.select('.widget-workCard-introduction a')[0].text
                book_href = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title')['href']
                author_id = author_href.split('/')[-1]
                book_id = book_href.split('/')[-1]
                hot_rank = index + 1
                author_data = { 'author_id': author_id, 'author_name': author_name }
                print(f'author_data============>{author_data}')
                book_data = { 'book_id': book_id, 'author_id': author_id, 'book_title': book_title, 'book_desc': book_desc, 'hot_rank': hot_rank }
                print(f'book_data============>{book_data}')
                try:
                    time.sleep(5)
                    AuthorCURDController().update_author(author_data)
                    GetPageDetailService.update_detail(book_href, book_data)
                    # BookCURDController().create_book(book_data)
                except Exception as e:
                    print(f'ERROR================>{e}')
                    return f'update faild!{e}'
        return 'update success!'
                
    
# 详情接口
class GetPageDetailService(BaseService):
    @classmethod
    def get_page_detail(cls, page_href):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls().get_soup("https://kakuyomu.jp{}".format(page_href))
        # author name
        author_name = soup.select('#workAuthor-activityName a')[0]
        # state number
        [publish_state, number_of_episode] = soup.select('.widget-toc-workStatus span')
        # last refresh time
        last_time = soup.select('.widget-toc-date time span')[0]
        # full_desc
        full_desc = soup.select('#introduction')[0].text.replace('…続きを読む', "")
        # episode data
        epi_data = soup.select('.widget-toc-items.test-toc-items li')
        epi_list = cls().get_epilist(epi_data)
        return {
            'author_name': author_name.text,
            'number_of_episode': number_of_episode.text,
            'publish_state': publish_state.text,
            'last_time': last_time.text,
            'full_desc': full_desc,
            'episode_data': epi_list,
        }

    # 进表操作
    @classmethod
    def update_detail(cls, page_href, book_data):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls().get_soup("https://kakuyomu.jp{}".format(page_href))
        # state number
        [publish_state, number_of_episode] = soup.select('.widget-toc-workStatus span')
        # last refresh time
        last_time = soup.select('.widget-toc-date time span')[0]
        # full_desc
        full_desc = soup.select('#introduction')[0].text.replace('…続きを読む', "")
        # episode data
        book_data.update({
            'last_time': last_time.text,
            'full_desc': full_desc,
            'number_of_episode': number_of_episode.text, 
            'publish_state': 0 if publish_state.text == '完結済' else 1
        })
        BookCURDController().update_book(book_data)

        epi_data = soup.select('.widget-toc-items.test-toc-items li')
        cls().update_epilist(epi_data, book_data['book_id'])

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
    
    def update_epilist(self, lst, book_id):
        current_maintitle = None
        for _, item in enumerate(lst):
            if 'widget-toc-chapter' in item.attrs['class']:
                current_maintitle = item.find('span').text
            elif current_maintitle is not None:
                episode_id = item.find('a')['href'].split('/')[-1]
                episode_data = {
                    'episode_id': episode_id,
                    'book_id': book_id,
                    'main_title': current_maintitle,
                    'sub_title': item.find('span').text,
                    'refresh_time': item.find('time').text,
                    'isupdated': 1,
                    'server_address': '',
                }
                EpisodeCURDController().update_episode(episode_data)
    
    
# /works/16816700429263197780/episodes/16817330656452046849
# 下载接口
class GetEpisodeTextService(BaseService):
    @classmethod
    def set_file(cls, book_id, episode_id):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls().get_soup("https://kakuyomu.jp/works/{0}/episodes/{1}".format(book_id, episode_id))
        text_content = extract_text.trans_text(soup)
        storage_path = os.getenv('STORAGE_PATH')
        # 创建持久层储存地址
        dir_addr = extract_text.find_dir(name=book_id, path=storage_path)
        # 存文件
        file_addr = extract_text.set_file(text=text_content, file_addr='{0}/{1}.txt'.format(dir_addr, episode_id))
        return file_addr
        
    @classmethod
    def get_episode_file(cls, book_id, episode_id):
        # 先根据服务器地址查文件，如果没有再创建文件(并缓存至缓存地址改名)然后抛出服务器地址
        # 缓存地址一天一清理(打包再用)
        episode_obj = Episode.objects.get(episode_id=episode_id)
        print(f'episode_obj====>{episode_obj}')
        file_addr = episode_obj.server_address
        file_name = '{0}-{1}'.format(episode_obj.main_title, episode_obj.sub_title)
        print(f'file_addr====>{file_addr}')
        if not file_addr:
            # 存文件
            file_addr = cls.set_file(book_id, episode_id)
            if file_addr:
                episode_obj.server_address = file_addr
                episode_obj.save()
                print(f'episode_obj====>{episode_obj}')
            else:
                print(f'episode_obj====>{episode_obj}')
            # 创建缓存区地址(留着给打包用吧，单个文件不用)
            # extract_text.find_dir(name=os.path.join(book_id, episode_id), path=storage_path)
        elif os.path.isfile(file_addr):
            # 如果有文件在，直接抛了读
            print(f'strength throung episode_obj====>{episode_obj}')
        else:
            file_addr = cls.set_file(book_id, episode_id)

        return { 'file_addr': file_addr, 'file_name': file_name}

    
# /works/1177354054893434437/episodes/1177354054893434453
# 章节接口，废弃不用
class GetEpisodeListService(BaseService):
    @classmethod
    def get_episode_list(self, book_id, cls):
        # book = Book.objects.get(book_id=book_id)
        episode_list = Episode.objects.filter(book_id__book_id=book_id)
        
        page = cls.paginate_queryset(episode_list)
        if page is not None:
            serializer = cls.get_serializer(page, many=True)

        serializer = cls.get_serializer(episode_list, many=True)
        
        res = json.dumps(serializer.data, ensure_ascii=False)
        print(type(json.loads(res)))
        return json.loads(res)