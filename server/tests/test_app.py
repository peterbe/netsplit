import os
import unittest
import json
import tempfile

import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        #self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        #flaskr.init_db()
        app.STATE = {}

    def tearDown(self):
        app.STATE = {}
        #os.close(self.db_fd)
        #os.unlink(flaskr.app.config['DATABASE'])

    def test_posting_event(self):
        event_data = [
          {'from': 'E', 'to': 'P', 'amount': 10},
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)
        assert state_data[0]['from'] == 'E'
        assert state_data[0]['to'] == 'P'
        assert state_data[0]['amount'] == 10

        event_data = [
            {'from': 'P', 'to': 'E', 'amount': 7},
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)
        assert state_data[0]['from'] == 'E'
        assert state_data[0]['to'] == 'P'
        assert state_data[0]['amount'] == 3

    def test_getting_state(self):
        event_data = [
          {'from': 'E', 'to': 'P', 'amount': 10},
        ]
        self.app.post('/event', data=dict(data=json.dumps(event_data)))
        event_data = [
            {'from': 'P', 'to': 'E', 'amount': 7},
        ]
        self.app.post('/event', data=dict(data=json.dumps(event_data)))
        response = self.app.get('/state')
        state_data = json.loads(response.data)
        assert state_data[0]['from'] == 'E'
        assert state_data[0]['to'] == 'P'
        assert state_data[0]['amount'] == 3

    def test_simple_scenario(self):
        event_data = [
            app.serialize('E', 'P', 10),
            app.serialize('L', 'P', 10),
            app.serialize('M', 'P', 5),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        assert app.serialize('E', 'P', 10) in state_data
        assert app.serialize('L', 'P', 10) in state_data
        assert app.serialize('M', 'P', 5) in state_data

        # 2
        event_data = [
            app.serialize('E', 'M', 10),
            app.serialize('L', 'M', 10),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        assert app.serialize('E', 'M', 10) in state_data
        assert app.serialize('L', 'M', 10) in state_data
        assert app.serialize('E', 'P', 10) in state_data
        assert app.serialize('L', 'P', 10) in state_data
        assert app.serialize('M', 'P', 5) in state_data

        # 3
        event_data = [
            app.serialize('P', 'L', 12),
            app.serialize('M', 'L', 12),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        assert app.serialize('P', 'L', 2) in state_data
        assert app.serialize('M', 'L', 2) in state_data
        assert app.serialize('E', 'P', 10) in state_data
        assert app.serialize('E', 'M', 10) in state_data
        assert app.serialize('M', 'P', 5) in state_data

        # 4
        event_data = [
            app.serialize('P', 'E', 7),
            app.serialize('L', 'E', 7),
            app.serialize('M', 'E', 7),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        assert app.serialize('E', 'P', 3) in state_data
        assert app.serialize('L', 'E', 7) in state_data
        assert app.serialize('E', 'M', 3) in state_data
        assert app.serialize('P', 'L', 2) in state_data
        assert app.serialize('M', 'L', 2) in state_data
        assert app.serialize('M', 'P', 5) in state_data


if __name__ == '__main__':
    unittest.main()
