# -*- coding:utf-8 -*-
import os

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.exists(os.path.join(SERVER_DIR, '__test__')):
    Debug = True
else:
    Debug = False
