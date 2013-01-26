import os
#os.environ['DATABASE_URI'] = 'postgresql://localhost/netsplit_test'
_path = os.path.join(os.path.dirname(__file__), 'netsplit_test.db')
os.environ['DATABASE_URI'] = 'sqlite:///%s' % _path
