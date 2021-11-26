# -*- coding:utf-8 -*-
import realpath
from models.auto_down_anime import model


_ = model.AnimeList()
_.ensure_index([('media_id', -1)])
_.ensure_index([('atime', -1)])
