# -*- coding:utf-8 -*-
import qiniu
import turbo.log
from bson import ObjectId
from helpers.auto_down_anime import anime, episode
from .base import BaseHandler

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render(
            'index.html',
        )


class AnimeHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '10'))
        list, count = anime.list(page, limit)
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


class EpisodeHandler(BaseHandler):

    def GET(self, type):
        self.route(type)

    def POST(self, type):
        self.GET(type)

    def do_list(self):
        page = int(self.get_argument('page', '1'))
        limit = int(self.get_argument('limit', '10'))
        list, count = episode.list(page, limit)
        self._data = {
            'list': list,
            'count': count,
        }

    def do_remove(self):
        id = self.get_argument('id', '')
        self._data = episode.remove(id)

