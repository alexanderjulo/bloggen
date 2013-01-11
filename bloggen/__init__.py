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
	CACHE_TYPE = 'simple'

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

	cache.init_app(app)

	import template
	template.setUp(app)

	import public
	public.setUp(app)

	if app.config['ADMIN']:
		import admin
		admin.setUp(app)

	try:
		from flask.ext.debugtoolbar import DebugToolbarExtension
		app.config['DEBUG_TB_PROFILER_ENABLED'] = True
		debugtoolbar = DebugToolbarExtension(app)
	except ImportError:
		pass

	return app

from flask.ext.cache import Cache
cache = Cache()

from classes import Mapper, Page, Post

pages = Mapper(contentclass=Page)
posts = Mapper(contentclass=Post)