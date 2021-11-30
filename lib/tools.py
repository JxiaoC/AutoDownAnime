import datetime
import json
import os

from bson import ObjectId
from cPython import cPython as cp
from models.auto_down_anime import model
from turbo.core.exceptions import ResponseMsg

DEBUG = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__'))
tb_setting = model.Setting()
tb_episode = model.EpisodeList()
tb_anime = model.AnimeList()

common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]


def isint(a):
    try:
        int(a)
        return True
    except:
        return False


def gen_http_header():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    }
    try:
        header['cookie'] = tb_setting.find_one()['cookie']
    except:
        raise ResponseMsg(-1, '第一次使用请先到系统设置中填写cookie等信息!')
    return header


def get_bilibili_userinfo():
    res = cp.get_html_for_requests('https://api.bilibili.com/x/member/web/account', headers=gen_http_header())
    res = json.loads(res)
    return res['data']


def get_bilibili_username():
    try:
        return get_bilibili_userinfo()['uname']
    except:
        return '登录失效'


def get_file_path(file_name='', ep_id=None):
    if not ep_id:
        ep_info = tb_episode.find_one()
    else:
        ep_info = tb_episode.find_by_id(ep_id)

    if not ep_info:
        ep_info = {'_id': ObjectId('61a5ce13cc08540d4f68f5c6'), 'title': '1', 'long_title': '光溜溜的王子', 'atime': datetime.datetime(2021, 11, 30, 15, 9, 7, 294000), 'down_time': None, 'complete_time': datetime.datetime(2021, 11, 30, 15, 9, 59, 653000), 'season_id': 39462, 'cover': 'http://i0.hdslb.com/bfs/archive/67b1837f5c10d8d611a6dc8e57a12570452f18d1.jpg', 'id': 424605, 'aid': 251119469, 'bid': 'BV1Vv41137RM', 'cid': 425311294, 'down_status': 0, 'file_path': '/Users/xiaoc/code/xiaoc/AutoDownAnime/download/国王排名/1/S1E1.光溜溜的王子.mp4', 'down_text': '下载音频 > 98.81%', 'file_size': 92618386}
    anime_info = tb_anime.find_one({'season_id': ep_info.get('season_id', 0)})
    if not anime_info:
        anime_info = {'_id': ObjectId('61a5ce13cc08540d4f68f5c5'), 'title': '国王排名', 'atime': datetime.datetime(2021, 11, 30, 15, 9, 6, 987000), 'desc': '国家的丰饶、麾下勇者的数量、\\n以及国王本人如何像勇者一般强大，\\n这些要素的综合排名，便是所谓的“国王排名”。\\n主人公波吉是国王排名第七名的伯斯王治下王国的第一王子。\\n但是波吉却生来又聋又哑，贫弱到挥不动剑。\\n不止家臣甚至连民众都轻蔑地说「他实在不是当国王的料」。\\n这样的波吉人生中第一位交到的朋友，卡克。\\n与卡克的邂逅，以及那些微小的勇气中诞生的，\\n波吉人生的巨变将要开始——', 'cover': 'http://i0.hdslb.com/bfs/bangumi/image/3d9ca89d2df4603a99b6a5f54bf6b0501ead39aa.png', 'season': 1, 'media_id': 28235154, 'season_id': 39462, 'rating_count': 115017, 'rating_score': 9.7, 'end': True}

    if not file_name:
        file_name = tb_setting.find_one().get('file_name', '')
    file_name = file_name.replace('%anime_title%', str(anime_info.get('title', '')))
    file_name = file_name.replace('%media_id%', str(anime_info.get('media_id', '')))
    file_name = file_name.replace('%season%', str(anime_info.get('season', '')))
    file_name = file_name.replace('%ep_num%', str(ep_info.get('title', '')))
    file_name = file_name.replace('%ep_title%', str(ep_info.get('long_title', '')))
    file_name = file_name.replace('%season_id%', str(ep_info.get('season_id', '')))
    file_name = file_name.replace('%ep_id%', str(ep_info.get('id', '')))
    file_name = file_name.replace('%avid%', str(ep_info.get('aid', '')))
    file_name = file_name.replace('%bvid%', str(ep_info.get('bid', '')))
    file_name = file_name.replace('%cid%', str(ep_info.get('cid', '')))

    dir_path = tb_setting.find_one().get('save_dir_path', '')
    return ('%s/%s.mp4' % (dir_path, file_name)).replace('//', '/')


def av2bv(av):
    data = cp.get_html_for_requests('https://api.bilibili.com/x/web-interface/view?aid=%s' % av)
    data = json.loads(data)
    return data['data']['bvid']


def get_ffmpeg_path():
    return tb_setting.find_one().get('ffmpeg_path', '')


def ffmpeg_merge_audio_video(files, dir_path):
    cmd = get_ffmpeg_path()
    out_path = '%s/out.mp4' % dir_path
    for f in files:
        cmd += " -i '%s'" % f
    cmd += ' -vcodec copy -acodec copy %s/out.mp4 -y' % dir_path
    os.popen(cmd).read()
    if not os.path.exists(out_path):
        raise ResponseMsg(-1, '合并失败')
    return out_path


def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total


if __name__ == '__main__':
    get_bilibili_userinfo()
