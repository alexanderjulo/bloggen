import os
import time
from datetime import datetime, date
from math import ceil
from bloggen import cache
from bloggen import urltomd
from bloggen.utils import get_date

def make_cache_key(f, element, body):
	return f.__name__ + "/" + element.path

class Mapper(urltomd.Mapper):

	def get(self, path, check=True):
		path = urltomd.trim_path(path)
		if check and not self.exists(path):
			return None
		return self._get(path, os.path.getctime(self.path + path + '.md'))

	@cache.memoize()
	def _get(self, file, ctime=None):
		return self.contentclass(self.path, file)

class CustomContent(urltomd.Content):

	def load_to_form(self, form):
		if not form.title.data:
			form.title.data = self.meta.get('Title')
		if not form.body.data:
			form.body.data = self.body
		if not form.url.data:
			form.url.data = self.path
		if not form.tags.data and self.meta.get('Tags'):
			taglist = self.meta.get('Tags')
			tags = taglist.pop(0)
			for tag in taglist:
				tags += ", %s" % tag
			form.tags.data = tags

	def save_from_form(self, form):
		self.meta['Title'] = form.title.data
		self.body = form.body.data
		self.path = form.url.data
		if form.tags.data:
			tags = [tag.strip() for tag in form.tags.data.split(',')]
			self.meta['Tags'] = tags

	@cache.memoize()
	def _render(self, body):
		return super(CustomContent, self)._render(body)

	_render.make_cache_key = make_cache_key

	def _load_meta(self, meta):
		return super(CustomContent, self)._load_meta(meta)

class Post(CustomContent):

	def __init__(self, *args, **kwargs):
		super(Post, self).__init__(*args, **kwargs)
		if not self.meta.get('Date'):
			if os.path.exists(self._full_path()):
				mtime = os.path.getctime(self._full_path())
				dt = datetime.strptime(time.ctime(mtime),
					"%a %b %d %H:%M:%S %Y")
				self.meta['Date'] = dt
		elif isinstance(self.meta.get('Date'), date):
			d = self.meta['Date']
			self.meta['Date'] = datetime(d.year, d.month, d.day)
		elif not isinstance(self.meta.get('Date'), datetime):
			self.meta['Date'] = get_date(self.meta['Date'])

	def load_to_form(self, form):
		super(Post, self).load_to_form(form)
		if not form.datetime.data:
			form.datetime.data = self.meta.get('Date')
		if not form.author.data:
			form.author.data = self.meta.get('Author')

	def save_from_form(self, form):
		super(Post, self).save_from_form(form)
		if form.datetime.data:
			self.meta['Date'] = form.datetime.data
		if form.author.data:
			self.meta['Author'] = form.author.data

	def _url(self):
		path = self.path.split('/')
		if len(path) > 1:
			path = '/'.join(path[1:])
		else:
			path = path[0]
		return '/blog/' + path + '/'

class Page(CustomContent):

	def _url(self):
		path = self.path.split('/')
		if len(path) > 1:
			path = '/'.join(path[1:])
		else:
			path = path[0]
		return '/' + path + '/'

class Pagination(object):

	def __init__(self, elements, page, per_page=5):
		self.elements = elements
		self.page = page
		self.per_page = per_page
		if per_page: 
			first = (page - 1) * per_page
			last = (page) * per_page
			self.on_page = elements[first:last]
		else:
			self.on_page = elements

	def __iter__(self):
		for element in self.on_page:
			yield element

	def iter_pages(self, left_edge=2, left_current=2,
					right_current=5, right_edge=2):
		last = 0
		for num in xrange(1, self.pages + 1):
			if num <= left_edge or \
				(num > self.page - left_current - 1 and \
				 num < self.page + right_current) or \
				num > self.pages - right_edge:
					if last + 1 != num:
						yield None
					yield num
					last = num

	@property
	def pages(self):
		if self.per_page:
			return int(ceil(len(self.elements) / float(self.per_page)))
		return 1

	@property
	def has_prev(self):
		return self.page > 1

	@property
	def has_next(self):
		return self.page < self.pages
