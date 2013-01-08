import re
# i stole this from pelican
# https://github.com/getpelican/pelican/blob/master/pelican/utils.py#L50
def get_date(string):
		"""Return a datetime object from a string.

		If no format matches the given date, raise a ValueError.
		"""
		string = re.sub(' +', ' ', string)
		formats = ['%Y-%m-%d %H:%M', '%Y/%m/%d %H:%M',
							 '%Y-%m-%d', '%Y/%m/%d',
							 '%d-%m-%Y', '%Y-%d-%m',  # Weird ones
							 '%d/%m/%Y', '%d.%m.%Y',
							 '%d.%m.%Y %H:%M', '%Y-%m-%d %H:%M:%S']
		for date_format in formats:
				try:
						return datetime.strptime(string, date_format)
				except ValueError:
						pass
		raise ValueError("'%s' is not a valid date" % string)

def group_by_tag(posts):
	grouped = {}
	for post in posts:
		tags = post.meta.get('Tags')
		if not tags:
			continue
		for tag in tags:
			if grouped.get(tag):
				grouped[tag].append(post)
			else:
				grouped[tag] = [post]
	return grouped
