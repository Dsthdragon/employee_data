# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!
import random
import string
import os
import functools

from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets, QtNetwork

class Camera(QtWidgets.QDialog):
    def __init__(self):
        super(Camera, self).__init__()
        print(Camera)

    def start(self, photoholder, link, _old):
        _old.close()
        self.photoholder = photoholder
        self.link_label = link
        self.imageLocation = ""
        self.main = QtWidgets.QDialog()
        self.main.setWindowFlags(QtCore.Qt.SplashScreen)
        self.main.resize(800, 500)

        self.layout = QtWidgets.QVBoxLayout(self.main)
        self.menuBar(self.main)
        self.imageDisplay =  QtWidgets.QLabel()
        self.imageDisplay.setFixedWidth(self.main.width()/2)
        sep = os.sep
        tempLink = os.getcwd()+""+sep+"data"+sep+"images"+sep+"images.png"
        image = QtGui.QPixmap(tempLink)
        newImage = image.scaled(self.imageDisplay.size(), QtCore.Qt.KeepAspectRatio)

        self.imageDisplay.setAlignment(QtCore.Qt.AlignCenter)
        self.imageDisplay.setScaledContents(True)
        self.imageDisplay.setPixmap(newImage)


        self.viewfinderpage = QtWidgets.QWidget()
        self.viewfinderpage.setFixedWidth(self.main.width()/2)
        self.viewfinder = QtMultimediaWidgets.QCameraViewfinder(self.viewfinderpage)
        self.hlayout = QtWidgets.QHBoxLayout()
        self.hlayout.addWidget(self.viewfinder)
        self.hlayout.addWidget(self.imageDisplay)
        self.layout.addLayout(self.hlayout)

        self.variables()
        self.horiontalLayout = QtWidgets.QHBoxLayout()

        self.closeBtn = QtWidgets.QPushButton()
        self.closeBtn.setText("CLOSE CAMERA")
        self.closeBtn.setFixedSize(200, 50)
        self.closeBtn.clicked.connect(self.closeCamera)
        self.horiontalLayout.addWidget(self.closeBtn)

        self.takeImageButton = QtWidgets.QPushButton()
        self.takeImageButton.setText("CAPTURE IMAGE")
        self.takeImageButton.setFixedSize(200, 50)
        self.takeImageButton.clicked.connect(self.takeImage)
        self.horiontalLayout.addWidget(self.takeImageButton)

        self.saveImageBtn = QtWidgets.QPushButton()
        self.saveImageBtn.setText("SAVE IMAGE")
        self.saveImageBtn.setFixedSize(200, 50)
        self.saveImageBtn.setEnabled(False)
        self.saveImageBtn.clicked.connect(self.saveImage)
        self.horiontalLayout.addWidget(self.saveImageBtn)

        self.layout.addLayout(self.horiontalLayout)
        self.main.exec_()

    def closeCamera(self):
        self.camera.stop()
        self.main.close()

    def saveImage(self):
        image = QtGui.QPixmap(self.imageLocation)
        newImage = image.scaled(self.photoholder.size(), QtCore.Qt.KeepAspectRatio)
        self.photoholder.setAlignment(QtCore.Qt.AlignCenter)
        self.photoholder.setScaledContents(True)
        self.photoholder.setPixmap(newImage)
        self.link_label.setText(self.imageLocation)
        self.closeCamera()


    def variables(self):
        self.camera = None
        self.imageCapture = None
        self.mediaRecorder = None
        self.isCapturingImage = False
        self.applicationExiting = False

        self.imageSetting = QtMultimedia.QImageEncoderSettings()
        self.audioSetting = QtMultimedia.QAudioEncoderSettings()
        self.videoSetting = QtMultimedia.QVideoEncoderSettings()
        self.videoContainerFormat = ""

        cameraDevice = QtCore.QByteArray()

        videoDevicesGroup = QtWidgets.QActionGroup(self)
        videoDevicesGroup.setExclusive(True)

        for deviceName in QtMultimedia.QCamera.availableDevices():
            description = QtMultimedia.QCamera.deviceDescription(deviceName)
            videoDeviceAction = QtWidgets.QAction(description, videoDevicesGroup)
            videoDeviceAction.setCheckable(True)
            videoDeviceAction.setData(deviceName)

            if cameraDevice.isEmpty():
                cameraDevice = deviceName
                videoDeviceAction.setChecked(True)

            self.menuDevices.addAction(videoDeviceAction)

        self.setCamera(cameraDevice)

    def setCamera(self, cameraDevice):
        if cameraDevice.isEmpty():
            self.camera = QtMultimedia.QCamera()
        else:
            self.camera = QtMultimedia.QCamera(cameraDevice)

        self.imageCapture = QtMultimedia.QCameraImageCapture(self.camera)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.stateChanged.connect(self.updateCameraState)

        #self.imageCapture.readyForCaptureChanged.connect(self.readyForCapture)
        self.imageCapture.imageCaptured.connect(self.processCapturedImage)
        self.imageCapture.imageSaved.connect(self.imageSaved)

        self.camera.start()

    def updateCameraState(self, state):
        if state == QtMultimedia.QCamera.ActiveState:
            self.actionStartCamera.setEnabled(False)
            self.actionStopCamera.setEnabled(True)
            self.actionSettings.setEnabled(True)


        elif state in (QtMultimedia.QCamera.UnloadedState, QtMultimedia.QCamera.LoadedState):
            self.actionStartCamera.setEnabled(True)
            self.actionStopCamera.setEnabled(False)
            self.actionSettings.setEnabled(False)

    def displayCameraError(self):
        QtWidgets.QMessageBox.warning(self, "Camera error", self.camera.errorString())

    def updateCameraDevice(self, action):
        self.setCamera(action.data())

    def takeImage(self):
        newRandom = random.SystemRandom()
        newName = ''.join(newRandom.choice(string.ascii_uppercase + string.digits) for _ in range(random.randrange(20,30) ))
        sep = os.sep
        link = os.getcwd()+""+sep+"data"+sep+"tmp"+sep+newName
        self.imageLocation = link+".jpg"
        self.isCapturingImage = True
        self.imageCapture.capture(link)

    def startCamera(self):
        self.camera.start()

    def stopCamera(self):
        self.camera.stop()

    def processCapturedImage(self, requestid, img):
        scaledImage = img.scaled(self.viewfinder.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.imageDisplay.setPixmap(QtGui.QPixmap.fromImage(scaledImage))
        self.saveImageBtn.setEnabled(True)
        #self.displayCapturedImage()

    def displayCapturedImage(self):
        main = QtWidgets.QDialog()
        layout = QtWidgets.QVBoxLayout(main)
        layout.addWidget(QtWidgets.QLabel("<font size=15><center>CAPTURED IMAGE</center></font>"))
        layout.addWidget(self.imageDisplay)
        main.exec_()

    #def readyForCapture(self, ready):
        #self.takeImageButton.setEnabled(ready)

    def imageSaved(self, id, fileName):
        self.isCapturingImage = False

        if self.applicationExiting:
            self.close()

    def menuBar(self, Camera):
        self.menubar = QtWidgets.QMenuBar(Camera)
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setTitle("File")

        self.menuDevices = QtWidgets.QMenu(self.menubar)
        self.menuDevices.setTitle("Devices")



        self.actionExit = QtWidgets.QAction(Camera)
        self.actionExit.setText("Exit")

        self.actionStartCamera = QtWidgets.QAction(Camera)
        self.actionStartCamera.setText("Start Camera")

        self.actionStopCamera = QtWidgets.QAction(Camera)
        self.actionStopCamera.setText("Stop Camera")

        self.actionSettings = QtWidgets.QAction(Camera)
        self.actionSettings.setText("Settings")

        self.menuFile.addAction(self.actionStartCamera)
        self.menuFile.addAction(self.actionStopCamera)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDevices.menuAction())

        self.layout.addWidget(self.menubar)
