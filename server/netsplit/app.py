#!/usr/bin/env python
import json

from flask import Flask, abort, make_response, request

DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('NETSPLIT_SETTINGS', silent=True)

from netsplit.database import db_session, init_db
from netsplit.models import Debt

init_db()


@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()


def add_debt(from_, to, amount):
    if from_ > to:
        amount *= -1
        from_, to = to, from_
    tup = (from_, to)
    cur = Debt.query.filter(
        Debt.from_ == from_,
        Debt.to == to
    )
    previous = cur.first()
    if previous:
        previous.amount += amount
    else:
        d = Debt(from_, to, amount)
        db_session.add(d)
    db_session.commit()


def serialize(from_, to, amount):
    return {"from": from_, "to": to, "amount": amount}


@app.route("/state", methods=['GET'])
def state():
    current_debts = _state_to_debts(None)
    response = make_response(json.dumps(current_debts))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


def _state_to_debts(around=None):
    if around:
        raise NotImplementedError('work harder')

    current_debts = []
    for each in Debt.query.all():
        from_ = each.from_
        to = each.to
        amount = float(each.amount)
        if amount < 0:
            from_, to = to, from_
            amount *= -1
        row = serialize(from_, to, amount)
        current_debts.append(row)
    return current_debts


@app.route("/event", methods=['POST'])
def event():
    raw = request.form.get('data')
    data = json.loads(raw)
    for debt in data:
        add_debt(debt['from'], debt['to'], int(debt['amount']))

    current_debts = _state_to_debts()

    response = make_response(json.dumps(current_debts))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


#if __name__ == "__main__":
#    app.run(debug=True, host='0.0.0.0')
