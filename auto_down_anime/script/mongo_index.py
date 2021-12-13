# -*- coding:utf-8 -*-
import realpath
from models.auto_down_anime import model


_ = model.AnimeList()
_.ensure_index([('media_id', -1)])
_.ensure_index([('atime', -1)])
_.ensure_index([('title', -1), ('atime', -1)])
_.ensure_index([('desc', -1), ('atime', -1)])
_.ensure_index([('media_id', -1), ('atime', -1)])
_.ensure_index([('season_id', -1), ('atime', -1)])


_ = model.EpisodeList()
_.ensure_index([('id', -1)])
_.ensure_index([('end', -1)])
_.ensure_index([('atime', -1)])
_.ensure_index([('season_id', -1), ('atime', -1)])
_.ensure_index([('down_status', -1), ('atime', -1)])
_.ensure_index([('long_title', -1), ('atime', -1)])
