import os
from flask import Blueprint, redirect, url_for, render_template, abort, current_app
from flask import send_from_directory
from bloggen.classes import Pagination
from bloggen.utils import sort_posts_by_date, group_posts_by_tag
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
	sorted = sort_posts_by_date(posts.contents.values())
	paginated = Pagination(sorted, page,
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

@public.route('/blog/tags/', defaults={'tag': None})
@public.route('/blog/tags/<string:tag>/')
def tags(tag):
	tags = group_posts_by_tag(posts.contents.values())
	tags = tags.items()
	tags.sort(key=lambda element: element[0])
	return render_template('blog/tags.html', tags=tags, tag=tag)

@public.route('/blog/tag/<string:tag>/', defaults={'page': 1})
@public.route('/blog/tag/<string:tag>/<int:page>/')
def tag(tag, page):
	tags = group_posts_by_tag(posts.contents.values())
	if not tags.get(tag):
		return abort(404)
	sorted = sort_posts_by_date(tags.get(tag))
	relevant = Pagination(sorted, page,
		per_page=current_app.config.get('PAGINATE'))
	return render_template('blog/tag.html', tag=tag, posts=relevant)

@public.route('/file/<path:filename>')
def file(filename):
	path = os.path.join(current_app.config['CONTENT_DIR'], 'files')
	abspath = os.path.abspath(path)
	return send_from_directory(abspath, filename)

def setUp(app):
	app.register_blueprint(public)