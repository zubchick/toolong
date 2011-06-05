# -*- coding: utf-8 -*-
from datetime import datetime
from util import to_new_base
from url_normalize import url_normalize

class Link(object):
    """ Link object repr in redis """

    time_f = '%Y-%m-%d %H:%M:%S'

    def __init__(self, connect, url=None, key=None):
        obj = {}
        self._r = connect
        if url:
            # create new
            self._url = url_normalize(url)

            id = int(self._r.incr('last_url_id'))
            self._key = key = to_new_base(id)

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
