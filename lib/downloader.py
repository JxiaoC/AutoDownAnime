import datetime
import hashlib
import json
import os
import realpath
import shutil
import threading
import time

import requests
from bson import ObjectId

from models.auto_down_anime import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_episode = model.EpisodeList()
tb_setting = model.Setting()


class Downloader:
    def __init__(self, ep_id):
        self.complete = False
        self.fail = False
        self.exit = False
        self.temp_dir_path = os.getcwd() + '/temp'
        self.file_path = tools.get_file_path(ep_id=ep_id)
        if not os.path.exists(os.path.split(self.file_path)[0]):
            os.makedirs(os.path.split(self.file_path)[0])
        if not os.path.exists(self.temp_dir_path):
            os.makedirs(self.temp_dir_path)
        if not ObjectId.is_valid(ep_id):
            raise ResponseMsg(-1, '错误的ObjectId')
        self.ep_id = ObjectId(ep_id)
        self.down_text = ''
        self.temp_file_paths = []
        pass

    def get_download_url(self):
        data = {}
        try:
            ep_info = tb_episode.find_by_id(self.ep_id)
            if not ep_info:
                raise ResponseMsg(-1, '不存在的分集数据')
            episode_id = ep_info.get('id', '')
            max_retry = 3
            now_retry = 1
            urls = {
                'video': [],
                'audio': [],
            }
            while now_retry <= max_retry:
                now_retry += 1
                url = 'https://api.bilibili.com/pgc/player/web/playurl?avid=%s&bvid=%s&cid=%s&qn=%s&fnver=0&fnval=80&fourk=1&ep_id=%s&session=%s' % (
                    ep_info.get('aid', ''),
                    ep_info.get('bid', ''),
                    ep_info.get('cid', ''),
                    int(tb_setting.find_one().get('quality', 120)),
                    episode_id,
                    hashlib.md5(str(time.time()).encode()).hexdigest(),
                )
                print(url)
                self.header = tools.gen_http_header()
                self.header['referer'] = 'https://www.bilibili.com/bangumi/play/ep%s' % episode_id
                data = cp.get_html_for_requests(url, headers=self.header)
                data = json.loads(data)
                if data['result']['message'] == 'No video info.':
                    raise ResponseMsg('No video info.')
                self.quality = data['result']['quality']
                for f in data['result']['dash']['video']:
                    if f['id'] == self.quality:
                        url = []
                        url.append(f.get('base_url', f.get('baseUrl', '')))
                        for ff in f.get('backup_url', f.get('backupUrl', [])):
                            url.append(ff)
                        urls['video'].append(url)
                        break
                if len(urls['video']) > 0:
                    break
                print('没有获取到指定清晰度的数据, 等待10秒重新尝试')
                time.sleep(10)

            if len(urls['video']) == 0:
                print('没有找到匹配的清晰度资源, 获取低级别画质')
                self.quality = data['result']['dash']['video'][0]['id']
                for f in data['result']['dash']['video']:
                    if f['id'] == self.quality:
                        url = []
                        url.append(f.get('base_url', f.get('baseUrl', '')))
                        for ff in f.get('backup_url', f.get('backupUrl', [])):
                            url.append(ff)
                        urls['video'].append(url)
                        break

            _ = data['result']['dash']['audio'][0]
            urls['audio'].append(_.get('base_url', _.get('baseUrl', '')))
            for f in _.get('backup_url', _.get('backupUrl', '')):
                urls['audio'].append(f)
            return urls
        except Exception as e:
            print(data)
            print('下载地址解析失败, %s' % e)
            self.down_text = '下载地址解析失败, %s' % e
            self.fail = True
            self.complete = True
            return None

    def start(self):
        tb_episode.update({'_id': self.ep_id}, {'$set': {'down_text': self.down_text, 'down_status': 2, 'down_time': datetime.datetime.now()}})
        threading.Thread(target=self.thread_start).start()
        threading.Thread(target=self.thread_print).start()

    def thread_print(self):
        sleep_time = 0
        last_down_text = ''
        while not self.complete:
            if self.down_text and self.down_text.startswith('下载') and self.down_text == last_down_text:
                sleep_time += 1
            else:
                last_down_text = self.down_text
                sleep_time = 0
            if sleep_time > 300:
                self.fail = True
                self.down_text = '下载超时'
                self.complete = True
            tb_episode.update({'_id': self.ep_id}, {'$set': {'down_text': self.down_text, 'down_status': 2, 'down_time': datetime.datetime.now()}})
            time.sleep(1)
        if self.fail:
            tb_episode.update({'_id': self.ep_id}, {'$set': {'down_status': 3, 'down_text': self.down_text}})
        else:
            tb_episode.update({'_id': self.ep_id}, {'$set': {
                'down_status': 0,
                'complete_time': datetime.datetime.now(),
                'file_path': self.file_path,
                'quality': int(self.quality),
                'file_size': os.path.getsize(self.file_path),
            }})
        self.exit = True

    def thread_start(self):
        files = []
        urls = self.get_download_url()
        if not urls:
            return
        for i, video_urls in enumerate(urls['video']):
            # 下载每段视频, 目前好像每个视频都只有一段
            filepath = '%s/video_%s.m4s' % (self.temp_dir_path, i)
            for video_url in video_urls:
                try:
                    start = time.time()
                    response = requests.get(video_url, stream=True, headers=self.header)  # stream=True必须写上
                    size = 0  # 初始化已下载大小
                    chunk_size = 1024  # 每次下载的数据大小
                    content_size = int(response.headers['content-length'])  # 下载文件总大小
                    if os.path.exists(filepath) and os.path.getsize(filepath) == content_size:
                        break
                    try:
                        if response.status_code == 200:  # 判断是否响应成功
                            print('Start download,[File size]:{size:.2f} MB'.format(
                                size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                        with open(filepath, 'wb') as file:  # 显示进度条
                            for data in response.iter_content(chunk_size=chunk_size):
                                if self.complete:
                                    return
                                file.write(data)
                                size += len(data)
                                self.down_text = '下载视频 > %.2f%%' % float(size / content_size * 100)
                                print('\r' + self.down_text, end=' ')
                        end = time.time()  # 下载结束时间
                        self.down_text = '视频下载完成'
                        print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
                        down_file_size = os.path.getsize(filepath)
                        if down_file_size == content_size:
                            break
                        else:
                            print('下载实际大小(%s)和预期(%s)不一致' % (down_file_size, content_size))
                            os.remove(filepath)
                    except:
                        pass
                except:
                    pass
            if not os.path.exists(filepath):
                self.down_text = '下载失败'
                time.sleep(2)
                raise ResponseMsg(-1, '下载失败')
            files.append(filepath)
            self.temp_file_paths.append(filepath)

        if len(files) > 1:
            raise ResponseMsg(-100, '需要合并!!!!!')

        filepath = '%s/audio.m4s' % self.temp_dir_path
        for audio_url in urls['audio']:
            # 下载音频
            try:
                start = time.time()
                response = requests.get(audio_url, stream=True, headers=self.header)  # stream=True必须写上
                size = 0  # 初始化已下载大小
                chunk_size = 1024  # 每次下载的数据大小
                content_size = int(response.headers['content-length'])  # 下载文件总大小
                if os.path.exists(filepath) and os.path.getsize(filepath) == content_size:
                    break
                try:
                    if response.status_code == 200:  # 判断是否响应成功
                        print('Start download,[File size]:{size:.2f} MB'.format(
                            size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小
                    filepath = '%s/audio.m4s' % self.temp_dir_path  # 设置图片name，注：必须加上扩展名
                    with open(filepath, 'wb') as file:  # 显示进度条
                        for data in response.iter_content(chunk_size=chunk_size):
                            if self.complete:
                                return
                            file.write(data)
                            size += len(data)
                            self.down_text = '下载音频 > %.2f%%' % float(size / content_size * 100)
                            print('\r' + self.down_text, end=' ')
                    end = time.time()  # 下载结束时间
                    self.down_text = '音频下载完成'
                    print('Download completed!,times: %.2f秒' % (end - start))  # 输出下载用时时间
                    down_file_size = os.path.getsize(filepath)
                    self.temp_file_paths.append(filepath)
                    if down_file_size == content_size:
                        break
                    else:
                        print('下载实际大小(%s)和预期(%s)不一致' % (down_file_size, content_size))
                        os.remove(filepath)
                except:
                    pass
            except:
                pass

        if not os.path.exists(filepath):
            self.down_text = '下载失败'
            time.sleep(2)
            self.remove_temp_file()
            raise ResponseMsg(-1, '下载失败')
        files.append(filepath)

        try:
            self.down_text = '正在合并音视频文件'
            print('正在合并...')
            out_path = tools.ffmpeg_merge_audio_video(files, self.temp_dir_path)
        except Exception as e:
            self.down_text = '合并失败, %s' % e
            self.fail = True
            self.complete = True
            self.remove_temp_file()
            return

        try:
            self.down_text = '正在移动文件'
            print('正在移动...')
            shutil.move(out_path, self.file_path)
        except Exception as e:
            self.down_text = '移动失败, %s' % e
            self.fail = True

        self.remove_temp_file()
        self.complete = True

    def remove_temp_file(self):
        for path in self.temp_file_paths:
            try:
                os.path.exists(path) and os.remove(path)
            except Exception as e:
                print('删除临时文件失败, %s' % e)
                pass


if __name__ == '__main__':
    d = Downloader('61a8260ce2e0e3192549b0a4')
    d.start()
    while not d.exit:
        time.sleep(1)