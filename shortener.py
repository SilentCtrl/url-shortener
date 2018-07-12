from flask import Flask, url_for, render_template, redirect
from werkzeug.routing import BaseConverter
from . import converter
from . import __init__
from . import db

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
    if 'shortener.py?url_to_shorten' == slug:
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
    """ Takes a URL and returns
        it's shortened URL.
    """
    link = db.get_db()
    cursor = link.cursor()
    existquery = "SELECT * from link, id WHERE link = " + url
    try: 
        exists = cursor.execute(existquery)
        if exists:
            return exists[1]
        insertquery = "INSERT INTO links(link) VALUES (" + url + ")"
        try:
            cursor.execute(insertquery)
            exists = cursor.execute(existquery)
            return exists[1]
        except:
            print("Error: unable to insert")
    except:
        print("Error: unable to fetch data")

def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
    """
