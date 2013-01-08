from flask import current_app, url_for
from bloggen import pages
from bloggen.utils import sort_posts_by_date

def formatdatetime(datetime):
	return datetime.strftime(current_app.config.get('DATETIME_FORMAT'))

def static(filename):
	return url_for('static', filename=filename)

def file(filename):
	return static('files/' + filename)

def firsts(elements, num=1):
	return elements[0:num]

def sortbydate(posts):
	return sort_posts_by_date(posts)

def inject_pages():
	sortedpages = sorted(pages.contents.values(),
		key=lambda page: page.meta.get('Title'))
	return dict(PAGES=sortedpages)


def setUp(app):
	app.add_template_filter(formatdatetime)
	app.add_template_filter(static)
	app.add_template_filter(file)
	app.add_template_filter(firsts)
	app.add_template_filter(sortbydate)
	app.context_processor(inject_pages)