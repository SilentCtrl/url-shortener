import MySQLdb
import click
from flask import current_app, g
from flask.cli import with_appcontext
from .converter import short_to_key, key_to_short

def get_db():
    if 'db' not in g:
        g.db = MySQLdb.connect('localhost','root','','URLs')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        cursor = db.cursor()
        cursor.execute(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

############################################################
#       DATABASE ACCESSING STUFF ###########################

def insert_to_database(url):
    """ Takes a URL and returns
        it's shortened URL.
    """
    link = get_db()
    cursor = link.cursor()
    existquery = "SELECT id from links WHERE link = \'" + url + "\'"
    print(existquery)
    try: 
        cursor.execute(existquery)
        exists = cursor.fetchall()
        if exists:
            return key_to_short(int(exists[0][0]))
        insertquery = "INSERT INTO links(link) VALUES (\'" + url + "\')"
        try:
            cursor.execute(insertquery)
            cursor.execute(existquery)
            exists = cursor.fetchall()
            link.commit()
            return key_to_short(int(exists[0][0]))
        except Exception as e:
            link.rollback()
            return "Error: unable to insert"
    except Exception as e:
        return "Error: unable to connect to database"

def lookup_in_database(url):
    """ Takes a shortened URL and looks it
        up in the database. Returns it's
        actual URL if it is in the database.
        Returns false otherwise.
    """
    key = short_to_key(url)
    link = get_db()
    cursor = link.cursor()
    existquery = "SELECT link from links WHERE id = " + str(key)
    try:
        cursor.execute(existquery)
        exists = cursor.fetchall()
        if exists:
            return exists[0][0]
        return False
    except:
        return "Error: unable to fetch data"
