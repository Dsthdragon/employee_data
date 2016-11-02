import functools
import os
import shutil
import random
import string
import camera

from PyQt5 import QtCore, QtGui, QtWidgets

class users():
    def __init__(self, parent):
        super(users, self).__init__()
        self.cameraClass = camera.Camera()
        self.parent = parent


    def search(self, value):
        self.usersPage(value.text())

    def usersPage(self, value = None):
        body = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(body)
        mainLayout.addWidget(QtWidgets.QLabel("<font size=20><center>STAFF LIST</center></font>"))

        #Search

        searchLayout = QtWidgets.QGridLayout()
        searchValue = QtWidgets.QLineEdit()
        if value:
            searchValue.setText(value)
        searchValue.setPlaceholderText("Staff Search...")

        searchBtn = QtWidgets.QPushButton()
        searchBtn.setText("FIND")
        searchBtn.clicked.connect(functools.partial(self.search, searchValue))

        searchLayout.addWidget(searchValue, 0,1,1,1)
        searchLayout.addWidget(searchBtn, 0,2,1,1)

        mainLayout.addLayout(searchLayout)

        #Table
        _data = self.parent.db.getUsers(value)
        table = QtWidgets.QTableWidget()
        table.setColumnCount(8)
        table.setRowCount(len(_data))
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
        for i in ['NAME: ', 'EMAIL: ', 'PHONE :', 'GENDER: ', 'DATE OF BIRTH: ', 'STATE: ', 'L.G.A: ', ""]:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in _data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['name'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['email'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(row['phone'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 3, content)
            contentitem = table.item(y, 3)
            contentitem.setText(str(row['gender']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 4, content)
            contentitem = table.item(y, 4)
            contentitem.setText(str(row['dob']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 5, content)
            contentitem = table.item(y, 5)
            contentitem.setText(str(row['state']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 6, content)
            contentitem = table.item(y, 6)
            contentitem.setText(str(row['lga']))

            modify = QtWidgets.QPushButton("VIEW")
            modify.clicked.connect(functools.partial(self.viewUser, row['id']))
            table.setCellWidget(y, 7, modify)

            y+=1

        mainLayout.addWidget(table)

        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)

        newBtn = QtWidgets.QPushButton();
        newBtn.setFixedSize(200, 50)
        newBtn.setText("NEW")
        newBtn.clicked.connect(self.newUser)

        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(newBtn)

        mainLayout.addLayout(btnLayout)

        self.parent.setCentralWidget(body)

    def viewUser(self, _id):
        body = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(body)

        _data = self.parent.db.getUser(_id)
        header = QtWidgets.QLabel("<font size=10><center>PROFILE</center></font>");
        header.setFixedHeight(50)
        mainLayout.addWidget(header)

        profile = QtWidgets.QGridLayout()

        profile.addWidget(QtWidgets.QLabel("NAME: "), 0, 0)
        profile.addWidget(QtWidgets.QLabel("EMAIL: "), 1, 0)
        profile.addWidget(QtWidgets.QLabel("PHONE: "), 2, 0)
        profile.addWidget(QtWidgets.QLabel("DATE OF BIRTH: "), 3, 0)
        profile.addWidget(QtWidgets.QLabel("GENDER: "), 4, 0)
        profile.addWidget(QtWidgets.QLabel("ADDRESS: "), 5, 0)
        profile.addWidget(QtWidgets.QLabel("STATE: "), 6, 0)
        profile.addWidget(QtWidgets.QLabel("LGA: "), 7, 0)
        profile.addWidget(QtWidgets.QLabel("DATE OF EMPLOYMENT: "), 8,0)
        profile.addWidget(QtWidgets.QLabel("DESIGNATION: "), 9,0)
        profile.addWidget(QtWidgets.QLabel("LEVEL: "), 10,0)

        profile.addWidget(QtWidgets.QLabel(str(_data['name'])), 0, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['email'])), 1, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['phone'])), 2, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['dob'])), 3, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['gender'])), 4, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['address'])), 5, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['state'])), 6, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['lga'])), 7, 1)
        profile.addWidget(QtWidgets.QLabel(str(_data['doe'])), 8,1)
        profile.addWidget(QtWidgets.QLabel(str(_data['designation'])), 9,1)
        profile.addWidget(QtWidgets.QLabel(str(_data['level'])), 10,1)

        photo_holder = QtWidgets.QLabel()
        photo_holder.setFixedSize(300, 300)
        if os.path.exists(_data['picture']):
            image = QtGui.QPixmap(_data['picture'])
        else:
            image = QtGui.QPixmap(os.getcwd()+_data['picture'])

        newimage = image.scaled(photo_holder.size(), QtCore.Qt.KeepAspectRatio)
        photo_holder.setAlignment(QtCore.Qt.AlignCenter)
        photo_holder.setPixmap(newimage)

        profile.addWidget(photo_holder,0,2,10,1)



        mainLayout.addLayout(profile)

        #Table
        activities = self.parent.db.staffActivity(_data['id'])

        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
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
        for i in ['TITLE: ', 'DATE: ', ""]:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in activities:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['shortDesc'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['dateAdded'])

            modify = QtWidgets.QPushButton("FULL")
            modify.clicked.connect(functools.partial(self.fullActivity, row['id'], 'user'))
            table.setCellWidget(y, 2, modify)

            y+=1

        mainLayout.addWidget(table)

        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)

        backBtn = QtWidgets.QPushButton();
        backBtn.setFixedSize(200, 50)
        backBtn.setText("BACK")
        backBtn.clicked.connect(self.usersPage)

        activityBtn = QtWidgets.QPushButton();
        activityBtn.setFixedSize(200, 50)
        activityBtn.setText("ADD ACTIVITY")
        activityBtn.clicked.connect(functools.partial(self.addActivity, _data['id']))

        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(backBtn)
        btnLayout.addWidget(activityBtn)

        mainLayout.addLayout(btnLayout)
        self.parent.setCentralWidget(body)

    def newUser(self):
        body = QtWidgets.QWidget(self.parent)

        mainLayout = QtWidgets.QVBoxLayout(body)
        header = QtWidgets.QLabel("<font size=15><center>NEW STAFF</center></font>")
        header.setFixedHeight(50)
        mainLayout.addWidget(header)
        error = QtWidgets.QLabel()
        error.setText("")
        if error.text() != "":
            mainLayout.addWidget(error)

        user = {}
        user['name'] = QtWidgets.QLineEdit()
        user['email'] = QtWidgets.QLineEdit()
        user['address'] = QtWidgets.QLineEdit()
        user['lga'] = QtWidgets.QLineEdit()
        user['designation'] = QtWidgets.QLineEdit()
        user['phone'] = QtWidgets.QLineEdit()
        user['phone'].setInputMask("00000000000")
        user['phone'].setMaxLength(11)
        user['level'] = QtWidgets.QLineEdit()


        user['dob'] = QtWidgets.QLineEdit()
        user['dob'].setReadOnly(True)



        dob = QtWidgets.QPushButton()
        dob.setText("SET DATE")
        dob.clicked.connect(functools.partial(self.showCalender, user['dob']))

        user['doe'] = QtWidgets.QLineEdit()
        user['doe'].setReadOnly(True)

        doe = QtWidgets.QPushButton()
        doe.setText("SET DATE")
        doe.clicked.connect(functools.partial(self.showCalender, user['doe']))




        user['gender'] = QtWidgets.QComboBox()
        user['state'] = QtWidgets.QComboBox()

        genders = ['Male', 'Female']
        states = [
            'Abia','Adamawa', 'Anambra', 'Awka Ibom', 'Bauchi', 'Bayelsa',
            'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Enugu',
            'Edo', 'Ekiti', 'Gombe', 'Imo', 'Jigawa', 'Kaduna',
            'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos',
            'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
            'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara', 'Other'
            ]

        user['gender'].addItems(genders)
        user['state'].addItems(states)

        user['picture'] = QtWidgets.QLineEdit()

        photoholder = QtWidgets.QLabel()
        photoholder.setMinimumWidth(300)

        imgBtn = QtWidgets.QPushButton()
        imgBtn.setText("IMAGE UPLOAD")
        imgBtn.setFixedSize(150, 40)
        imgBtn.clicked.connect(functools.partial(self.image_option, photoholder, user['picture']))




        newForm =QtWidgets.QGridLayout()

        newForm.addWidget(QtWidgets.QLabel("NAME: "), 0, 0)
        newForm.addWidget(user['name'], 0, 1, 1, 2)
        newForm.addWidget(imgBtn, 0, 3, 1, 1, QtCore.Qt.AlignCenter)




        newForm.addWidget(QtWidgets.QLabel("GENDER: "),1, 0)
        newForm.addWidget(user['gender'], 1, 1, 1, 2)
        newForm.addWidget(photoholder,1,3,10,1)


        newForm.addWidget(QtWidgets.QLabel("DATE OF BIRTH: "), 2, 0)
        newForm.addWidget(user['dob'], 2, 1)
        newForm.addWidget(dob, 2, 2)

        newForm.addWidget(QtWidgets.QLabel("PHONE NUMBER: "), 3, 0)
        newForm.addWidget(user['phone'], 3, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("EMAIL ADDRESS: "), 4, 0)
        newForm.addWidget(user['email'], 4, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("RESIDENTIAL ADDRESS: "), 5, 0)
        newForm.addWidget(user['address'], 5, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("STATE OF ORIGIN: "), 6, 0)
        newForm.addWidget(user['state'], 6, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("LGA: "), 7, 0)
        newForm.addWidget(user['lga'], 7, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("DESIGNATION: "), 8, 0)
        newForm.addWidget(user['designation'], 8, 1, 1, 2)

        newForm.addWidget(QtWidgets.QLabel("DATE OF EMPLOYMENT: "), 9, 0)
        newForm.addWidget(user['doe'], 9, 1)
        newForm.addWidget(doe, 9, 2)

        newForm.addWidget(QtWidgets.QLabel("LEVEL: "), 10, 0)
        newForm.addWidget(user['level'], 10, 1, 1, 2)

        mainLayout.addLayout(newForm)
        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)

        backBtn = QtWidgets.QPushButton();
        backBtn.setFixedSize(200, 50)
        backBtn.setText("BACK")
        backBtn.clicked.connect(self.usersPage)

        saveBtn = QtWidgets.QPushButton();
        saveBtn.setFixedSize(200, 50)
        saveBtn.setText("SAVE")
        saveBtn.clicked.connect(functools.partial(self.parent.db.saveUser, user, error))

        clearBtn = QtWidgets.QPushButton();
        clearBtn.setFixedSize(200, 50)
        clearBtn.setText("CLEAR")
        clearBtn.clicked.connect(functools.partial(self.clearNewForm, user, photoholder))


        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(backBtn)
        btnLayout.addWidget(clearBtn)
        btnLayout.addWidget(saveBtn)

        mainLayout.addLayout(btnLayout)

        self.parent.setCentralWidget(body)

    def showCalender(self, widget):
        main = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout(main)
        calender = QtWidgets.QCalendarWidget()
        _date = calender.selectedDate()

        layout.addWidget(calender)

        btnLayout = QtWidgets.QHBoxLayout()

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("CANCEL")
        cancelBtn.clicked.connect(main.close)


        okBtn = QtWidgets.QPushButton()
        okBtn.setText("OK")

        okBtn.clicked.connect(functools.partial(self.setDate, widget, calender, main))

        btnLayout.addWidget(cancelBtn)
        btnLayout.addWidget(okBtn)

        layout.addLayout(btnLayout)

        main.exec_()

    def setDate(self, _widget, _calender, _dialog):
        _date = _calender.selectedDate()
        _newDate = str(_date.day())+"/"+str(_date.month())+"/"+str(_date.year())
        _widget.setText(_newDate)
        _dialog.close()

    def clearNewForm(self, user, photoholder):
        try:
            if user['picture']:
                os.remove(user['picture'].text())
        except FileNotFoundError as e:
            pass
        user['dob'].clear()
        user['level'].clear()
        user['doe'].clear()
        user['gender'].setCurrentText("Male")
        user['picture'].clear()
        user['state'].setCurrentText("Abia")
        user['email'].clear()
        user['name'].clear()
        user['lga'].clear()
        user['phone'].clear()
        user['address'].clear()
        user['designation'].clear()

        photoholder.clear()

    def image_option(self, photoholder, link):
        main = QtWidgets.QDialog()
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        main.resize(500, 300)
        layout = QtWidgets.QVBoxLayout(main)
        hLayout = QtWidgets.QHBoxLayout()
        layout.addWidget(QtWidgets.QLabel("<h3><center>SELECT IMAGE UPLOAD OPTION</center></h3>"))

        filedialog = QtWidgets.QPushButton()
        filedialog.setText("FILES")
        filedialog.setFixedSize(150, 40)
        filedialog.clicked.connect(functools.partial(self.get_image, photoholder, link))
        hLayout.addWidget(filedialog)

        camera = QtWidgets.QPushButton()
        camera.setText("CAMERA")
        camera.setFixedSize(150, 40)
        camera.clicked.connect(functools.partial(self.cameraClass.start, photoholder, link, main))

        layout.addLayout(hLayout)
        hLayout.addWidget(camera)
        main.exec_()

    def get_image(self, photo_holder, link):
        Holder = QtWidgets.QWidget()
        fname, ok = QtWidgets.QFileDialog.getOpenFileName(Holder, 'Open file', '.',

                                                               "Image files (*.jpg *.gif *.jpeg *.png)")
        if fname:

            ext = fname.split(".")
            ext = ext[len(ext)-1]
            newRandom = random.SystemRandom()
            newName = ''.join(newRandom.choice(string.ascii_uppercase + string.digits) for _ in range(random.randrange(20,30) ))
            sep = os.sep
            newlink = os.getcwd()+""+sep+"data"+sep+"tmp"+sep+newName+"."+ext
            link.setText(newlink)

            shutil.copy(fname, newlink)
            image = QtGui.QPixmap(newlink)
            newimage = image.scaled(photo_holder.size(), QtCore.Qt.KeepAspectRatio)
            photo_holder.setAlignment(QtCore.Qt.AlignCenter)
            photo_holder.setPixmap(newimage)

    def addActivity(self, _id):
        body = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(body)
        mainLayout.addWidget(QtWidgets.QLabel("<font size=5><center>ADD ACTIVITY</center></font>"))

        _error = QtWidgets.QLabel()
        _error.setText("")
        mainLayout.addWidget(_error)

        activity = {'staffId': _id}
        activity['shortDesc'] = QtWidgets.QPlainTextEdit()
        activity['shortDesc'].setMaximumHeight(50)
        activity['date'] = QtWidgets.QLabel()

        dob = QtWidgets.QPushButton()
        dob.setText("SET DATE")
        dob.clicked.connect(functools.partial(self.showCalender, activity['date']))

        activity['fullDesc'] = QtWidgets.QPlainTextEdit()
        activity['fullDesc'].setMinimumHeight(400)

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(dob, activity['date'])
        formLayout.addRow(QtWidgets.QLabel("SHORT DESCRIPTION: "), activity['shortDesc'])
        formLayout.addRow(QtWidgets.QLabel("FULL DESCRIPTION: "), activity['fullDesc'])

        mainLayout.addLayout(formLayout)

        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)

        backBtn = QtWidgets.QPushButton();
        backBtn.setFixedSize(200, 50)
        backBtn.setText("BACK")
        backBtn.clicked.connect(functools.partial(self.viewUser, _id))

        saveBtn = QtWidgets.QPushButton();
        saveBtn.setFixedSize(200, 50)
        saveBtn.setText("SAVE")
        saveBtn.clicked.connect(functools.partial(self.parent.db.addActivity, activity, _error))


        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(backBtn)
        btnLayout.addWidget(saveBtn)

        mainLayout.addLayout(btnLayout)

        self.parent.setCentralWidget(body)

    def fullActivity(self, _id, _from, _returnData = None):
        body = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout(body)
        header = QtWidgets.QLabel("<font size=10><center>Activity</center></font>");
        header.setFixedHeight(50)
        mainLayout.addWidget(header)
        seperater = QtWidgets.QFrame()
        seperater.setFrameStyle(QtWidgets.QFrame.HLine)

        mainLayout.addWidget(seperater)

        _data = self.parent.db.fullActivity(_id)
        staffData = self.parent.db.getUser(_data['staffID'])
        name = QtWidgets.QLabel("STAFF: "+ staffData['name'])
        _date = QtWidgets.QLabel("DATE: "+ str(_data['dateAdded']))
        full = QtWidgets.QLabel(_data['fullDesc'])
        full.setAlignment(QtCore.Qt.AlignTop)
        full.setWordWrap(True)

        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.ensureWidgetVisible(full)
        #scroll.setHorizontalScrollBar(QtWidgets.QScrollBar)
        scroll.setWidget(full)

        mainLayout.addWidget(name)
        mainLayout.addWidget(_date)
        mainLayout.addWidget(scroll)

        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton();
        homeBtn.setFixedSize(200, 50)
        homeBtn.setText("HOME")
        homeBtn.clicked.connect(self.parent.startPage)

        backBtn = QtWidgets.QPushButton();
        backBtn.setFixedSize(200, 50)
        backBtn.setText("BACK")
        if _from == "user":
            backBtn.clicked.connect(functools.partial(self.viewUser, staffData['id']))
        elif _from == 'activity':
            backBtn.clicked.connect(functools.partial(self.parent.activity.activityPage, _returnData))

        activityBtn = QtWidgets.QPushButton();
        activityBtn.setFixedSize(200, 50)
        activityBtn.setText("ADD ACTIVITY")
        activityBtn.clicked.connect(functools.partial(self.addActivity, _data['id']))

        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(backBtn)
        btnLayout.addWidget(activityBtn)

        mainLayout.addLayout(btnLayout)

        self.parent.setCentralWidget(body)
