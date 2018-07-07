from flask import Flask, url_for, render_template, redirect, current_app, g
from flask.cli import with_appcontext
from werkzeug.routing import BaseConverter
from . import converter
from . import __init__
import MySQLdb

app = Flask(__name__)

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
@app.route('/s/<slug>')
def shortener_render(slug=None):
    if not slug:
    	return render_template('hello.html')
    if 'shortener.py?url_to_shorten' in slug:
        print('action not implemented')
        return render_template('hello.html')
    #TODO: lookup the url here
    return redirect("http://www.google.com")

@app.route('/g/')
def reroute_google():
    return redirect("http://www.google.com")


############################################################
#       DATABASE ACCESSING STUFF ###########################

def insert_to_database(url):
    """ Takes a URL to insert and returns
        it's shortened URL.
    """
    #ADD THE CURSOR SOMEWHERE


def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
    """

############################################################
#      DATABASE ABSTRACTION LAYER ##########################

import click

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect(host='localhost',user='root',passwd='')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)