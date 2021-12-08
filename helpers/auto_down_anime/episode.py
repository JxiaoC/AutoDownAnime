import datetime
import os
import re
import json

from bson import ObjectId

from models.auto_down_anime import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_anime_list = model.AnimeList()
tb_episode = model.EpisodeList()


def list(page, limit, search_key, search_value, down_status=-1):
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['long_title']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    if down_status != -1:
        Q['down_status'] = down_status
    for f in tb_episode.find(Q).skip((page - 1) * limit).limit(limit).sort('atime', -1):
        f['anime_info'] = tb_anime_list.find_one({'season_id': f.get('season_id', 0)})
        f['file_exists'] = os.path.exists(f.get('file_path', ''))
        res.append(f)
    return res, tb_episode.find(Q).count()


def remove(ids):
    ids = [ObjectId(f) for f in ids.split(',') if ObjectId.is_valid(f)]
    tb_episode.remove({'_id': {'$in': ids}}, multi=True)


def reset(ids):
    ids = [ObjectId(f) for f in ids.split(',') if ObjectId.is_valid(f)]
    tb_episode.update({'_id': {'$in': ids}}, {'$set': {
        'down_time': None,
        'complete_time': None,
        'down_status': 1,
        'down_text': '',
        'file_path': '',
        'file_size': 0
    }}, multi=True)


def ref_episode_data(season_id):
    try:
        data = json.loads(cp.get_html_for_requests('https://api.bilibili.com/pgc/web/season/section?season_id=%s' % season_id, headers=tools.gen_http_header()))
    except Exception as e:
        raise ResponseMsg(-1, '解析番剧分集列表时出错, %s' % e)
    for episode in data['result']['main_section']['episodes']:
        try:
            id = episode['id']
            if tb_episode.find_one({'id': id}):
                print('[%s]已经存在的分集信息' % id)
                continue
            episode_info = {
                'title': episode['title'],
                'long_title': episode['long_title'],
                'atime': datetime.datetime.now(),
                'down_time': None,
                'complete_time': None,
                'season_id': season_id,
                'cover': episode['cover'],
                'id': id,
                'aid': episode['aid'],
                'bid': tools.av2bv(episode['aid']),
                'cid': episode['cid'],
                'down_status': 1,
                'file_path': '',
            }
            tb_episode.insert(episode_info)
            print('新增%s.%s' % (episode_info['title'], episode_info['long_title']))
        except Exception as e:
            raise ResponseMsg(-1, '解析番剧分集信息时出错, %s' % e)
        pass
    pass


if __name__ == '__main__':
    ref_episode_data(39462)