# 定时刷新连载中番剧的评分和连载状态
import datetime
import json
import os
import time
import realpath

import psutil as psutil

from models.auto_down_anime import model
from helpers.auto_down_anime import setting
from lib import tools
from cPython import cPython as cp

tb_episode = model.EpisodeList()
tb_anime = model.AnimeList()


def write_pid():
    pid = os.getpid()
    fp = open("auto_ref_anime_end.log", 'w')
    fp.write(str(pid))
    fp.close()


def read_pid():
    if os.path.exists("auto_ref_anime_end.log"):
        fp = open("auto_ref_anime_end.log", 'r')
        pid = fp.read()
        fp.close()
        return pid
    else:
        return False


def start():
    for f in tb_anime.find({'end': {'$ne': True}}):
        try:
            data = json.loads(
                cp.get_html_for_requests('https://api.bilibili.com/pgc/review/user?media_id=%s' % f.get('media_id', ''),
                                         headers=tools.gen_http_header()))
            U = {'end': data['result']['media']['new_ep']['index_show'].startswith('全')}
            try:
                U['rating_count'] = data['result']['media']['rating']['count']
            except Exception as e:
                U['rating_count'] = 0

            try:
                U['rating_score'] = data['result']['media']['rating']['score']
            except Exception as e:
                U['rating_count'] = 0
            tb_anime.update({'_id': f['_id']}, {'$set': U})
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), '更新%s > %s, end: %s' % (f['_id'], f['title'], U))
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)


if __name__ == '__main__':
    pid = read_pid()
    if pid:
        running_pid = psutil.pids()
        if int(pid) in running_pid:
            exit(0)
    write_pid()

    print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), 'auto refresh anime end info running...')
    while True:
        try:
            _ = tools.get_bilibili_username()
            if _.startswith('登录失效, ') and\
                    (datetime.datetime.now() - setting.get().get('cookie_disabled_last_send_time', datetime.datetime(2000, 1, 1))).days >= 1:
                tools.send_server_jiang_msg('自动番剧下载 - 登录失效', 'cookie已经失效, 请尽快重新设置以免影响下载和分集下载质量, %s' % _)
                setting.tb_setting.update({}, {'$set': {
                    'cookie_disabled_last_send_time': datetime.datetime.now()
                }})
            start()
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)
        time.sleep(86400)