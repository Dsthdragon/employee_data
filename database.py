import sqlite3
import os
import shutil


class database():
    def __init__(self, parent=None):
        super(database, self).__init__()
        self.parent = parent
        self.connection()

    def connection(self):
        try:
            self.conn = sqlite3.connect(os.getcwd()+""+os.sep+"data"+os.sep+"db"+os.sep+"database.db")
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))
            
    def saveUser(self, _data, _error):
        data = {}
        data['dob'] = _data['dob'].text()
        data['level'] = _data['level'].text()
        data['doe'] = _data['doe'].text()
        data['phone'] = _data['phone'].text()
        data['gender'] = _data['gender'].currentText()
        data['picture'] = _data['picture'].text()
        data['state'] = _data['state'].currentText()
        data['email'] = _data['email'].text()
        data['name'] = _data['name'].text()
        data['lga'] = _data['lga'].text()
        data['address'] = _data['address'].text()
        data['designation'] = _data['designation'].text()

        noNull = 1
        if not os.path.exists(data['picture']):
            noNull = 0

        for i in data:
            if data[i] == "":
                noNull = 0

        if noNull == 1:
            try:
                image = data['picture'].split(os.sep)
                image = image[len(image)-1]
                newImage = os.sep+"data"+os.sep+"profiles"+os.sep+""+image
                shutil.copy(data['picture'],os.getcwd()+newImage)
                os.remove(data['picture'])
                data['picture'] = newImage
                self.cursor.execute("INSERT INTO staffs (name, gender, address, state, lga, dob, phone, email, doe, designation, level, picture) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(data['name'], data['gender'], data['address'], data['state'], data['lga'], data['dob'], data['phone'], data['email'], data['doe'], data['designation'], data['level'], data['picture']))
                self.conn.commit()
                _id = self.cursor.lastrowid
                self.parent.usersPage.viewUser(_id)
            except sqlite3.DatabaseError as e:
                self.parent.errorReport(str(e))

            except FileNotFoundError as e:
                self.parent.errorReport(str(e))
        else:
            _error.setText("<font color=red><center><i>All fields required</i></center></font>")

    def getUsers(self, value=None):
        try:
            if value:
                newSearch = ''
                x = 0
                for i in value.split(" "):
                    if x == 0:
                        newSearch += "name LIKE '%"+i+"%'"
                    else:
                        newSearch += " OR name LIKE '%"+i+"%'"
                    x += 1
                print(newSearch)
                sql = "SELECT * FROM staffs WHERE {} ".format(newSearch)
                print(sql)
                self.cursor.execute(sql)
            else:
                self.cursor.execute("SELECT * FROM staffs")
            return self.cursor.fetchall()


        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))

    def getUser(self, _id):
        try:
            self.cursor.execute("SELECT * FROM staffs WHERE id = ?", (_id,))
            return self.cursor.fetchone()
        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))

    def addActivity(self, _data, _error):
        data = {}
        data['staffId'] = _data['staffId']
        data['shortDesc'] =  _data['shortDesc'].toPlainText()
        data['fullDesc'] =  _data['fullDesc'].toPlainText()
        data['dateAdded'] = _data['date'].text()
        noNull = 1
        for i in data:
            if data[i] == "":
                noNull = 0

        if noNull == 1:
            try:
                sql ="INSERT INTO activity (staffId, shortDesc, fullDesc, dateAdded) VALUES (?, ?, ?, ?)"
                self.cursor.execute(sql,(str(data['staffId']), str(data['shortDesc']), str(data['fullDesc']), str(data['dateAdded'])))
                self.conn.commit()
                self.parent.usersPage.viewUser(data['staffId'])
            except sqlite3.DatabaseError as e:
                self.parent.errorReport(str(e))
        else:
            _error.setText("<font color=red><center><i>All fields required</i></center></font>")

    def staffActivity(self, staffId):
        try:
            sql = "SELECT * FROM activity WHERE staffId = ?"
            self.cursor.execute(sql, (staffId,))
            return self.cursor.fetchall()
        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))

    def fullActivity(self, _id):
        try:
            self.cursor.execute("SELECT * FROM activity WHERE id = ?", (_id,))
            return self.cursor.fetchone()
        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))

    def getActivity(self, value = None):
        try:
            if value:
                newSearch = ''
                x = 0
                for i in value.split(" "):
                    if x == 0:
                        newSearch += "shortDesc LIKE '%"+i+"%'"
                    else:
                        newSearch += " OR shortDesc LIKE '%"+i+"%'"
                    x += 1
                sql = "SELECT * FROM activity WHERE {} ".format(newSearch)
                self.cursor.execute(sql)
            else:
                self.cursor.execute("SELECT * FROM activity")
            return self.cursor.fetchall()

        except sqlite3.DatabaseError as e:
            self.parent.errorReport(str(e))