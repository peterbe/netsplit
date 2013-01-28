import os
_path = os.path.join(os.path.dirname(__file__), 'netsplit_test.db')
os.environ['DATABASE_URI'] = 'sqlite:///%s' % _path
