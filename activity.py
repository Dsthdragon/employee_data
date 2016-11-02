import functools
from PyQt5 import QtCore, QtGui, QtWidgets


class activity():
    def __init__(self, parent):
        super(activity, self).__init__()
        self.parent = parent

    def search(self, value):
        self.activityPage(value.text())

    def activityPage(self, value = None):
        body = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(body)
        mainLayout.addWidget(QtWidgets.QLabel("<font size=20><center>ACTIVITY LIST</center></font>"))

        #Search

        searchLayout = QtWidgets.QGridLayout()
        searchValue = QtWidgets.QLineEdit()
        if value:
            searchValue.setText(value)
        searchValue.setPlaceholderText("Activity Search...")

        searchBtn = QtWidgets.QPushButton()
        searchBtn.setText("FIND")
        searchBtn.clicked.connect(functools.partial(self.search, searchValue))

        searchLayout.addWidget(searchValue, 0,1,1,1)
        searchLayout.addWidget(searchBtn, 0,2,1,1)

        mainLayout.addLayout(searchLayout)
        activities = self.parent.db.getActivity(value)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(activities))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(False)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'TITLE: ', 'DATE: ', ""]:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in activities:
            staff = self.parent.db.getUser(row['staffId'])
            staff = staff['name']
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(staff)

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['shortDesc'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(row['dateAdded'])

            modify = QtWidgets.QPushButton("FULL")
            modify.clicked.connect(functools.partial(self.parent.usersPage.fullActivity, row['id'], 'activity', value))
            table.setCellWidget(y, 3, modify)

            y+=1

        mainLayout.addWidget(table)

        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)


        btnLayout.addWidget(homeBtn)

        mainLayout.addLayout(btnLayout)

        self.parent.setCentralWidget(body)
