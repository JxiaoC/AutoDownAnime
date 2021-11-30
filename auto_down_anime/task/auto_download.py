# 定时脚本
import os
import time
import realpath

import psutil as psutil

from models.auto_down_anime import model
from lib import downloader

tb_episode = model.EpisodeList()


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
        print('download %s > %s', (f['_id'], f.get('long_title', '')))
        d = downloader.Downloader(f['_id'])
        d.start()
        while not d.exit:
            time.sleep(1)


if __name__ == '__main__':
    pid = read_pid()
    pid = int(pid)
    if pid:
        running_pid = psutil.pids()
        if pid in running_pid:
            exit(0)
    write_pid()

    print("auto download running...")
    while True:
        start()
        time.sleep(60)
