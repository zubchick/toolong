# -*- coding: utf-8 -*-

from datetime import datetime
from util import to_new_base
from url_normalize import url_normalize
from redis import Redis
from hashlib import sha256

red = Redis()

class Link(object):
    """ Link object repr in redis """

    time_f = '%Y-%m-%d %H:%M:%S'

    def __init__(self, url=None, key=None):
        obj = {}
        self._r = red
        if url:
            # create new
            self._url = url_normalize(url)

            self._r.incr('last_url_id') # inc global counter
            self._key = key = self._find_key(self._url)

            obj[key] = self._url
            obj['%s:created_at' % key] = datetime.now().strftime(self.time_f)
            self._r.mset(obj)
        if key:
            # load exist
            self._key = key

    @property
    def key(self):
        return self._key

    @property
    def created_at(self):
        time = self._r.get('%s:created_at' % self.key)
        return datetime.strptime(time, self.time_f)

    @property
    def clicks(self):
        """ How many clicks """
        return self._r.llen(self.key + ':clicks')

    def incr_click(self):
        """ add new click """
        self._r.rpush(self.key + ':clicks', datetime.now().strftime(self.time_f))

    @property
    def url(self):
        return self._r.get(self._key)

    def _find_key(self, url):
        number = int(sha256(url).hexdigest(), 16) % (62 ** 6)
        if self._r.get(to_new_base(number)) is None:
            return to_new_base(number)
        else:
            while self._r.get(to_new_base(number)) is not None:
                number += 1
            else:
                return to_new_base(number)
