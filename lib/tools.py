import os
DEBUG = os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__'))
gen_http_header_cookie_path = 'config/cookie.ini' if not DEBUG else '/Users/xiaoc/code/xiaoc/AutoDownAnime/config/cookie.ini'


def isint(a):
    try:
        int(a)
        return True
    except:
        return False


def gen_http_header():
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
    }
    if os.path.exists(gen_http_header_cookie_path):
        header['cookie'] = open(gen_http_header_cookie_path, 'r').read()
    return header
