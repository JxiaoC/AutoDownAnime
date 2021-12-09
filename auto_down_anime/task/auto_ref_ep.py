# 定时刷新分集列表
import datetime
import os
import time
import realpath

import psutil as psutil

from models.auto_down_anime import model
from helpers.auto_down_anime import episode, setting
from lib import tools

tb_episode = model.EpisodeList()
tb_anime = model.AnimeList()


def write_pid():
    pid = os.getpid()
    fp = open("auto_ref_ep.log", 'w')
    fp.write(str(pid))
    fp.close()


def read_pid():
    if os.path.exists("auto_ref_ep.log"):
        fp = open("auto_ref_ep.log", 'r')
        pid = fp.read()
        fp.close()
        return pid
    else:
        return False


def start():
    for f in tb_anime.find({'end': {'$ne': True}}):
        try:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), '更新%s > %s' % (f['_id'], f['title']))
            episode.ref_episode_data(f.get('season_id', 0))
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)


if __name__ == '__main__':
    pid = read_pid()
    if pid:
        running_pid = psutil.pids()
        if int(pid) in running_pid:
            exit(0)
    write_pid()

    print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), 'auto refresh episode info running...')
    while True:
        try:
            if tools.get_bilibili_username() == '登录失效, 请重新替换cookie' and\
                    (datetime.datetime.now() - setting.get().get('cookie_disabled_last_send_time', datetime.datetime(2000, 1, 1))).days >= 1:
                tools.send_server_jiang_msg('自动番剧下载 - 登录失效', 'cookie已经失效, 请尽快重新设置以免影响下载和分集下载质量')
                setting.tb_setting.update({}, {'$set': {
                    'cookie_disabled_last_send_time': datetime.datetime.now()
                }})
            start()
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)
        time.sleep(600)
