#!/usr/bin/env python
import json

from flask import Flask, abort, make_response, request
app = Flask(__name__)


STATE = {}

def add_debt(from_, to, amount):
    if from_ > to:
        amount *= -1
        from_, to = to, from_
    tup = (from_, to)
    STATE[tup] = STATE.get(tup, 0) + amount


def serialize(from_, to, amount):
    return {"from": from_, "to": to, "amount": amount}


@app.route("/event", methods=['POST'])
def event():
    data = json.loads(request.data)
    for debt in data:
        add_debt(debt['from'], debt['to'], debt['amount'])

    current_debts = []
    for (from_, to), amount in STATE.items():
        if amount < 0:
            from_, to = to, from_
            amount *= -1
        row = serialize(from_, to, amount)
        current_debts.append(row)

    response = make_response(json.dumps(current_debts))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    #return json.dumps(current_debts)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
