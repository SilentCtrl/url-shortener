from flask import Flask, url_for, render_template, redirect, request
from werkzeug.routing import BaseConverter
import click
from flask.cli import with_appcontext
import os
import cgi
import validators
from .db import init_app, insert_to_database, lookup_in_database
from .converter import key_to_short

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
	@app.route('/s/<slug>', methods=['POST', 'GET'])
	def shortener_render(slug=None):
		if request.method == 'POST':
			text = request.form['url_to_shorten']
			link = insert_to_database(text)
			print(link)
			return key_to_short(int(link))
		if not slug:
			return render_template('hello.html')
		link = lookup_in_database(slug)
		if link and "Error:" not in link:
			return redirect(link)
		return "Error: " + str(slug) + " is not a shortened URL" #maybe print out an error message

	@app.route('/g/')
	def reroute_google():
	    return redirect("http://www.google.com")

	db.init_app(app)
	return app
