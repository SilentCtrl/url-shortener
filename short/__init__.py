from flask import Flask, url_for, render_template, redirect
from werkzeug.routing import BaseConverter
import click
from flask.cli import with_appcontext
import os
import cgi
import validators
from .converter import Converter
from .db import Db
from .shortener import Shortener 

def create_app():

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
	            link = shortener.insert_to_database(form["url_to_shorten"].value)
	            print(link)
	        return render_template('hello.html')
	    link = shortener.lookup_in_database(slug)
	    if link:
	        return redirect(link)
	    return render_template('hello.html')

	@app.route('/g/')
	def reroute_google():
	    return redirect("http://www.google.com")

	db.init_app(app)
	return app
