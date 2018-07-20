from flask import Flask, url_for, render_template, redirect
from werkzeug.routing import BaseConverter
import click
from flask.cli import with_appcontext
from . import converter
from . import __init__
from . import db
import cgi
import validators

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
    if "shortener.py" in str(slug):
        form = cgi.FieldStorage()
        if "url_to_shorten" in form and validators.url(form["url_to_shorten"]):
            link = insert_to_database(form["url_to_shorten"].value)
            print(link)
        return render_template('hello.html')
    link = lookup_in_database(slug)
    if link:
        return redirect(link)
    return redirect("http://www.google.com")

@app.route('/g/')
def reroute_google():
    return redirect("http://www.google.com")


############################################################
#       DATABASE ACCESSING STUFF ###########################

def insert_to_database(url):
    """ Takes a URL and returns
        it's shortened URL.
    """
    link = db.get_db()
    cursor = link.cursor()
    existquery = "SELECT id from links WHERE link = " + url
    try: 
        cursor.execute(existquery)
        exists = cursor.fetchall()
        if exists:
            return cursor.key_to_short(exists[0])
        insertquery = "INSERT INTO links(link) VALUES (" + url + ")"
        try:
            cursor.execute(insertquery)
            cursor.execute(existquery)
            exists = cursor.fetchall()
            link.commit()
            return cursor.key_to_short(exists[0])
        except:
            link.rollback()
            print("Error: unable to insert")
    except:
        print("Error: unable to fetch data")

def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
        Returns false otherwise.
    """
    key = converter.short_to_key(url)
    link = db.get_db()
    cursor = link.cursor()
    existquery = "SELECT link from links WHERE id = " + str(key)
    try:
        cursor.execute(existquery)
        exists = cursor.fetchall()
        if exists:
            return exists[0]
        return False
    except:
        print("Error: unable to fetch data")

###########################################################
#       DATABASE INITIALIZATION STUFF #####################
@click.command('init-db')
@with_appcontext
def init_db_command():
    db.init_db()
    click.echo('Initialized the database.')