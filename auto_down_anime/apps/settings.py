# -*- coding:utf-8 -*-
import os
# installed app list
INSTALLED_APPS = (
    'app',
)


# language
LANG = 'en'

TEMPLATE_PATH = 'app/'


AES_KEY = 'Agc8Th6Ivy4Iti1Y'

if len(AES_KEY) != 16:
    raise Exception('aes key length error')