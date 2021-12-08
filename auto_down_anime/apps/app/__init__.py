# -*- coding:utf-8 -*-
from turbo import register

from . import api, god

register.register_group_urls('', [
    ('/share', api.ShareHandler),
])

register.register_group_urls('/god', [
    ('', god.HomeHandler),
    ('/anime/(add|list|remove|ref_episode|end|down|edit)', god.AnimeHandler),
    ('/episode/(list|remove|reset)', god.EpisodeHandler),
    ('/setting/(get|save|get_file_name|test_server_jiang)', god.SettingHandler),
])
