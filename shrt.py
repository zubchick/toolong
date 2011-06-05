# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for
from redis import Redis
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
red = Redis()

def to_new_base(number, alph=None):
    """ from number(10-base) to number(62-base) """
    alph = alph or '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base = len(alph)

    res = []
    i = number
    while i != 0:
        i, rem = divmod(i, base)
        res.append(alph[rem])

    return ''.join(reversed(res)) or '0'


@app.route('/')
def main_page():
    url =  request.args.get('url', None)
    id = red.incr(app.config['LAST_ID']) #increment id
    if url:
        new_url = to_new_base(id)
        red.set(new_url, url) # short url
        return "http://%s/%s" % (request.host, new_url)
    else:
        return request.host
        # render_template('main.html', re)

if __name__ == '__main__':
    app.run()
