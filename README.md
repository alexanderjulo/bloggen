# Bloggen

Welcome to bloggen, the successor of [blogen](https://github.com/alexex/blogen). While blogen only generated a static collection of files, bloggen will also (and for now it only can do that) run in a live mode, where it generates contents as requested.

It is based on python, flask and my own urltomd library.

It is fairly easy to use and setup.

## Setup
This is just an example setup. You can of course adjust paths and settings to your liking!

```bash
git clone git@github.com:alexex/bloggen.git
cd bloggen

virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt

mkdir -p content/posts content/pages content/files
touch content/config.py

python manage.py runserver -c content/config.py
```

By now you have a fully running environment. You cann create posts and pages in their folders and bloggen will pick them up as long as they end with '.md'

## Settings
These settings are available to tweak:

```python
CONTENT_DIR = 'path'
# place where contents are stored
# optional
# default is the contents subdirectory of the current directory
# the path has to have three subirectories: posts/, pages/ and files/

OUTPUT_DIR = 'path'
# optional
# place where the generated static version will be saved

DEBUG = True or False
# enables debugging 
# optional
# default is False, 

SITE_NAME = 'site name'
# the name of your site
# optional
# default is julo.ch

PAGES_MENU = True or False
# whether you want to add your pages to the navbar
# optional
# default is False

BLOG_MENU = True or False
# whether you want to have further blog links in your menu
# optional
# default is True

DISQUS_NAME = False or 'your disqus name'
# if you want to enable disqus, set this to your short name
# optional
# default is False

SOCIAL_MENU = False or [('link', 'Name')]
# if you want a social dropdown in your navbar,
# add a list of tuples of url and name here
# optional
# default is False

ADMIN = False or 'password'
# if you want to enable the admin interface set this
# to a password
# optional
# default is False

PAGINATE = <INT>
# Paginate posts, set to 0 to disable pagination
# optional
# default is 5

DATETIME_FORMAT = 'strftime string'
# configure the format of dates, you can use string that strftime
# accepts
# optional
# default is '%d. %B %Y'

AUTHOR = 'name'
# this is the author that is used, if no author is given
# optional
# default is 'Uknown'
```

## File Format
Pages and posts are stored as plain text files in their folders. Metadata will be saved as YAML and the body as html, the files have the following format:

```
Title: <title>
Author: <author>
Date: <date>
Tags:
- i
- am
- a
- tag

## Markdown body
```

Besides `Title` all metadata is optional and can be spared. If you want to use `:` in your metadata contents, please enclose the strings in "".

Every tag has to be in it's own line and has to be prefix by an -. PYYAML is very intolerant in this regard, so indentation is not allowed either.