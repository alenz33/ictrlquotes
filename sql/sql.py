from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

Base = declarative_base()
engine = create_engine('mysql://quote_user:' +
                       'ictrl' +
                       '@172.25.2.7/ictrl?charset=utf8',
                       echo=False)
Session = sessionmaker(bind=engine)
session = Session()


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)

    def __repr__(self):
        return ("<Author(firstname='%s', lastname='%s')>" % (
            self.firstname, self.lastname)).encode('utf-8')


class Quote(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    author = Column(Integer, ForeignKey('author.id'))

    full_author = relationship(
        "Author", backref=backref('quotes', order_by=id))

    def __repr__(self):
        return ("<Quote(text='%s')>" % self.text).encode('utf-8')


# andi = author(firstname="Andreas", lastname="Schulz")
# session.add(andi)
# session.commit()

def get_users():
    author_query = session.query(Author).order_by(Author.id)
    return author_query.all()


def get_quotes():
    quote_query = session.query(Quote).order_by(Quote.id)
    return quote_query.all()
