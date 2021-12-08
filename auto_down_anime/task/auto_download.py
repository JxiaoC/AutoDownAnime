# 定时脚本
import datetime
import os
import time
import realpath

import psutil as psutil

from models.auto_down_anime import model
from lib import downloader

tb_episode = model.EpisodeList()
tb_anime = model.AnimeList()


def write_pid():
    pid = os.getpid()
    fp = open("auto_download_pid.log", 'w')
    fp.write(str(pid))
    fp.close()


def read_pid():
    if os.path.exists("auto_download_pid.log"):
        fp = open("auto_download_pid.log", 'r')
        pid = fp.read()
        fp.close()
        return pid
    else:
        return False


def start():
    for f in tb_episode.find({'down_status': 1}):
        anime_info = tb_anime.find_one({'season_id': f.get('season_id', 0)})
        if anime_info and not anime_info.get('down', False):
            continue
        print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), ' > download %s > %s', (f['_id'], f.get('long_title', '')))
        d = downloader.Downloader(f['_id'])
        d.start()
        while not d.exit:
            time.sleep(1)


if __name__ == '__main__':
    pid = read_pid()
    if pid:
        running_pid = psutil.pids()
        if int(pid) in running_pid:
            exit(0)
    write_pid()

    print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), " > auto download running...")
    while True:
        try:
            start()
        except Exception as e:
            print(datetime.datetime.now().strftime('%Y-%m-%d,%H:%m:%S'), e)
        time.sleep(60)
