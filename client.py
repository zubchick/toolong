# -*- coding: utf-8 -*-

import urllib

def get_short(url, service_url='http://2long.ru/'):
    return urllib.urlopen('%s?url=%s' % (service_url, url)).read()
