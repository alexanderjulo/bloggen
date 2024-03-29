import os
import yaml
import misaka
from exceptions import IOError

def trim_path(path):
	if path.startswith('/'):
		path = path[1:]
	if path.endswith('/'):
		path = path[:-1]
	return path

class Content(object):

	def __init__(self, root, path):
		self.root = root
		self.path = path
		self.body = None
		self._meta = {}
		if os.path.exists(self._full_path()):
			self._read()

	def __repr__(self):
		return "<Content object at '%s.md'>" % self.path

	def _read(self):
		"""Load the current state on the disk. If you use `_read`
		before you saved eventual changes with `_write` they will
		be lost."""
		with open(self._full_path()) as f:
			content = f.read().decode('utf8')
		content = content.split(u'\n\n')
		meta = self._load_meta(content[0])
		if not isinstance(meta, dict):
			meta = {}
		self._meta = meta
		self.body = '\n\n'.join(content[1:])

	def _write(self):
		"""Write the current state to the file."""
		with open(self._full_path(), 'w') as f:
			f.write(self._dump_meta(self.meta))
			f.write(u'\n')
			f.write(self.body.encode('utf8'))

	def _full_path(self):
		return self.root + self.path + '.md'

	def _url(self):
		"""This one can be overwritten by subclasses, if they want
		to manually pretend to have a different url."""
		return '/' + self.path + '/'

	def _load_meta(self, meta):
		return yaml.safe_load(meta)

	def _dump_meta(self, meta):
		return yaml.safe_dump(self._meta,
			default_flow_style=False).encode('utf8')

	def _render(self, body):
		return misaka.html(body)

	@property
	def url(self):
		return self._url()

	@property
	def meta(self):
		return self._meta

	def __getitem__(self, item):
		return self.meta[item]

	@property
	def html(self):
		return self._render(self.body)

	def __html__(self):
		return self.html

	def save(self):
		self._write()

	def reload(self):
		self._read()

class Mapper(object):

	def __init__(self, path=None, contentclass=Content):
		self.contentclass = contentclass
		if path:
			self.init_path(path)

	def init_path(self, path):
		if not os.path.isdir(path):
			raise IOError('%s does not exist or is not a directory.'
				% path)
		if not path.endswith('/'):
			path += '/'
		self.path = path

	def exists(self, path):
		path = trim_path(path)
		return os.path.exists(self.path + path + '.md')

	def _get(self, path):
		return self.contentclass(self.path, path)

	def get(self, path, check=True):
		path = trim_path(path)
		if check and not self.exists(path):
			return None
		return self._get(path)

	def create(self, path):
		path = trim_path(path)
		if self.exists(path):
			return False
		directory = '/'.join(path.split('/')[:-1])
		if len(directory) > 0 and not os.path.exists(self.path + directory):
			os.makedirs(self.path + path)
		return self.get(path, check=None)

	def delete(self, path):
		path = trim_path(path)
		if not os.path.exists(self.path + path + '.md'):
			return False
		os.remove(self.path + path + '.md')
		return True

	def _list(self, subdirectory=None):
		def _walk(directory, path_prefix=()):
			for name in os.listdir(directory):
				fullname = os.path.join(directory, name)
				if os.path.isdir(fullname):
					_walk(fullname, path_prefix + (name,))
				elif name.endswith('.md'):
					path = u'/'.join(path_prefix + (name[:-3],))
					if subdirectory:
						path = u'/'.join([subdirectory, path])
					element = self.get(path, check=None)
					elements[element.url] = element
		elements = {}
		if subdirectory:
			_walk(self.path + subdirectory)
		else:
			_walk(self.path)
		return elements

	@property
	def contents(self):
		"""This property will return a full list of all contents
		with their path paths. As this has to index the whole
		directory every time it is run, it can be very slow on
		bigger collections and should be used carefully."""
		return self._list()

	def subcontents(self, path):
		path = trim_path(path)
		"""Get all contents that start with the given path. This
		will only work is the path is the full part before a
		slash, which means all contents will be stored in one
		directory and its subdirectories."""
		if not os.path.isdir(self.path + path):
			return None
		return self._list(path)