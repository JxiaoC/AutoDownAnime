import datetime
import re
import json

from bson import ObjectId

from helpers.auto_down_anime import episode
from helpers.auto_down_anime import setting
from models.auto_down_anime import model
from turbo.core.exceptions import ResponseMsg
from cPython import cPython as cp
from lib import tools

tb_anime_list = model.AnimeList()
tb_episode = model.EpisodeList()


def list(page, limit, search_key, search_value):
    res = []
    Q = {}
    if search_key and search_value:
        if search_key in ['title', 'desc']:
            Q[search_key] = {'$regex': search_value}
        else:
            Q[search_key] = int(search_value) if tools.isint(search_value) else search_value
    for f in tb_anime_list.find(Q).skip((page - 1) * limit).limit(limit).sort('atime', -1):
        res.append(f)
    return res, tb_anime_list.find(Q).count()


def add(url):
    if tools.isint(url):
        media_id = int(url)
    else:
        _ = re.findall('md(\d*)', url)
        if len(_) <= 0:
            raise ResponseMsg(-1, '无法解析出media_id, 请检查输入是否正确')
        media_id = int(_[0])
    print(media_id)
    __get_anime_data(media_id)


def edit(id, key, value):
    id = ObjectId(id)
    anime_info = tb_anime_list.find_by_id(id)
    if not anime_info:
        raise ResponseMsg(-1, '不存在的番剧信息')
    if key not in anime_info.keys():
        raise ResponseMsg(-1, '不存在的key')
    tb_anime_list.update({'_id': anime_info['_id']}, {'$set': {
        key: value
    }})


def remove(id):
    id = ObjectId(id)
    anime_info = tb_anime_list.find_by_id(id)
    if tb_episode.find({'season_id': anime_info.get('season_id', 0)}).count() > 0:
        raise ResponseMsg(-1, '存在未删除的分集内容, 无法删除番剧信息')
    tb_anime_list.remove_by_id(id)


def ref_episode(id):
    id = ObjectId(id)
    anime_info = tb_anime_list.find_by_id(id)
    episode.ref_episode_data(anime_info.get('season_id', 0))


def switch_end(id):
    id = ObjectId(id)
    anime_info = tb_anime_list.find_by_id(id)
    tb_anime_list.update({'_id': anime_info['_id']}, {'$set': {
        'end': not anime_info.get('end', False)
    }})


def switch_down(id):
    id = ObjectId(id)
    anime_info = tb_anime_list.find_by_id(id)
    tb_anime_list.update({'_id': anime_info['_id']}, {'$set': {
        'down': not anime_info.get('down', False)
    }})


def __get_anime_data(media_id):
    if tb_anime_list.find_one({'media_id': media_id}):
        raise ResponseMsg(-1, '已经存在此番剧了!')
    data = cp.get_html_for_requests('https://www.bilibili.com/bangumi/media/md%s/' % media_id, headers=tools.gen_http_header())
    doc = {
        'title': '',
        'atime': datetime.datetime.now(),
        'desc': cp.get_string(data, '"evaluate":"', '"'),
        'cover': '',
        'season': 1,
        'media_id': media_id,
        'season_id': 0,
        'rating_count': 0,
        'rating_score': 0,
        'end': False,
        'down': setting.get().get('add_auto_down', False),
    }
    try:
        data = json.loads(cp.get_html_for_requests('https://api.bilibili.com/pgc/review/user?media_id=%s' % media_id, headers=tools.gen_http_header()))
    except Exception as e:
        raise ResponseMsg(-1, '解析番剧基础内容时出错, %s' % e)

    try:
        doc['cover'] = data['result']['media']['cover']
    except Exception as e:
        raise ResponseMsg(-1, '获取封面图时出错, %s' % e)

    try:
        doc['season_id'] = data['result']['media']['season_id']
    except Exception as e:
        raise ResponseMsg(-1, '获取season_id时出错, %s' % e)

    try:
        doc['title'] = data['result']['media']['title']
    except Exception as e:
        raise ResponseMsg(-1, '获取标题时出错, %s' % e)

    try:
        doc['rating_count'] = data['result']['media']['rating']['count']
    except Exception as e:
        doc['rating_count'] = 0

    try:
        doc['rating_score'] = data['result']['media']['rating']['score']
    except Exception as e:

        doc['rating_count'] = 0

    try:
        _ = re.search('[\(\[]第(.+?)季[\)\]]', doc['title'])
        if not _:
            _ = re.search('第(.+?)季', doc['title'])

        if _:
            doc['season'] = tools.chinese2digits(_.group(1))
            doc['title'] = doc['title'].replace(_.group(0), '').strip()
    except Exception as e:
        raise ResponseMsg(-1, '获取第几季时出错, %s' % e)

    doc['end'] = data['result']['media']['new_ep']['index_show'].startswith('全')
    tb_anime_list.insert(doc)
    episode.ref_episode_data(doc['season_id'])


if __name__ == '__main__':
    add('https://www.bilibili.com/bangumi/media/md28235160/?spm_id_from=666.25.b_6d656469615f6d6f64756c65.2')
