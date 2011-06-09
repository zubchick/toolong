# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, abort
from models import Link

app = Flask(__name__)
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        return show_short_url()

    url =  request.args.get('url', None)
    if not url:
        return render_template('mainpage.html')

    if url.find(request.host) >= 0:
        # redirect loop protection
        return url
    elif len(url) < len('http://') + len(request.host) + 6:
        # url already short
        return url
    else:
        l = Link(url=url)
    return "http://%s/%s" % (request.host, l.key)

@app.route('/<key>')
def key_url(key):
    l = Link(key=key)
    url = l.url

    if url:
        l.incr_click()
        return redirect(l.url)
    else:
        abort(404)

def show_short_url():
    url = request.form.get('url', None)
    if not url:
        return render_template('mainpage.html', error='Input url at first')

    if url.find(request.host) >= 0:
        # redirect loop protection
        return render_template('shorturl.html', short_url=url)
    elif len(url) < len('http://') + len(request.host) + 6:
        # url already short
        return render_template('shorturl.html', short_url=url)
    else:
        l = Link(url=url)
        return render_template('shorturl.html', link=l,
                               short_url="http://%s/%s" % (request.host, l.key))


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
