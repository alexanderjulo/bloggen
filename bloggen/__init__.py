import os
from flask import Flask, Blueprint

class DefaultConfig(object):
	SECRET_KEY = 'i am an unsafe key, that has to be ignored.'
	CONTENT_DIR = './content/'
	OUTPUT_DIR = './output/'
	DEBUG = False
	SITE_NAME = 'julo.ch'
	PAGES_MENU = False
	DISQUS_NAME = False
	SOCIAL_MENU = False
	ADMIN = False
	PAGINATE = 5
	DATETIME_FORMAT = '%d. %B %Y'
	AUTHOR = None
	FREEZE = False
	BLOG_MENU = True

def create_app(config=None, configfile=None):
	app = Flask(__name__)
	app.config.from_object(DefaultConfig)
	app.config.from_envvar('BLOGGEN_CONFIG', silent=True)
	if config:
		app.config.from_object(config)
	if configfile:
		app.config.from_pyfile(os.path.abspath(configfile))

	pages.init_path(os.path.join(app.config['CONTENT_DIR'], 'pages'))
	posts.init_path(os.path.join(app.config['CONTENT_DIR'], 'posts'))

	import template
	template.setUp(app)

	import public
	public.setUp(app)

	if app.config['ADMIN']:
		import admin
		admin.setUp(app)

	return app

import urltomd
from classes import Page, Post

pages = urltomd.Mapper(contentclass=Page)
posts = urltomd.Mapper(contentclass=Post)