# 定时刷新分集列表
import datetime
import os
import time
import realpath

import psutil as psutil

from models.auto_down_anime import model
from helpers.auto_down_anime import episode
from lib import downloader

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
            start()
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)
        time.sleep(600)
