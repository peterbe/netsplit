from sqlalchemy import Column, Integer, String, Numeric
from netsplit.database import Base


class Debt(Base):
    __tablename__ = 'debts'
    id = Column(Integer, primary_key=True)
    from_ = Column('from', String(200), nullable=False)
    to = Column(String(200), nullable=False)
    amount = Column(Numeric(precision=2), nullable=False)

    def __init__(self, from_, to, amount):
        self.from_ = from_
        self.to = to
        self.amount = amount

    def __repr__(self):
        return '<Debt %r owes %r %.2f>' % (self.from_, self.to, self.amount)


class Key(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    email = Column('from', String(200), nullable=False)
    key = Column(String(100), nullable=False)

    def __init__(self, email, key):
        self.email = email
        self.key = key

    def __repr__(self):
        return '<Key %r (%r)>' % (self.email, self.key)
