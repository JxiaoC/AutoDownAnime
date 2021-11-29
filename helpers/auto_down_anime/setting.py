import datetime
import re
import json

from bson import ObjectId

from models.auto_down_anime import model
from lib import tools

tb_setting = model.Setting()
tb_episode = model.EpisodeList()


def get():
    _ = tb_setting.find_one()
    if not _:
        _ = {
            'cookie': '',
            'ffmpeg_path': '',
            'save_dir_path': '',
            'file_name': '',
        }
        tb_setting.insert(_)
    return _


def get_file_name(file_name):
    return tools.get_file_name(file_name, tb_episode.find_one()['_id'])


def save(cookie, ffmpeg_path, save_dir_path, file_name):
    if save_dir_path.endswith('/'):
        save_dir_path = save_dir_path[:-1]
    tb_setting.update({}, {'$set': {
        'cookie': cookie,
        'ffmpeg_path': ffmpeg_path,
        'save_dir_path': save_dir_path,
        'file_name': file_name,
    }})
