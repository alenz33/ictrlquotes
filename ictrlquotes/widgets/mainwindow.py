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

from PyQt4 import uic
from PyQt4.QtGui import QMainWindow, QInputDialog, QIcon, QPixmap

from ictrlquotes.utilities import projectpath_join
from ictrlquotes.sql import get_authors, get_quotes, Session
from ictrlquotes.sql import add_author as sql_add_author
from ictrlquotes.sql import del_author as sql_del_author
from ictrlquotes.sql import add_quote as sql_add_quote
from ictrlquotes.sql import del_quote as sql_del_quote
from authoritem import AuthorItem
from quoteitem import QuoteItem
from addauthordialog import AddAuthorDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(projectpath_join('widgets', 'ui', 'mainwindow.ui'), self)
        # SQL session
        self.session = Session()

        # connections
        self.actionExit.triggered.connect(self.close)
        self.authorsListWidget.itemClicked.connect(self.author_selected)
        self.quotesListWidget.itemClicked.connect(self.quote_selected)
        self.addAuthorPushButton.clicked.connect(self.add_author)
        self.deleteAuthorPushButton.clicked.connect(self.del_author)
        self.addQuotePushButton.clicked.connect(self.add_quote)
        self.deleteQuotePushButton.clicked.connect(self.del_quote)

        # toolbar
        self.actionRefresh.setIcon(QIcon(QPixmap(
            projectpath_join('res/reload.png'))))
        self.actionRefresh.triggered.connect(self.updateAuthorWidget)

        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([250, 500])
        self.updateAuthorWidget()

    def session_reinit(self):
        self.session = None
        self.session = Session()

    def updateAuthorWidget(self):
        self.session_reinit()
        authors = get_authors(self.session)
        authorids = [author.id for author in authors]
        needQuoteUpdate = True

        # check if there are authors in db without a QListWidgetItem
        for author in authors:
            if self.checkIfAuthorNeedsNewItem(author.id):
                self.authorsListWidget.addItem(AuthorItem(
                    author.firstname,
                    author.lastname,
                    author.id,
                    self.authorsListWidget))

        # check if there are QListWidgetItems without an author in db
        for authorItem in [self.authorsListWidget.item(row) for row
                           in range(self.authorsListWidget.count())]:
            if authorItem.authorid not in authorids:
                if self.authorsListWidget.currentItem() is not None:
                    if authorItem.authorid\
                            == self.authorsListWidget.currentItem().authorid:
                        # the item that is currently selected is being deleted.
                        self.quotesListWidget.clear()
                        needQuoteUpdate = False
                        self.addQuotePushButton.setEnabled(False)
                        self.deleteQuotePushButton.setEnabled(False)
                        self.deleteAuthorPushButton.setEnabled(False)
                row = self.authorsListWidget.row(authorItem)
                self.authorsListWidget.takeItem(row)
                self.authorsListWidget.clearSelection()

        self.authorsListWidget.sortItems()
        if self.authorsListWidget.currentItem() is not None:
            if needQuoteUpdate:
                self.updateQuoteWidget(
                    self.authorsListWidget.currentItem().authorid)

    def updateQuoteWidget(self, authorid):
        self.session_reinit()
        author = [author for author in
                  get_authors(self.session) if author.id == authorid][0]
        all_quotes = get_quotes(self.session)
        quotes = [quote for quote in all_quotes if quote.author == author.id]
        quoteids = [quote.id for quote in quotes]

        # check if there are quotes in db without a QListWidgetItem
        for quote in quotes:
            if self.checkIfQuoteNeedsNewItem(quote.id):
                self.quotesListWidget.addItem(QuoteItem(
                    quote.text,
                    quote.id,
                    self.quotesListWidget))

        # check if there are QListWidgetItems without an quote in db
        for quoteItem in [self.quotesListWidget.item(row) for row
                          in range(self.quotesListWidget.count())]:
            if quoteItem.quoteid not in quoteids:
                if self.quotesListWidget.currentItem() is not None:
                    if quoteItem.quoteid\
                            == self.quotesListWidget.currentItem().quoteid:
                        # the item that is currently selected is being deleted.
                        self.deleteQuotePushButton.setEnabled(False)
                row = self.quotesListWidget.row(quoteItem)
                self.quotesListWidget.takeItem(row)
                self.quotesListWidget.clearSelection()

        self.quotesListWidget.sortItems()

    def checkIfAuthorNeedsNewItem(self, authorid):
        for authorItem in [self.authorsListWidget.item(row) for row
                           in range(self.authorsListWidget.count())]:
            if authorItem.authorid == authorid:
                return False
        return True

    def checkIfQuoteNeedsNewItem(self, quoteid):
        for quoteItem in [self.quotesListWidget.item(row) for row
                          in range(self.quotesListWidget.count())]:
            if quoteItem.quoteid == quoteid:
                return False
        return True

    def author_selected(self, authorItem):
        self.quotesListWidget.clear()
        self.deleteQuotePushButton.setEnabled(False)
        self.addQuotePushButton.setEnabled(True)
        self.deleteAuthorPushButton.setEnabled(True)
        self.session_reinit()
        for author in get_authors(self.session):
            if author.id == authorItem.authorid:
                for quote in author.quotes:
                    self.quotesListWidget.addItem(QuoteItem(
                        quote.text, quote.id, self.quotesListWidget))

    def quote_selected(self, quoteItem):
        self.deleteQuotePushButton.setEnabled(True)

    def add_author(self):
        dlg = AddAuthorDialog()
        result = dlg.exec_()
        if result:
            fn = dlg.firstNameLineEdit.text()
            ln = dlg.lastNameLineEdit.text()
            self.session_reinit()
            id = sql_add_author(self.session, fn, ln)
            self.authorsListWidget.addItem(AuthorItem(fn,
                                                      ln,
                                                      id,
                                                      self.authorsListWidget))

    def del_author(self):
        author = self.authorsListWidget.currentItem()
        row = self.authorsListWidget.row(author)
        self.session_reinit()
        sql_del_author(self.session, author.authorid)
        self.quotesListWidget.clear()
        self.authorsListWidget.takeItem(row)
        if not self.authorsListWidget.count():
            self.deleteAuthorPushButton.setEnabled(False)
            self.addQuotePushButton.setEnabled(False)
            self.deleteQuotePushButton.setEnabled(False)
        self.authorsListWidget.clearSelection()

    def add_quote(self):
        (text, answer) = QInputDialog.getText(self, 'Add new quote', 'Quote:')
        if answer:
            authorid = self.authorsListWidget.currentItem().authorid
            self.session_reinit()
            quoteid = sql_add_quote(self.session, text, authorid)
            self.quotesListWidget.addItem(QuoteItem(
                text, quoteid, self.quotesListWidget))

    def del_quote(self):
        quote = self.quotesListWidget.currentItem()
        row = self.quotesListWidget.row(quote)
        self.session_reinit()
        sql_del_quote(self.session, quote.quoteid)
        self.quotesListWidget.takeItem(row)
        if not self.quotesListWidget.count():
            self.deleteQuotePushButton.setEnabled(False)
