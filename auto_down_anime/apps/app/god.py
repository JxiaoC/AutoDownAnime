# -*- coding:utf-8 -*-
import turbo.log

from helpers.auto_down_anime import anime, episode, setting
from lib import tools
from .base import BaseHandler

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render(
            'index.html',
            username=tools.get_bilibili_username(),
        )


class AnimeHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '10'))
        search_key = self.get_argument('search_key', '')
        search_value = self.get_argument('search_value', '')
        list, count = anime.list(page, limit, search_key, search_value)
        self._data = {
            'list': list,
            'count': count,
        }

    def do_add(self):
        url = self.get_argument('url', '')
        self._data = anime.add(url)

    def do_remove(self):
        id = self.get_argument('id', '')
        self._data = anime.remove(id)

    def do_ref_episode(self):
        id = self.get_argument('id', '')
        self._data = anime.ref_episode(id)

    def do_end(self):
        id = self.get_argument('id', '')
        self._data = anime.switch_end(id)

    def do_down(self):
        id = self.get_argument('id', '')
        self._data = anime.switch_down(id)

    def do_edit(self):
        id = self.get_argument('id', '')
        key = self.get_argument('key', '')
        value = self.get_argument('value', '')
        self._data = anime.edit(id, key, value)


class EpisodeHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '10'))
        search_key = self.get_argument('search_key', '')
        search_value = self.get_argument('search_value', '')
        down_status = int(self.get_argument('down_status', '-1'))
        list, count = episode.list(page, limit, search_key, search_value, down_status)
        self._data = {
            'list': list,
            'count': count,
        }

    def do_remove(self):
        ids = self.get_argument('ids', '')
        self._data = episode.remove(ids)

    def do_reset(self):
        ids = self.get_argument('ids', '')
        self._data = episode.reset(ids)


class SettingHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_get(self):
        self._data = setting.get()

    def do_get_file_name(self):
        file_name = self.get_argument('file_name', '')
        self._data = setting.get_file_name(file_name)

    def do_test_server_jiang(self):
        self._data = setting.send_server_jiang_test()

    def do_save(self):
        cookie = self.get_argument('cookie', '')
        ffmpeg_path = self.get_argument('ffmpeg_path', '')
        save_dir_path = self.get_argument('save_dir_path', '')
        file_name = self.get_argument('file_name', '')
        quality = self.get_argument('quality', '')
        add_auto_down = self.get_argument('add_auto_down', 'true')
        server_jiang_send_key = self.get_argument('server_jiang_send_key', '')
        self._data = setting.save(cookie, ffmpeg_path, save_dir_path, file_name, quality, add_auto_down, server_jiang_send_key)

