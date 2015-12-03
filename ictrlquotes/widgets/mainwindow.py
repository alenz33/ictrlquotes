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

import os

from PyQt4 import uic
from PyQt4.QtGui import QMainWindow, QInputDialog

from ictrlquotes.utilities import getResourcesPath
from ictrlquotes.sql.sql import get_authors
from ictrlquotes.sql.sql import add_author as sql_add_author
from ictrlquotes.sql.sql import del_author as sql_del_author
from ictrlquotes.sql.sql import add_quote as sql_add_quote
from ictrlquotes.sql.sql import del_quote as sql_del_quote
from authoritem import AuthorItem
from quoteitem import QuoteItem
from addauthordialog import AddAuthorDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi(os.path.join(getResourcesPath(), 'widgets',
                                                    'ui', 'mainwindow.ui'),
                   self)
        # connections
        self.actionExit.triggered.connect(self.close)
        self.authorsListWidget.itemClicked.connect(self.author_selected)
        self.quotesListWidget.itemClicked.connect(self.quote_selected)
        self.addAuthorPushButton.clicked.connect(self.add_author)
        self.deleteAuthorPushButton.clicked.connect(self.del_author)
        self.addQuotePushButton.clicked.connect(self.add_quote)
        self.deleteQuotePushButton.clicked.connect(self.del_quote)

        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([250, 500])
        for author in get_authors():
            self.authorsListWidget.addItem(AuthorItem(
                (author.firstname + ' ' + author.lastname),
                author.id,
                self.authorsListWidget))

    def author_selected(self, authorItem):
        self.quotesListWidget.clear()
        self.deleteQuotePushButton.setEnabled(False)
        self.addQuotePushButton.setEnabled(True)
        self.deleteAuthorPushButton.setEnabled(True)
        for author in get_authors():
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
            id = sql_add_author(fn, ln)
            self.authorsListWidget.addItem(AuthorItem(fn + ' ' + ln,
                                                      id,
                                                      self.authorsListWidget))

    def del_author(self):
        author = self.authorsListWidget.currentItem()
        row = self.authorsListWidget.row(author)
        sql_del_author(author.authorid)
        self.quotesListWidget.clear()
        self.authorsListWidget.takeItem(row)
        if not self.authorsListWidget.count():
            self.deleteAuthorPushButton.setEnabled(False)
            self.addQuotePushButton.setEnabled(False)
            self.deleteQuotePushButton.setEnabled(False)

    def add_quote(self):
        (text, answer) = QInputDialog.getText(self, 'Add new quote', 'Quote:')
        if answer:
            authorid = self.authorsListWidget.currentItem().authorid
            quoteid = sql_add_quote(text, authorid)
            self.quotesListWidget.addItem(QuoteItem(
                text, quoteid, self.quotesListWidget))

    def del_quote(self):
        quote = self.quotesListWidget.currentItem()
        row = self.quotesListWidget.row(quote)
        sql_del_quote(quote.quoteid)
        self.quotesListWidget.takeItem(row)
        if not self.quotesListWidget.count():
            self.deleteQuotePushButton.setEnabled(False)
