import re
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup


class crawl(object):


    def search_video(search_name, pages):
        bvid_lst = []  # bv号表
        up_lst = []  # up主表
        for page in range(1, pages):
            url = ('http://search.bilibili.com/all?keyword=' + search_name +
                   '&single_column=0&&order=click&page=' + str(page))
            req = requests.get(url)
            content = req.text
            pattern = re.compile('<a href="//www.bilibili.com/video/(.*?)\?from=search" title=')
            pattern_up = re.compile('<a href="//space.bilibili.com/.*?class="up-name">(.*?)</a></span>')
            lst_add = pattern.findall(content)
            up_lst_add = pattern_up.findall(content)
            time.sleep(1)
            print('第{}页'.format(page), lst_add)
            up_lst.extend(up_lst_add)
            bvid_lst.extend(lst_add)
        return bvid_lst, up_lst

    def get_base_info(bvid):
        s = requests.get('https://api.bilibili.com/x/web-interface/archive/stat?bvid=%s' % bvid, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/80.0.3987.149 Safari/537.36 '
        }
                         )
        try:
            base_info = s.json()['data']
            # print('播放量：{}\n弹幕数量：{}\n收藏数量：{}\n硬币数量：{}\n分享数量：{}\n点赞数量：{}\n-----\n评论数量：{}'.format(
            #     base_info['view'], base_info['danmaku'], base_info['favorite'], base_info['coin'], base_info['share'],
            #     base_info['like'], base_info['reply']))
        except:
            print('Error')
        return base_info

    def get_title_time_tag(bvid, idx):
        tag_lst = []    #tag表
        url = 'https://www.bilibili.com/video/%s' % bvid
        content = requests.get(url).content
        soup = BeautifulSoup(content, 'html.parser')
        tags = soup.find_all('a', class_='tag-link')
        title_lst = soup.find_all('title')
        print(title_lst[0].text.split('_')[0])
        title = title_lst[0].text.split('_')[0] #标题
        time_lst = soup.find_all(itemprop='uploadDate')
        time = time_lst[0]['content'].split(' ')[0]
        for tag in tags:
            tag_lst.append(tag.text.strip())
        return title, time, set(tag_lst)


if __name__ == '__main__':
    search_name = input('Please input the keyword:')
    num = int(input('Please input the pages:'))
    bvid_lst, up_lst = crawl.search_video(search_name, pages=(num + 1))
    df_result = pd.DataFrame()
    for idx, bvid in enumerate(bvid_lst):
        print('正在提取第{}个视频的信息，BV号为：{}'.format(idx + 1, bvid))
        title, ttime, tag_lst = crawl.get_title_time_tag(bvid, idx)
        base_info = crawl.get_base_info(bvid)
        df_result = df_result.append({'bvid': bvid, '标题': title, '日期': ttime, '作者': up_lst[idx],
                                      '标签': tag_lst,
                                      '播放量': base_info['view'], '弹幕数量': base_info['danmaku'],
                                      '点赞量': base_info['like'], '收藏量': base_info['favorite'],
                                      '分享次数': base_info['share'], '投币数': base_info['coin'],
                                      '评论数量': base_info['reply']}, ignore_index=True)

        time.sleep(1)
    df_result.to_csv('{}_count{}.csv'.format(search_name, num*20), index=False)
    print('有%d项结果' % (idx + 1))
