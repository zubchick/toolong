# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, abort
from models import Link

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def main_page():
    url =  request.args.get('url', None)
    if url:
        if url.find(request.host) >= 0:
            # redirect loop protection
            return url
        elif len(url) < len(request.host) + 6:
            # url already short
            return url
        else:
            l = Link(url=url)
        return "http://%s/%s" % (request.host, l.key)
    else:
        return render_template('mainpage.html')

@app.route('/<key>')
def key_url(key):
    l = Link(key=key)
    url = l.url

    if url:
        l.incr_click()
        return redirect(l.url)
    else:
        abort(404)

@app.route('/short', methods=['POST'])
def show_short_url():
    url = request.form.get('url', None)
    if url:
        if url.find(request.host) >= 0:
            # redirect loop protection
            return render_template('shorturl.html', short_url=url)
        elif len(url) < len(request.host) + 6:
            # url already short
            return render_template('shorturl.html', short_url=url)
        else:
            l = Link(url=url)
            return render_template('shorturl.html', link=l,
                                   short_url="http://%s/%s" % (request.host, l.key))
    else:
        return render_template('mainpage.html', error='Input url at first')

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
