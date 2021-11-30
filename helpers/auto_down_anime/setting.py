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
            'quality': 120,
            'file_name': '%anime_title%/Season %season%/%ep_title% S%season%E%ep_num%',
        }
        tb_setting.insert(_)
    return _


def get_file_name(file_name):
    return tools.get_file_path(file_name.strip())


def save(cookie, ffmpeg_path, save_dir_path, file_name, quality):
    if save_dir_path.endswith('/'):
        save_dir_path = save_dir_path[:-1]
    if file_name.startswith('/'):
        file_name = file_name[1:]
    tb_setting.update({}, {'$set': {
        'cookie': cookie,
        'quality': int(quality),
        'ffmpeg_path': ffmpeg_path.strip(),
        'save_dir_path': save_dir_path.strip(),
        'file_name': file_name.strip(),
    }})
