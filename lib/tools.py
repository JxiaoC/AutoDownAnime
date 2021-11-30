import json
import os
from cPython import cPython as cp
from models.auto_down_anime import model
from turbo.core.exceptions import ResponseMsg

DEBUG = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__'))
tb_setting = model.Setting()
tb_episode = model.EpisodeList()
tb_anime = model.AnimeList()


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
    header['cookie'] = tb_setting.find_one()['cookie']
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
        raise ResponseMsg(-1, '不存在的分集数据')
    anime_info = tb_anime.find_one({'season_id': ep_info.get('season_id', 0)})
    if not anime_info:
        raise ResponseMsg(-1, '不存在的番剧数据')

    if not file_name:
        file_name = tb_setting.find_one().get('file_name', '')
    file_name = file_name.replace('%anime_title%', str(anime_info.get('title', '')))
    file_name = file_name.replace('%media_id%', str(anime_info.get('media_id', '')))
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


if __name__ == '__main__':
    get_bilibili_userinfo()