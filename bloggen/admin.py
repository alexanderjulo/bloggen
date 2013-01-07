from functools import wraps
from wtforms import fields, validators, ValidationError
from flask import Blueprint, render_template, redirect, abort, url_for
from flask import current_app, g, session
from flask.ext.wtf import Form
from bloggen import pages, posts
from classes import Pagination

admin = Blueprint('admin', __name__)

class ContentForm(Form):
	title = fields.TextField('Title', [validators.Required()])
	body = fields.TextAreaField('Body', [validators.Required()])
	url = fields.TextField('URL', [validators.Required()])
	submit = fields.SubmitField('Submit')

class PageForm(ContentForm):
	pass

class PostForm(ContentForm):
	datetime = fields.DateTimeField('Date and Time', [validators.Optional()])
	author = fields.TextField('Author', [validators.Optional()])

class LoginForm(Form):
	password = fields.PasswordField('Password', [validators.Required()])
	submit = fields.SubmitField('Login')

	def validate_password(self, field):
		if not current_app.config['ADMIN'] == field.data:
			raise ValidationError('Invalid password.')

def admin_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		if not g.admin:
			return abort(403)
		else:
			return f(*args, **kwargs)
	return wrapper

@admin.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		g.admin = True
		return redirect(url_for('.index'))
	return render_template('admin/login.html', form=form)

@admin.route('/logout/')
@admin_required
def logout():
	g.admin = False
	return redirect(url_for('public.home'))

@admin.route('/', defaults={'page': 1})
@admin.route('/<int:page>/')
@admin_required
def index(page):
	sortedpages = pages.contents.values()
	sortedpages.sort(
		key=lambda page: page.meta.get('Title'), reverse=True)
	unpaginatedposts = posts.contents.values()
	unpaginatedposts.sort(
			key=lambda post: post.meta.get('Date'), reverse=True)
	return render_template('admin/index.html', pages=sortedpages,
		posts=unpaginatedposts)

@admin.route('/create/')
@admin_required
def create():
	return render_template('admin/create.html')

@admin.route('/post/create/', methods=['GET', 'POST'])
@admin_required
def create_post():
	form = PostForm()
	if form.validate_on_submit():
		post = posts.create(form.url.data)
		post.save_from_form(form)
		post.save()
		return redirect(post.url)
	return render_template('admin/editor.html', form=form)

@admin.route('/post/<path:path>/edit/', methods=['GET', 'POST'])
@admin_required
def edit_post(path):
	post = posts.get(path)
	if not post:
		return abort(404)
	form = PostForm()
	post.load_to_form(form)
	if form.validate_on_submit():
		print form.author.data
		post.save_from_form(form)
		print post.meta['Author']
		post.save()
		return redirect(post.url)
	return render_template('admin/editor.html', form=form)

@admin.route('/page/create/', methods=['GET', 'POST'])
@admin_required
def create_page():
	form = PageForm()
	if form.validate_on_submit():
		page = page.create(form.url.data)
		page.save_from_form(form)
		page.save()
		return redirect(page.url)
	return render_template('admin/editor.html', form=form)

@admin.route('/page/<path:path>/edit/')
@admin_required
def edit_page(path):
	page = pages.get(path)
	if not page:
		return abort(404)
	form = PostForm()
	page.load_to_form(form)
	if form.validate_on_submit():
		page.save_from_form(form)
		page.save()
		return redirect(page.url)
	return render_template('admin/editor.html', form=form)

@admin.route('/post/<path:path>/delete/')
@admin_required
def delete_post(path):
	if not posts.exists(path):
		return abort(404)
	posts.delete(path)
	return redirect(url_for('admin.index'))

@admin.route('/page/<path:path>/delete/')
@admin_required
def delete_page(path):
	if not pages.exists(path):
		return abort(404)
	pages.delete(path)
	return redirect(url_for('admin.index'))

def check_admin_session():
	g.admin = session.get('admin', False)

def save_admin_session(response):
	session['admin'] = g.admin
	return response

def setUp(app):
	app.register_blueprint(admin, url_prefix='/admin')
	app.before_request(check_admin_session)
	app.after_request(save_admin_session)
