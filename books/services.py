import random
import json
import threading

import requests
from bs4 import BeautifulSoup
from .tools import extract_text
from .curd_controllers import AuthorCURDController, BookCURDController, EpisodeCURDController
from books.models import Book, Episode
from books.serializers import BookSerializer, EpisodeSerializer
import time, os, copy
from django.db.models import Q
from datetime import datetime

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
        time.sleep(random.uniform(2, 5))

        res = session.get(url, headers=headers)

        return BeautifulSoup(res.text, "html.parser")
    


# 列表接口
class UpdateService(BaseService):
    # 进表操作
    @classmethod
    def update_hotlist(cls, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/tags/怪談?page={}".format(page_index))
        # soup = cls.get_soup("https://kakuyomu.jp/search?genre_name=horror?page={}".format(page_index))
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
                    time.sleep(random.uniform(5, 10))
                    # 进表前先把之前的rank清空避免重复
                    target_list = Book.objects.filter(Q(hot_rank__gt=0) & Q(hot_rank__lt=51))
                    target_list.update(hot_rank=999)

                    AuthorCURDController().update_author(author_data)
                    print(f'author update================>{author_name}')


                    # return;
                    BookCURDController().update_book(book_data)
                    print(f'book update================>{book_title}')
                    # return;
                    # 先不爬章节，页面结构变了，得从__NEXT_DATA__里面爬，为了避免防爬，在点进页面之后再爬
                    cls.update_detail(book_data['book_id'])
                    print(f'{book_title}的章节更新================>success')

                except Exception as e:
                    print(f'ERROR================>{e}')
                    return f'update faild!{e}'
        return 'update success!'
    
    # 进表操作 根据book_id获取章节列表并存表且更新，记得先查询一下章节表里有没有这个book的章节，避免重复爬取
    # 哎，不对，设计层面就有问题了，应该再book上添加是否有更新的标记，每次只用爬book那一层就行，再判断。
    # 时间不够了，先把这个方法的接口开出来，每次进页面就查一下，以后再说
    # 改为传id，自己查，能进来的肯定都有id且有对应book
    @classmethod
    def update_detail(cls, book_id):
        try:
            # print(f'进来了,看看data========>{book_data}')
            # print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # 用book_id查到该book下episode是否存在，如果存在就直接return
            is_episode_exists = Episode.objects.filter(book_id=book_id).exists()
            print(f'{book_id}============>章节数据是否已存在: {is_episode_exists}')
            if is_episode_exists:
                print(f'{book_id}============>章节数据已存在，无需更新')
                return

            book_obj = Book.objects.get(book_id=book_id)
            print(f'{book_obj.book_title}============>开始更新章节数据')
            soup = cls.get_soup("https://kakuyomu.jp/works/{}".format(book_id))
            # soup = cls.get_soup("https://kakuyomu.jp/works/{}".format('16818093079992812465'))
            print(f'{book_obj.book_title}============>开始更新')
            
            data = soup.find("script", id="__NEXT_DATA__").string
            json_data = json.loads(data)
            page_data = json_data.get('props', {}).get('pageProps', {}).get('__APOLLO_STATE__', {})
            # print(f'page_data============>{page_data}')
            full_desc = page_data.get('Work:{}'.format(book_id), {}).get('introduction', '')
            # full_desc = page_data.get('Work:{}'.format('16818093079992812465'), {}).get('introduction', '')
            print(f'full_desc============>{full_desc}')
            for key, value in page_data.items():
                if key.startswith('TableOfContentsChapter:'):
                    print(f'进循环了============>{value}')
                    search_chapter_key = value.get('chapter').get('__ref') if value.get('chapter') else 999
                    print(f'chapter_key============>{search_chapter_key}')
                    main_title = page_data.get(search_chapter_key).get('title') if search_chapter_key != 999 else 'blank'
                    print(f'main_title============>{main_title}')
                    for episode_v in value.get('episodeUnions', []):
                        data_key = episode_v.get('__ref')
                        print(f'data_key============>{data_key}')
                        time_str = page_data.get(data_key).get('publishedAt')
                        print(f'time_str============>{time_str}')
                        try:
                            dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
                        except Exception:
                            dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
                        # print(f'dt============>{dt}')
                        # print(f'refresh_time============>{f"{dt.year}年{dt.month}月{dt.day}日 {dt.hour:02d}:{dt.minute:02d}"}')
                        episode_item = {
                            'episode_id': page_data.get(data_key).get('id'),
                            'book_id': book_id,
                            # 'book_id': '16818093079992812465',
                            'main_title': main_title,
                            'chapter_key': value.get('id') if value.get('id') else page_data.get(data_key).get('id'),
                            'sub_title': page_data.get(data_key).get('title'),
                            'refresh_time': f"{dt.year}年{dt.month}月{dt.day}日 {dt.hour:02d}:{dt.minute:02d}",
                            'isupdated': 0,
                            'server_address': '',
                            'is_crawling': 0,
                        }
                        cls.update_epilist(episode_item, book_id)
                        # cls.update_epilist(episode_item, '16818093079992812465')

            print(f'{book_obj.book_title}============>的章节数据更新完了')

            book_obj.full_desc = full_desc
            book_obj.save()
            # episode data
            # book_obj.update({
            #     'last_time': last_time.text,
            #     'full_desc': full_desc
            #     'number_of_episode': number_of_episode.text, 
            #     'publish_state': 0 if publish_state.text == '完結済' else 1
            # })
            # BookCURDController().update_book(book_data)
        except Exception as e:
            print(f'Error occurred while updating book and episodes=====================>: {e}')

    # 进表操作 逻辑有问题 需要重更新写，功能应该是点击按钮后手动刷新
    @classmethod
    def refresh_episode(cls, book_id):
        return
        # print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # soup = cls.get_soup("https://kakuyomu.jp/works/{}".format(book_id))
        # # state number
        # [publish_state, number_of_episode] = soup.select('.widget-toc-workStatus span')
        # # last refresh time
        # last_time = soup.select('.widget-toc-date time span')[0]
        # # full_desc
        # full_desc = soup.select('#introduction')[0].text.replace('…続きを読む', "")
        # epi_data = soup.select('.widget-toc-items.test-toc-items li')
        # book_obj = {}
        # # pdb.set_trace()
        # exists_flag = Book.objects.filter(book_id=book_id).exists()
        # if exists_flag:
        #     book_obj = Book.objects.get(book_id=book_id)
        
        # if book_obj and book_obj.last_time != last_time.text:
        #     BookCURDController().update_book({
        #         'book_id': book_id, 
        #         'author_id': book_obj.author_id,
        #         'last_time': last_time.text,
        #         'full_desc': full_desc,
        #         'number_of_episode': number_of_episode.text, 
        #         'publish_state': 0 if publish_state.text == '完結済' else 1
        #     })
        #     cls.update_epilist(epi_data, book_id)
        #     return { 'msg': 'upload success' }
        # else:
        #     return {'msg': 'is most fresh data'}

    #重写更新章节列表的逻辑，之前是根据页面结构爬的，现在改成根据__NEXT_DATA__爬了，之前的逻辑就注释掉了
    @classmethod
    def update_epilist(cls, episode_item, book_id):
        episode_obj = {}
        exists_flag = Episode.objects.filter(episode_id=episode_item.get('episode_id')).exists()
        if exists_flag:
            episode_obj = Episode.objects.get(episode_id=episode_item.get('episode_id'))
        episode_data = {}
        if episode_obj:
            if episode_obj.refresh_time != episode_item.get('refresh_time'):
                episode_obj.isupdated = 1,
                episode_obj.refresh_time = episode_item.get('refresh_time'),
                episode_obj.save()
        else:
            episode_data = {
                'episode_id': episode_item.get('episode_id'),
                'book_id': book_id,
                'main_title': episode_item.get('main_title'),
                'chapter_key': episode_item.get('chapter_key'),
                'sub_title': episode_item.get('sub_title'),
                'refresh_time': episode_item.get('refresh_time'),
                'isupdated': 0,
                'server_address': '',
                'is_crawling': 0,
            }
            EpisodeCURDController().update_episode(episode_data)



    # @classmethod
    # def update_epilist(self, episode_list, book_id):
    #     current_maintitle = ' '
    #     for index, item in enumerate(episode_list):
    #         #   if 是章节
    #         #       cm = 章节名
    #         #   else 
    #         #       if index = 0
    #         #           cm = ' '
    #         #       ~~~逻辑处理
    #         if 'widget-toc-chapter' in item.attrs['class']:
    #             current_maintitle = item.find('span').text
    #         else:
    #             if index == 0:
    #                 current_maintitle = ' '
    #             # pdb.set_trace()
    #             episode_id = item.find('a')['href'].split('/')[-1]
    #             # 这里插入比较的逻辑
    #             episode_obj = {}
    #             exists_flag = Episode.objects.filter(episode_id=episode_id).exists()
    #             if exists_flag:
    #                 episode_obj = Episode.objects.get(episode_id=episode_id)
    #             episode_data = {}
    #             if episode_obj:
    #                 if episode_obj.refresh_time != item.find('time').text:
    #                     episode_obj.isupdated = 1,
    #                     episode_obj.refresh_time = item.find('time').text,
    #                     episode_obj.save()
    #             else:
    #                 episode_data = {
    #                     'episode_id': episode_id,
    #                     'book_id': book_id,
    #                     'main_title': current_maintitle,
    #                     'chapter_key': item.chapter_key, # 这里要重写
    #                     'sub_title': item.find('span').text,
    #                     'refresh_time': item.find('time').text,
    #                     'isupdated': 0,
    #                     'server_address': '',
    #                 }
    #                 EpisodeCURDController().update_episode(episode_data)
                
    
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
        episode_obj = Episode.objects.get(episode_id=episode_id)
        episode_obj.server_address = file_addr
        episode_obj.is_crawling = '2'
        episode_obj.save()
        
    # 纯返回地址，给前端轮询用
    @classmethod
    def get_episode_status(cls, episode_id):
        episode_obj = Episode.objects.get(episode_id=episode_id)
        print(f'episode_obj.book.book_id=========================>{episode_obj.book.book_id}')
        status = episode_obj.is_crawling
        print(f'status=========================>{status}')
        # 0-空的 1-正在爬 2-爬取完成
        if status == '0':
            # 没爬过，开始爬
            cls.get_episode_text(episode_obj.book.book_id, episode_id)
            return { 'status': 'processing' }
        elif status == '1':
            return { 'status': 'processing' }
        else:
            return { 'status': 'done' }
    
    # 纯开给下载文件用
    @classmethod
    def get_episode_addr(cls, episode_id):
        episode_obj = Episode.objects.get(episode_id=episode_id)
        file_addr = episode_obj.server_address
        print(f'file_addr====>{file_addr}')

        return { 'file_addr': file_addr, 'file_name': '{0}-{1}'.format(episode_obj.main_title, episode_obj.sub_title) }

    @classmethod
    def get_episode_text(cls, book_id, episode_id):
        # 先根据服务器地址查文件，如果没有再创建文件(并缓存至缓存地址改名)然后抛出服务器地址
        # 缓存地址一天一清理(打包再用)
        episode_obj = Episode.objects.get(episode_id=episode_id)
        print(f'episode_obj====>{episode_obj}')
        file_addr = episode_obj.server_address
        print(f'file_addr====>{file_addr}')
        file_name = '{0}-{1}'.format(episode_obj.main_title, episode_obj.sub_title)
        # 创建缓存区地址(留着给打包用吧，单个文件不用)
        # extract_text.find_dir(name=os.path.join(book_id, episode_id), path=storage_path)
        if episode_obj.is_crawling == '1':
            return { 'file_content': '', 'file_name': '', 'status': 'processing' }
        
        elif episode_obj.is_crawling == '2':
            file_addr = episode_obj.server_address
            file_content = ''
            try:
                with open(file_addr, 'r', encoding='utf-8') as file:
                    file_content = file.read()
            except FileNotFoundError as e:
                file_content = ''

            return { 'file_content': file_content, 'file_name': file_name, 'status': 'done' }
        

        # 没爬过，开始爬
        update = Episode.objects.filter(episode_id=episode_id, is_crawling='0').update(is_crawling='1')
        if update:
            # 存文件
            threading.Thread(
                target=cls.set_file,
                args=(book_id, episode_id)
            ).start()
            return { 'file_content': '', 'file_name': '', 'status': 'processing' }


class SearchService(BaseService):
    # 搜索列表
    @classmethod
    def get_searched_list(cls, search_name, page_index):
        print('caution!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        soup = cls.get_soup("https://kakuyomu.jp/search?q={0}&page={1}".format(search_name, page_index))
        moudle_list = soup.find_all('div', class_='Gap_size-2s__r5pBU Gap_direction-y__ELoPO')
        result = []
        data = soup.find("script", id="__NEXT_DATA__").string
        json_data = json.loads(data)
        page_data = json_data.get('props', {}).get('pageProps', {}).get('__APOLLO_STATE__', {})
        for key, value in page_data.items():
            if key.startswith('Work:'):
                book_id = value.get('id')
                book_title = value.get('title')
                book_desc = value.get('introduction', '無')
                author_id = value.get('author', {}).get('__ref', '').split(':')[-1]
                author_name = page_data.get(value.get('author', {}).get('__ref', ''), {}).get('activityName', '')
                hot_rank = 999
                last_time = value.get('lastEpisodePublishedAt', '')
                publish_state = value.get('serialStatus', '')
                number_of_episode = value.get('publicEpisodeCount', 0)
                author_data = { 'author_id': author_id, 'author_name': author_name }
                dt = datetime.strptime(last_time, "%Y-%m-%dT%H:%M:%SZ")
                book_data = {
                    'author': author_data,
                    'book_desc': book_desc,
                    'book_id': book_id,
                    'book_title': book_title,
                    'hot_rank': hot_rank,
                    'last_time': f"{dt.year}年{dt.month}月{dt.day}日 {dt.hour:02d}:{dt.minute:02d}",
                    'number_of_episode': number_of_episode,
                    'publish_state': 0 if publish_state == 'COMPLETED' else 1
                }
                result.append(book_data)
        # for index, moudle in enumerate(moudle_list):
        #     book_moudle = moudle.select('.Gap_size-4s__P2EWr.Gap_direction-x__3b2TF a')
        #     if not len(book_moudle):
        #         continue
        #     book_title = book_moudle[0]['title']
        #     book_href = book_moudle[0]['href']
        #     author_moudle = moudle.select('.partialGiftWidgetActivityName.ActivityName_inlineBlock__TBG1H a')[0]
        #     author_name = author_moudle.text
        #     author_href = author_moudle['href']
        #     book_desc = moudle.select('.partialGiftWidgetWeakText span')[0].text
        #     author_id = author_href.split('/')[-1]
        #     book_id = book_href.split('/')[-1]
        #     hot_rank = 999
        #     [publish_state, number_of_episode] = moudle.select('.Meta_lineHeightSmall__fM62M li:nth-child(3) .Meta_metaItem__c_ZZh')[0].text.split(' ')
        #     last_time = moudle.select('.Meta_lineHeightSmall__fM62M li:nth-child(5) .Meta_metaItem__c_ZZh time')[0].text
        #     author_data = { 'author_id': author_id, 'author_name': author_name }
        #     book_data = {
        #         'author': author_data,
        #         'book_desc': book_desc,
        #         'book_id': book_id,
        #         'book_title': book_title,
        #         'hot_rank': hot_rank,
        #         'last_time': last_time,
        #         'number_of_episode': number_of_episode,
        #         'publish_state': 0 if publish_state == '完結済' else 1
        #     }
        #     result.append(book_data)
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
        print(f'book_target============>{book_target}')
        if not book_target:
            # 先存书籍数据
            book_data = {
                'book_id': book_id, 
                'author_id': author_data.get('author_id'), 
                'book_title': copy_data.get('book_title'), 
                'book_desc': copy_data.get('book_desc'), 
                'hot_rank': copy_data.get('hot_rank'),
                'last_time': copy_data.get('last_time'),
                'full_desc': copy_data.get('book_desc'),
                'number_of_episode': copy_data.get('number_of_episode'), 
                'publish_state': copy_data.get('publish_state')
            }
            try:
                BookCURDController().update_book(book_data)
                UpdateService.update_detail(book_id)
                return { 'msg': 'success' }
            except Exception as e:
                print(f'Error occurred while updating book: {e}')
                return { 'msg': 'error' }
        else:
            try:
                UpdateService.update_detail(book_id)
                return { 'msg': 'success' }
            except Exception as e:
                print(f'Error occurred while updating book and episodes=====================>: {e}')
                return { 'msg': 'error' }

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
