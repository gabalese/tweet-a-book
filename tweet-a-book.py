# coding=utf-8
from StringIO import StringIO
import datetime
import urllib
from flask import Flask, jsonify, request, render_template, make_response
from markupsafe import Markup

from src.epub import InvalidEpub, EPUB
from src.functions import extract_tweets
import src.settings

from xml.etree.ElementTree import ParseError

app = Flask(__name__)


@app.route('/ping')
def ping():
    response = {
        "status": "200 OK",
        "method": request.method,
        "time": datetime.datetime.now().strftime('%s')
    }
    return jsonify(response)


@app.route('/')
def main_view():
    return render_template("index.html")


@app.route('/post', methods=["GET", "POST"])
def find_tweets():

    if request.method == "GET":
        return render_template('load.html')

    if request.method == "POST":
        try:
            min_length = request.form.get("minimum", None)
            max_length = request.form.get("maximum", None)
            if min_length and max_length:
                src.settings.MAX_LENGTH = int(max_length)
                src.settings.MIN_LENGTH = int(min_length)
        except ValueError:
            pass

        try:
            requestfile = request.files["epubfile"]
            temporary = StringIO()
            temporary.write(requestfile.read())
        except Exception as e:
            return make_response(e, 500)
        try:
            epubfile = EPUB(temporary)
            tweets_list = extract_tweets(epubfile)
        except (InvalidEpub, ParseError):
            return make_response("Invalid EPUB", 403)

        keywords = request.form["keywords"].encode("UTF-8").split()
        option = request.form.get("option", None)

        partial = True if request.form.get("partial", None) == "yes" else False

        if len(keywords) > 0 and option == "any":
            tweets_list = filter(
                lambda x: any(k.lower() in (x.lower() if partial else x.lower().split()) for k in keywords),
                tweets_list)
        if len(keywords) > 0 and option == "all":
            tweets_list = filter(
                lambda x: all(k.lower() in (x.lower() if partial else x.lower().split()) for k in keywords),
                tweets_list)

        return render_template("output.html", tweets=tweets_list, title=epubfile.title, author=epubfile.author)


@app.template_filter('urlencode')
def urlencode_filter(s):
    if type(s) == 'Markup':
        s = s.unescape()
    s = s.encode('utf8')
    s = urllib.quote_plus(s)
    return Markup(s)


if __name__ == '__main__':
    app.debug = True
    app.run()
