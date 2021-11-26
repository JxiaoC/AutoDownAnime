# -*- coding:utf-8 -*-

from db.conn import mc

# mc = mongo_client
MONGO_DB_MAPPING = {
    'db': {
        'auto-down-anime-server': mc['auto_down_anime_server'],
    },
    'db_file': {
    }
}
