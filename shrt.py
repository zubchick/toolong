# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, url_for, abort
from redis import Redis
from models import Link

app = Flask(__name__)
app.config.from_object('config')
red = Redis()

@app.route('/')
def main_page():
    url =  request.args.get('url', None)
    if url:
        l = Link(red, url=url)
        return "http://%s/%s" % (request.host, l.key)
    else:
        return u"<h1>Привет мир</h1>%s<p>Your IP - %s</p>" % (request.host, request.remote_addr)


@app.route('/<key>')
def key_url(key):
    l = Link(red, key=key)

    if request.args.get('clicks', None) is None:
        url = l.url
        if url:
            l.incr_click()
            return redirect(l.url)
        else:
            abort(404)
    else:
        return str(l.clicks)

@app.errorhandler(404)
def my404(error):
    return "404 - ololo", 404

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

