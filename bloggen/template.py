from flask import current_app, url_for
from bloggen import pages

def formatdatetime(datetime):
	return datetime.strftime(current_app.config.get('DATETIME_FORMAT'))

def static(filename):
	return url_for('static', filename=filename)

def file(filename):
	return static('files/' + filename)

def inject_pages():
	sortedpages = sorted(pages.contents.values(),
		key=lambda page: page.meta.get('Title'))
	return dict(PAGES=sortedpages)


def setUp(app):
	app.add_template_filter(formatdatetime)
	app.add_template_filter(static)
	app.add_template_filter(file)
	app.context_processor(inject_pages)