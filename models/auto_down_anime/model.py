# -*- coding:utf-8 -*-
from bson import ObjectId
from datetime import datetime

from .base import *


class AnimeList(Model):
    """
    番剧列表
        'title': 标题
        'atime': 添加时间
        'desc': 描述
        'cover': 封面
        'media_id': media_id
        'season_id': season_id
        'rating_count': 评分人数
        'rating_score':  评分
        'rating_score':  评分
        'end': 完结, 完结后的番剧将不再自动刷新
    """
    name = 'anime_list'

    field = {
        'title':                (str,           None),
        'atime':                (datetime,      None),
        'desc':                 (str,           None),
        'cover':                (str,           None),
        'media_id':             (int,           None),
        'season_id':            (int,           None),
        'rating_count':         (int,           None),
        'rating_score':         (float,         None),
        'end':                  (bool,          None),
    }


class EpisodeList(Model):
    """
    内容列表
        'title': 标题(一般是数字, 第几集)
        'long_title': 长标题(这才叫标题)
        'atime': 添加时间
        'down_time': 下载开始时间
        'complete_time': 下载完成时间
        'season_id': season_id
        'cover': 封面
        'id': id
        'aid': aid
        'bid': bvid
        'cid': cid
        'down_status': 下载状态, 0=完成, 1=未下载, 2=正在下载, 3=下载失败
        'down_text': 下载过程中用于显示的文本信息
        'file_path': 文件存放位置
        'file_size': 文件大小
    """
    name = 'episode_list'

    field = {
        'title':                (str,           None),
        'long_title':           (str,           None),
        'atime':                (datetime,      None),
        'down_time':            (datetime,      None),
        'complete_time':        (datetime,      None),
        'season_id':            (int,           None),
        'cover':                (str,           None),
        'id':                   (int,           None),
        'aid':                  (int,           None),
        'bid':                  (str,           None),
        'cid':                  (int,           None),
        'down_status':          (int,           None),
        'down_text':            (str,           None),
        'file_path':            (str,           None),
        'file_size':            (int,           None),
    }


class LogList(Model):
    """
    日志列表
        'atime': 添加时间
        'data': 日志内容
        'id': 所属id
    """
    name = 'log_list'

    field = {
        'atime':                (datetime,          None),
        'data':                 (str,               None),
        'id':                   (ObjectId,          None),
    }


class Setting(Model):
    """
    设置
        'cookie': cookie
        'ffmpeg_path': ffmpeg路径
        'save_dir_path': 保存文件夹
        'file_name': 保存名称
    """
    name = 'log_list'

    field = {
        'cookie':               (str,          None),
        'ffmpeg_path':          (str,          None),
        'save_dir_path':        (str,          None),
        'file_name':            (str,          None),
    }
