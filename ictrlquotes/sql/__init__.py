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

import sys
import os

from PyQt4.QtGui import QMessageBox

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from ConfigParser import SafeConfigParser

# path to ~/.config/ictrlquotes.cfg
configfile = os.path.join(os.path.expanduser('~'),
                          '.config',
                          'ictrlquotes.cfg')
parser = SafeConfigParser()
try:
    # try parsing out information out of config
    parser.read(configfile)
    sql_user = parser.get('sql', 'sql_user')
    sql_url = parser.get('sql', 'sql_url')
    sql_pw = parser.get('sql', 'sql_pw')
    sql_db = parser.get('sql', 'sql_db')
    usedefaults = False
except Exception:
    usedefaults = True
if usedefaults:
    # if any errors occured during parsing, replace config file with defaults.
    open(configfile, 'w+').close()
    parser.read(configfile)
    parser.add_section('sql')
    sql_user = 'quote_user'
    sql_url = '172.25.2.7'
    sql_pw = 'ictrl'
    sql_db = 'ictrl'
    parser.set('sql', 'sql_user', sql_user)
    parser.set('sql', 'sql_url', sql_url)
    parser.set('sql', 'sql_pw', sql_pw)
    parser.set('sql', 'sql_db', sql_db)
    with open(configfile, 'w') as dump:
        parser.write(dump)

Base = declarative_base()
engine = create_engine('mysql://' + sql_user + ':' +
                       sql_pw +
                       '@' + sql_url + '/' +
                       sql_db + '?charset=utf8',
                       echo=False)

try:
    connection = engine.connect()
    connection.execute("SELECT 1")
    connection.close()
except Exception as e:
    msg = QMessageBox()
    msg.setText("Could not connect to database: " + e.args[0])
    msg.exec_()
    sys.exit(0)

Session = sessionmaker(bind=engine)


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


def add_author(session, new_firstname, new_lastname):
    new_author = Author(firstname=new_firstname, lastname=new_lastname)
    session.add(new_author)
    session.commit()
    for author in session.query(Author).order_by(Author.id):
        if author is new_author:
            return author.id


def del_author(session, authorid):
    author = session.query(Author).get(authorid)
    session.delete(author)
    session.commit()


def add_quote(session, new_text, authorid):
    new_quote = Quote(text=new_text, author=authorid)
    session.add(new_quote)
    session.commit()
    for quote in session.query(Quote).order_by(Quote.id):
        if quote is new_quote:
            return quote.id


def del_quote(session, quoteid):
    quote = session.query(Quote).get(quoteid)
    try:
        session.delete(quote)
    except:
        # Quote had already been deleted
        pass
    session.commit()


def get_authors(session):
    author_query = session.query(Author).order_by(Author.id)
    return author_query.all()


def get_quotes(session):
    quote_query = session.query(Quote).order_by(Quote.id)
    return quote_query.all()
