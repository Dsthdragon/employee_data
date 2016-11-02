# default imports
import sys
import datetime
import os

# custom imports
import users
import database
import activity

# PyQt5 imports
from PyQt5 import QtCore, QtGui, QtWidgets

class Staff_data(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Staff_data, self).__init__(parent)
        sep = os.sep
        tempdir = os.getcwd()+""+sep+"data"+sep+"tmp"+sep
        for f in os.listdir(tempdir):
            os.remove(tempdir+f)

        #self.centralWidget = QtWidgets.QWidget(self)

        # set paging systems
        self.db = database.database(self)
        self.usersPage = users.users(self)
        self.activity = activity.activity(self)
        #self.setWindowIcon
        self.showFullScreen()
        self.setWindowTitle("Staff Data")
        self.startPage()

    def startPage(self):
        self.centralWidget = QtWidgets.QWidget(self)
        mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        banner = QtWidgets.QLabel()
        #banner.setMaximumHeight(300)
        sep = os.sep
        tempLink = os.getcwd()+""+sep+"data"+sep+"images"+sep+"banner.jpg"
        image = QtGui.QPixmap(tempLink)
        newImage = image.scaled(banner.size(), QtCore.Qt.KeepAspectRatio)

        banner.setAlignment(QtCore.Qt.AlignCenter)
        banner.setScaledContents(True)
        banner.setPixmap(newImage)
        mainLayout.addWidget(banner)

        btnLayout = QtWidgets.QGridLayout()

        userBtn = QtWidgets.QPushButton()
        userBtn.setFixedSize(200, 50)
        userBtn.clicked.connect(self.usersPage.usersPage)
        userBtn.setText("USERS")

        activityBtn = QtWidgets.QPushButton()
        activityBtn.setFixedSize(200, 50)
        activityBtn.clicked.connect(self.activity.activityPage)
        activityBtn.setText("ACTIVITIES")

        changePassBtn = QtWidgets.QPushButton()
        changePassBtn.setFixedSize(200, 50)
        changePassBtn.setText("CHANGE PASSWORD")

        aboutBtn = QtWidgets.QPushButton()
        aboutBtn.setFixedSize(200, 50)
        aboutBtn.clicked.connect(self.aboutApp)
        aboutBtn.setText("ABOUT")

        rmcoBtn = QtWidgets.QPushButton()
        rmcoBtn.setFixedSize(200, 50)
        rmcoBtn.clicked.connect(self.aboutRmco)
        rmcoBtn.setText("RMCO")

        exitBtn = QtWidgets.QPushButton()
        exitBtn.setFixedSize(200, 50)
        exitBtn.clicked.connect(self.close)
        exitBtn.setText("EXIT")

        btnLayout.addWidget(userBtn, 0, 0, 1, 1)
        btnLayout.addWidget(activityBtn, 0, 1, 1, 1)
        btnLayout.addWidget(changePassBtn, 0, 2, 1, 1)
        btnLayout.addWidget(aboutBtn, 1, 0, 1, 1)
        btnLayout.addWidget(rmcoBtn, 1, 1, 1, 1)
        btnLayout.addWidget(exitBtn, 1, 2, 1, 1)

        mainLayout.addLayout(btnLayout)

        self.setCentralWidget(self.centralWidget)

    def closeEvent(self, event):
        message = QtWidgets.QMessageBox()
        message.setText("Are you sure you want to exit?")
        message.setIcon(QtWidgets.QMessageBox.Question)
        message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message.setWindowFlags(QtCore.Qt.SplashScreen)
        reply = message.exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def aboutApp(self):
        body = QtWidgets.QDialog()
        body.resize(400, 300)
        body.setWindowFlags(QtCore.Qt.SplashScreen)
        body.setWindowTitle("About RMCO")
        grid = QtWidgets.QVBoxLayout(body)

        label = QtWidgets.QLabel()
        label.setText("<font size=15>STAFF MONITOR</font>")
        label.setAlignment(QtCore.Qt.AlignCenter)
        message = QtWidgets.QLabel("This is a staff monitoring app design by <font color=red>RMCO</font> to store staff data and activity")
        message.setWordWrap(True)
        closeBtn = QtWidgets.QPushButton()
        closeBtn.setText("CLOSE")
        closeBtn.clicked.connect(body.close)
        closeBtn.setFixedSize(200, 50)
        grid.addWidget(label)
        grid.addWidget(message)
        grid.addWidget(closeBtn,1, QtCore.Qt.AlignCenter)

        body.exec_()
    

    def aboutRmco(self):
        body = QtWidgets.QDialog()
        body.resize(400, 200)
        body.setWindowFlags(QtCore.Qt.SplashScreen)
        body.setWindowTitle("About RMCO")
        grid = QtWidgets.QVBoxLayout(body)
        sep = os.sep
        tempLink = os.getcwd()+""+sep+"data"+sep+"images"+sep+"rmcologo.png"
        image = QtGui.QPixmap(tempLink)
        newimage = image.scaled(QtCore.QSize(300,200), QtCore.Qt.KeepAspectRatio)
        photoholder = QtWidgets.QLabel(body)
        photoholder.setText("")
        photoholder.setAlignment(QtCore.Qt.AlignCenter)
        photoholder.setPixmap(image)
        grid.addWidget(photoholder, 1)
        label = QtWidgets.QLabel()
        label.setText("<font size=15>Powered by </font><font size=15 color=red>RMCO</font>")
        label.setAlignment(QtCore.Qt.AlignCenter)
        message = QtWidgets.QLabel("Rinnas is a start up TECH company specialized in the web and software development solution.")
        message.setWordWrap(True)
        closeBtn = QtWidgets.QPushButton()
        closeBtn.setText("CLOSE")
        closeBtn.clicked.connect(body.close)
        closeBtn.setFixedSize(200, 50)
        grid.addWidget(label)
        grid.addWidget(message)
        grid.addWidget(closeBtn,1, QtCore.Qt.AlignCenter)
        body.exec_()

    def errorReport(self, _message):
        message = QtWidgets.QMessageBox()
        message.setText("Error: " + _message)
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.setWindowFlags(QtCore.Qt.SplashScreen)
        message.exec_()
        sys.exit()

app = QtWidgets.QApplication(sys.argv)
window = Staff_data()
window.show()
app.exec_()
