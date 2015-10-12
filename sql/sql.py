#!/usr/bin/env python
# ictrl_quotes. Created on 08.10.2015
# Copyright (C) 2014 Andreas Schulz <andreas.schulz@frm2.tum.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 US

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

    quotes = relationship('Quote',
                          backref=backref('full_author', order_by=id),
                          cascade="all, delete, delete-orphan")

    def __repr__(self):
        return ("<Author(firstname='%s', lastname='%s')>" % (
            self.firstname, self.lastname)).encode('utf-8')


class Quote(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    author = Column(Integer, ForeignKey('author.id'))

    def __repr__(self):
        return ("<Quote(text='%s')>" % self.text).encode('utf-8')


def add_author(new_firstname, new_lastname):
    new_author = Author(firstname=new_firstname, lastname=new_lastname)
    session.add(new_author)
    session.commit()
    for author in session.query(Author).order_by(Author.id):
        if author is new_author:
            return author.id


def del_author(authorid):
    author = session.query(Author).get(authorid)
    session.delete(author)
    session.commit()


def add_quote(new_text, authorid):
    new_quote = Quote(text=new_text, author=authorid)
    session.add(new_quote)
    session.commit()
    for quote in session.query(Quote).order_by(Quote.id):
        if quote is new_quote:
            return quote.id


def del_quote(quoteid):
    quote = session.query(Quote).get(quoteid)
    session.delete(quote)
    session.commit()


def get_authors():
    author_query = session.query(Author).order_by(Author.id)
    return author_query.all()


def get_quotes():
    quote_query = session.query(Quote).order_by(Quote.id)
    return quote_query.all()
