from flask.ext.script import Manager
from bloggen import create_app

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='configfile', required=False)

if __name__ == '__main__':
	manager.run()