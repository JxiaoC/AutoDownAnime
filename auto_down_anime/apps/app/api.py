# -*- coding:utf-8 -*-
import requests
import turbo.log
from .base import BaseHandler
import urllib.parse

logger = turbo.log.getLogger(__file__)

channel = '3e5a6b56d8c70441'  # 讯飞提供的渠道号
column_id = "242811"  # 科大讯飞提供的栏目id

base_url = "http://api.kuyinyun.com/p/"


class ShareHandler(BaseHandler):
    def get(self):
        self.render('share.html')


class FissionHandler(BaseHandler):
    def GET(self, type):
        self.route(type)

    def do_help_list(self):
        token = self.get_argument('token', '')
        limit = int(self.get_argument('limit', '10'))
        self._data = fission.get_help_list(token, limit)
