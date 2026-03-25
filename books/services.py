import random
import json

import requests
from bs4 import BeautifulSoup
from .tools import extract_text
from .curd_controllers import AuthorCURDController, BookCURDController, EpisodeCURDController
from books.models import Book, Episode
from books.serializers import BookSerializer, EpisodeSerializer
import time, os, copy
from django.db.models import Q

class BaseService:
    # @classmethod
    # def get_soup(self, url):
    #     res = requests.get(url)
    #     con = res.content.decode('utf-8')
    #     soup = BeautifulSoup(con, 'html.parser')
    #     return soup

    @classmethod
    def get_soup(cls, url):
        session = requests.Session()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept-Language": "ja-JP,ja;q=0.9,en;q=0.8",
            "Referer": "https://kakuyomu.jp/",
        }

        # 先访问首页拿 cookie
        session.get("https://kakuyomu.jp/", headers=headers)
        time.sleep(random.uniform(1, 3))

        res = session.get(url, headers=headers)

        return BeautifulSoup(res.text, "html.parser")
    


# 列表接口
class UpdateService(BaseService):
    # 进表操作
    @classmethod
    def update_hotlist(cls, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/tags/%E7%99%BE%E5%90%88?page={}".format(page_index))
        # soup = cls.get_soup("https://kakuyomu.jp/")
        # 大模块
        moudle_list = soup.find_all('div', class_='widget-work float-parent')
        print(f'看看长度============>{len(moudle_list)}')
        for index, moudle in enumerate(moudle_list):
            # left_moudle = len(moudle.select('.float-left')) ? moudle.select('.float-left')[0] : None
            left_moudle = None if not len(moudle.select('.float-left')) else moudle.select('.float-left')[0]
            # print(left_moudle)
            if left_moudle:
                book_title = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title').text

                author_name = left_moudle.find('a', class_='widget-workCard-authorLabel').text

                author_href = left_moudle.find('a', class_='widget-workCard-authorLabel')['href']
                
                book_desc = left_moudle.select('.widget-workCard-introduction a')[0].text if left_moudle.select('.widget-workCard-introduction a') else '無'

                book_href = left_moudle.find('a', class_='widget-workCard-titleLabel bookWalker-work-title')['href']

                author_id = author_href.split('/')[-1]
                
                book_id = book_href.split('/')[-1]

                hot_rank = index + 1

                last_time = left_moudle.select('.widget-workCard-dateUpdated')[0].text
                
                publish_state = left_moudle.select('.widget-workCard-statusLabel')[0].text
                number_of_episode = left_moudle.select('.widget-workCard-episodeCount')[0].text

                author_data = { 'author_id': author_id, 'author_name': author_name }
                print(f'author_data============>{author_data}')
                book_data = {
                    'book_id': book_id, 
                    'author_id': author_id, 
                    'book_title': book_title, 
                    'book_desc': book_desc, 
                    'hot_rank': hot_rank,
                    'last_time': last_time,
                    'full_desc': book_desc,
                    'number_of_episode': number_of_episode, 
                    'publish_state': 0 if publish_state == '完結済' else 1
                }
                print(f'book_data============>{book_data}')
                try:
                    
                    # 避免短期内大量访问
                    # time.sleep(5)
                    # 进表前先把之前的rank清空避免重复
                    target_list = Book.objects.filter(Q(hot_rank__gt=0) & Q(hot_rank__lt=51))
                    target_list.update(hot_rank=999)
                    AuthorCURDController().update_author(author_data)
                    # 先不爬章节，页面结构变了，得从__NEXT_DATA__里面爬
                    # cls.update_detail(book_data)
                    BookCURDController().create_book(book_data)
                except Exception as e:
                    print(f'ERROR================>{e}')
                    return f'update faild!{e}'
        return 'update success!'
    
    # 进表操作
    @classmethod
    def update_detail(cls, book_data):
        print(f'进来了,看看data========>{book_data}')
        # print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/works/{}".format(book_data['book_id']))

        
        data = soup.find("script", id="__NEXT_DATA__").string
        json_data = json.loads(data)

        print(f'json_data=============>{json_data}')
        
        # print('看看soup============>', soup)
        # state number
        # [publish_state, number_of_episode] = soup.select('.widget-workCard-status span')
        # publish_state = soup.select('.Meta_metaItem__8eZTP')
        # dataPack = soup.find_all('div', class_='Meta_metaItem__8eZTP')
        # print(f'看看publish_state============>{dataPack[1]}')
        # print(f'看看number_of_episode============>{number_of_episode}')
        # last refresh time
        # last_time = soup.select('.widget-toc-date time span')[0]
        # print(f'看看last_time============>{last_time}')
        # full_desc
        # full_desc = soup.select('#introduction')[0].text.replace('…続きを読む', "")
        # print(f'看看full_desc============>{full_desc}')


        # epi_data = soup.find_all('div', class_='NewBox_box__45ont NewBox_padding-px-m__OQCYI')

        # package_data = {}
        # for index, epi in enumerate(epi_data):
        #     main_title = epi.find('h3', class_='Heading_heading__lQ85n Heading_left__RVp4h Heading_size-1s___G7AX').text
        #     chaptepi = epi.find_all('a', class_='WorkTocSection_link__ocg9K')
        #     for dataindex, data in enumerate(chaptepi):
        #         print(f'看看index==============>', dataindex)
        #         try:
        #             package_data = {
        #                 'episode_id': data['href'].split('/')[-1],
        #                 'book_id': book_data['book_id'],
        #                 'main_title': main_title,
        #                 'sub_title': data.select_one("div.WorkTocSection_title__H2007").get_text(strip=True),
        #                 'refresh_time': data.find('time').text,
        #                 'isupdated': 0,
        #                 'server_address': '',
        #             }
        #             print(f'看看episode_data==============>', package_data)
        #         except Exception as e:
        #             print(f'ERROR================>{e}')
        #             return f'update faild!{e}'

            
        #     print(f'看看index==============>', index)



        # print(f'看看epi_data============>{epi_data}')

        # episode data
        # book_data.update({
        #     'last_time': last_time.text,
        #     'full_desc': full_desc,
        #     'number_of_episode': number_of_episode.text, 
        #     'publish_state': 0 if publish_state.text == '完結済' else 1
        # })
        # BookCURDController().update_book(book_data)
        
        # cls.update_epilist(epi_data, book_id)

    # 进表操作
    @classmethod
    def refresh_episode(cls, book_id):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/works/{}".format(book_id))
        # state number
        [publish_state, number_of_episode] = soup.select('.widget-toc-workStatus span')
        # last refresh time
        last_time = soup.select('.widget-toc-date time span')[0]
        # full_desc
        full_desc = soup.select('#introduction')[0].text.replace('…続きを読む', "")
        epi_data = soup.select('.widget-toc-items.test-toc-items li')
        book_obj = {}
        # pdb.set_trace()
        exists_flag = Book.objects.filter(book_id=book_id).exists()
        if exists_flag:
            book_obj = Book.objects.get(book_id=book_id)
        
        if book_obj and book_obj.last_time != last_time.text:
            BookCURDController().update_book({
                'book_id': book_id, 
                'author_id': book_obj.author_id,
                'last_time': last_time.text,
                'full_desc': full_desc,
                'number_of_episode': number_of_episode.text, 
                'publish_state': 0 if publish_state.text == '完結済' else 1
            })
            cls.update_epilist(epi_data, book_id)
            return { 'msg': 'upload success' }
        else:
            return {'msg': 'is most fresh data'}

    @classmethod
    def update_epilist(self, episode_list, book_id):
        current_maintitle = ' '
        for index, item in enumerate(episode_list):
            #   if 是章节
            #       cm = 章节名
            #   else 
            #       if index = 0
            #           cm = ' '
            #       ~~~逻辑处理
            if 'widget-toc-chapter' in item.attrs['class']:
                current_maintitle = item.find('span').text
            else:
                if index == 0:
                    current_maintitle = ' '
                # pdb.set_trace()
                episode_id = item.find('a')['href'].split('/')[-1]
                # 这里插入比较的逻辑
                episode_obj = {}
                exists_flag = Episode.objects.filter(episode_id=episode_id).exists()
                if exists_flag:
                    episode_obj = Episode.objects.get(episode_id=episode_id)
                episode_data = {}
                if episode_obj:
                    if episode_obj.refresh_time != item.find('time').text:
                        episode_obj.isupdated = 1,
                        episode_obj.refresh_time = item.find('time').text,
                        episode_obj.save()
                else:
                    episode_data = {
                        'episode_id': episode_id,
                        'book_id': book_id,
                        'main_title': current_maintitle,
                        'sub_title': item.find('span').text,
                        'refresh_time': item.find('time').text,
                        'isupdated': 0,
                        'server_address': '',
                    }
                    EpisodeCURDController().update_episode(episode_data)
                
    
# /works/16816700429263197780/episodes/16817330656452046849
# 下载接口
class EpisodeService(BaseService):
    @classmethod
    def set_file(cls, book_id, episode_id):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/works/{0}/episodes/{1}".format(book_id, episode_id))
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
        file_addr = episode_obj.server_address
        file_name = '{0}-{1}'.format(episode_obj.main_title, episode_obj.sub_title)
        print(f'file_addr====>{file_addr}')
        if not file_addr or episode_obj.isupdated == 1:
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
    
    @classmethod
    def get_episode_text(cls, book_id, episode_id):
        # 先根据服务器地址查文件，如果没有再创建文件(并缓存至缓存地址改名)然后抛出服务器地址
        # 缓存地址一天一清理(打包再用)
        episode_obj = Episode.objects.get(episode_id=episode_id)
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

        file_content = ''
        try:
            with open(file_addr, 'r', encoding='utf-8') as file:
                file_content = file.read()
        except FileNotFoundError as e:
            file_content = ''

        return { 'file_content': file_content, 'file_name': file_name}
    
class SearchService(BaseService):
    # 搜索列表
    @classmethod
    def get_searched_list(cls, search_name, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/search?q={0}&page={1}".format(search_name, page_index))
        moudle_list = soup.find_all('div', class_='Gap_size-2s__r5pBU Gap_direction-y__ELoPO')
        result = []
        for index, moudle in enumerate(moudle_list):
            book_moudle = moudle.select('.Gap_size-4s__P2EWr.Gap_direction-x__3b2TF a')
            if not len(book_moudle):
                continue
            book_title = book_moudle[0]['title']
            book_href = book_moudle[0]['href']
            author_moudle = moudle.select('.partialGiftWidgetActivityName.ActivityName_inlineBlock__TBG1H a')[0]
            author_name = author_moudle.text
            author_href = author_moudle['href']
            book_desc = moudle.select('.partialGiftWidgetWeakText span')[0].text
            author_id = author_href.split('/')[-1]
            book_id = book_href.split('/')[-1]
            hot_rank = 999
            [publish_state, number_of_episode] = moudle.select('.Meta_lineHeightSmall__fM62M li:nth-child(3) .Meta_metaItem__c_ZZh')[0].text.split(' ')
            last_time = moudle.select('.Meta_lineHeightSmall__fM62M li:nth-child(5) .Meta_metaItem__c_ZZh time')[0].text
            author_data = { 'author_id': author_id, 'author_name': author_name }
            book_data = {
                'author': author_data,
                'book_desc': book_desc,
                'book_id': book_id,
                'book_title': book_title,
                'hot_rank': hot_rank,
                'last_time': last_time,
                'number_of_episode': number_of_episode,
                'publish_state': 0 if publish_state == '完結済' else 1
            }
            result.append(book_data)
        return result
        
    # 搜索列表点进特定book的详情，入库
    @classmethod
    def get_searched_book(cls, book_data):
        copy_data = copy.deepcopy(book_data)
        book_id = copy_data.get('book_id')
        author_data = copy_data.pop('author')
        if author_data:
            AuthorCURDController().update_author(author_data)
        copy_data.update({
            'author_id': author_data.get('author_id')
        })

        
        book_target = Book.objects.filter(book_id=book_id)
        if not book_target:
            UpdateService.update_detail(book_id, copy_data)
        # Episode.objects.get(book=book_id)
        # episode_list = Episode.objects.filter(book=book_id)
        # serializer = EpisodeSerializer(episode_list, many=True)
        # book_target = Book.objects.get(book_id=book_id)
        # pdb.set_trace()
        # copy_data.update({
        #     'full_desc': book_target[0].full_desc,
        #     'author': author_data
        # })
        return { 'msg': 'success' }
