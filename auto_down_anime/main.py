# -*- coding:utf-8 -*-
import os
import threading
import time

import tornado.options
import turbo.app
import turbo.register
from tornado.options import define, options

import setting

# uncomment this to init state managedocument.forms['form'].reset();r: store
# import store

turbo.register.register_app(
    setting.SERVER_NAME,
    setting.TURBO_APP_SETTING,
    setting.WEB_APPLICATION_SETTING,
    __file__,
    globals()
)

define("port", default=8860, type=int)


def guardian_auto_download():
    while True:
        os.popen('python3 task/auto_download.py').read()
        time.sleep(60)


def guardian_ref_ep():
    while True:
        os.popen('python3 task/auto_ref_ep.py').read()
        time.sleep(60)


if __name__ == '__main__':
    threading.Thread(target=guardian_auto_download).start()
    threading.Thread(target=guardian_ref_ep).start()
    tornado.options.parse_command_line()
    turbo.app.start(options.port)
