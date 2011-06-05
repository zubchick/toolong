# -*- coding: utf-8 -*-

import urllib

def get_short(url, service_url='http://2long.ru/'):
    return urllib.urlopen('%s?url=%s' % (service_url, url)).read()

def get_clicks(key, service_url='http://2long.ru/'):
    """ get clicks count
    key - last part of short url:
    `http://2long.ru/SDf2ed` key = SDf2ed
    """
    return urllib.urlopen('%s%s?clicks' % (service_url, key)).read()
