import os
from flask import Blueprint, redirect, url_for, render_template, abort, current_app
from flask import send_from_directory
from bloggen.classes import Pagination
from bloggen import pages, posts

public = Blueprint('public', __name__)

@public.route('/')
def home():
	page = pages.get('home')
	if not page:
		return redirect(url_for('.index'))
	return render_template('page.html', page=page)

@public.route('/blog/', defaults={'page': 1})
@public.route('/blog/<int:page>/')
def index(page):
	relevant = posts.contents.values()
	relevant.sort(key=lambda post: post.meta.get('Date'),
		reverse=True)
	paginated = Pagination(relevant, page,
		per_page=current_app.config.get('PAGINATE'))
	return render_template('blog/index.html', posts=paginated)

@public.route('/<path:url>/')
def page(url):
	page = pages.get(url)
	if not page:
		return abort(404)
	return render_template('page.html', page=page)

@public.route('/blog/<path:url>')
def post(url):
	post = posts.get(url)
	if not post:
		return abort(404)
	return render_template('blog/post.html', post=post)

@public.route('/file/<path:filename>')
def file(filename):
	path = os.path.join(current_app.config['CONTENT_DIR'], 'files')
	abspath = os.path.abspath(path)
	return send_from_directory(abspath, filename)

def setUp(app):
	app.register_blueprint(public)