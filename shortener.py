from flask import Flask, url_for, render_template
from werkzeug.routing import BaseConverter
from . import converter

app = Flask(__name__, template_folder='')

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/<regex("[abcABC0-9]{4,6}"):uid>-<slug>/')
def example(uid, slug):
    return "uid: %s, slug: %s" % (uid, slug)

@app.route('/s/')
def shortener_render():
    return render_template('/src/app/app.component.html')

@app.route('/s/<slug>/')
def test_short(slug):
    """ Looks up the slug in the shortener database. If it does not exist,
       go to the root shortener. Otherwise, redirect.
    """
    return slug
