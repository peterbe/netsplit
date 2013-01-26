import os
import unittest
import json
from nose.tools import eq_, ok_

from netsplit import app
from netsplit.models import Debt


class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        # would be nice to somehow check the URI used as *_test
        app.init_db()

    def tearDown(self):
        # XXX because I don't know how to delete the entire table contents
        for each in Debt.query.all():
            app.db_session.delete(each)
        app.db_session.commit()

    def test_add_debt(self):
        func = app.add_debt
        app.add_debt('E', 'P', 10)
        eq_(Debt.query.filter(Debt.from_ == 'E').first().amount, 10.0)

        app.add_debt('P', 'E', 7)
        eq_(Debt.query.filter(Debt.from_ == 'E').first().amount, 3.0)

        app.add_debt('P', 'E', 2)
        eq_(Debt.query.filter(Debt.from_ == 'E').first().amount, 1.0)

        app.add_debt('P', 'E', 4)
        eq_(Debt.query.filter(Debt.from_ == 'E').first().amount, -3.0)

    def test_posting_event(self):
        event_data = [
          {'from': 'E', 'to': 'P', 'amount': 10},
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)
        eq_(state_data[0]['from'], 'E')
        eq_(state_data[0]['to'], 'P')
        eq_(state_data[0]['amount'], 10.00)

        event_data = [
            {'from': 'P', 'to': 'E', 'amount': 7},
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)
        eq_(state_data[0]['from'], 'E')
        eq_(state_data[0]['to'], 'P')
        eq_(state_data[0]['amount'], 3.00)

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
        eq_(state_data[0]['from'], 'E')
        eq_(state_data[0]['to'], 'P')
        eq_(state_data[0]['amount'], 3.00)

    def test_simple_scenario(self):
        event_data = [
            app.serialize('E', 'P', 10),
            app.serialize('L', 'P', 10),
            app.serialize('M', 'P', 5),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        ok_(app.serialize('E', 'P', 10) in state_data)
        ok_(app.serialize('L', 'P', 10) in state_data)
        ok_(app.serialize('M', 'P', 5) in state_data)

        # 2
        event_data = [
            app.serialize('E', 'M', 10),
            app.serialize('L', 'M', 10),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        ok_(app.serialize('E', 'M', 10) in state_data)
        ok_(app.serialize('L', 'M', 10) in state_data)
        ok_(app.serialize('E', 'P', 10) in state_data)
        ok_(app.serialize('L', 'P', 10) in state_data)
        ok_(app.serialize('M', 'P', 5) in state_data)

        # 3
        event_data = [
            app.serialize('P', 'L', 12),
            app.serialize('M', 'L', 12),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        ok_(app.serialize('P', 'L', 2) in state_data)
        ok_(app.serialize('M', 'L', 2) in state_data)
        ok_(app.serialize('E', 'P', 10) in state_data)
        ok_(app.serialize('E', 'M', 10) in state_data)
        ok_(app.serialize('M', 'P', 5) in state_data)

        # 4
        event_data = [
            app.serialize('P', 'E', 7),
            app.serialize('L', 'E', 7),
            app.serialize('M', 'E', 7),
        ]
        response = self.app.post('/event', data=dict(data=json.dumps(event_data)))
        state_data = json.loads(response.data)

        ok_(app.serialize('E', 'P', 3) in state_data)
        ok_(app.serialize('L', 'E', 7) in state_data)
        ok_(app.serialize('E', 'M', 3) in state_data)
        ok_(app.serialize('P', 'L', 2) in state_data)
        ok_(app.serialize('M', 'L', 2) in state_data)
        ok_(app.serialize('M', 'P', 5) in state_data)


if __name__ == '__main__':
    unittest.main()
