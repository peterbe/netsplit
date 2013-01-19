import app

def test_add_debt():
    func = app.add_debt
    app.add_debt('E', 'P', 10)
    assert app.STATE[('E', 'P')] == 10

    app.add_debt('P', 'E', 7)
    assert app.STATE[('E', 'P')] == 3

    app.add_debt('P', 'E', 2)
    assert app.STATE[('E', 'P')] == 1

    app.add_debt('P', 'E', 4)
    assert app.STATE[('E', 'P')] == -3
