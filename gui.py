#!/usr/bin/env python3
from os import read
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, uic,QtSql
from PyQt5.QtCore import Qt
import subprocess,csv,os
from PyQt5.uic.uiparser import QtWidgets

def AddPoint(p,id):
    with open(os.path.join("Data","coding.csv")) as f:
        all = []
        reader = csv.reader(f)
        for stud in reader:
            all.append(stud)
    for i in range(1,len(all)):
        if all[i][2] == id and all[i][3].lower() =="student":
            all[i][4] = str(float(all[i][4])+p)
            all[i][5] = str(float(all[i][5])+p)
        elif all[i][2] == id and (all[i][3].lower() =="leader" or all[i][3].lower() =="co.leader" ):
            all[i][4] = str(float(all[i][4])+2*p)
            all[i][5] = str(float(all[i][5])+2*p)
    with open(os.path.join("Data","coding.csv"),"w") as f:
        writer = csv.writer(f)
        writer.writerows(all)
    with open(os.path.join("Data","coding.csv"),"r") as f:
        all = f.readlines()
        all[-1] = all[-1][:-1]
    with open(os.path.join("Data","coding.csv"),"w") as f:
        f.writelines(all)
class LoginGui(QMainWindow):
    def __init__(self,cu):
        super(LoginGui,self).__init__()
        uic.loadUi("Data/InterfaceData/loginUi.ui",self) #ui load
        #to access elem€nts use their objectNam€ in designer self.nom
        self.widget = cu
        self.openDB()
        self.pushButton.clicked.connect(self.checkUser)
    def openDB(self):
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("data.sqlite")
        if not self.db.open():
            print("Error on opening Login Data Base")
        self.query = QtSql.QSqlQuery()
    def checkUser(self):
        username_ = self.lineEdit.text()
        password_ = self.lineEdit_2.text()
        self.query.exec_(f"select * from userdata where username ='{username_}' and password = '{password_}';")
        self.query.first()
        if self.query.value("username") != None and self.query.value("password") != None:
            self.loggedIn()
        else:
            window = QMessageBox()
            window.setText("Invalid Username or Password")
            window.setIcon(QMessageBox.Critical)
            x = window.exec_()
    def loggedIn(self):
        widget = self.widget
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setWindowFlags(Qt.WindowCloseButtonHint)
        widget.show()
class MainGui(QMainWindow):
    def __init__(self,cu,table):
        super(MainGui,self).__init__()
        uic.loadUi("Data/InterfaceData/main.ui",self) #ui load
        #to access elem€nts use their objectNam€ in designer self.nom
        self.widget = cu
        self.table = table
        self.scanCamera.clicked.connect(self.scanCam)
        self.scanCamera2.clicked.connect(self.scanCam)
        self.scanNoCamera.clicked.connect(self.scanNo)
        self.scanNoCamera2.clicked.connect(self.scanNo)
        self.studentList.clicked.connect(self.ToList)
        self.studentList2.clicked.connect(self.ToList)
    def scanCam(self):
        subprocess.run(['./Handler.py',"1"])
    def scanNo(self):
        subprocess.run(['./Handler.py',"2"])
    def ToList(self):
        widget = self.widget
        widget.setCurrentIndex(widget.currentIndex()+1)
        widget.setFixedHeight(650)
        widget.setFixedWidth(800)
        self.table.loadData()
        widget.show()
class TableGui(QMainWindow):
    def __init__(self,cu):
        super(TableGui,self).__init__()
        uic.loadUi("Data/InterfaceData/table.ui",self) #ui load
        self.tableWidget.setColumnWidth(6,120)
        self.tableWidget.setColumnWidth(5,120)
        self.tableWidget.setColumnWidth(0,120)
        self.tableWidget.setColumnWidth(2,119)
        self.selectedRow = None
        self.tableWidget.selectionModel().selectionChanged.connect(self.handleSelection)
        self.widget = cu
        self.pushButton.clicked.connect(self.goBack)
        self.addButton.clicked.connect(self.add)
        self.resetSession.clicked.connect(self.resetSes)
        self.resetAbs.clicked.connect(self.resetAbsences)
        self.resetPre.clicked.connect(self.resetPresence)
    def setColortoRow(self, rowIndex, color):
        for j in range(7):
            self.tableWidget.item(rowIndex, j).setBackground(color)
    def handleSelection(self,selected,deselected):
        for i in selected.indexes():
            self.selectedRow = i.row()
        if len(selected.indexes()) == 0:
            self.selectedRow = None
    def add(self):
        if self.selectedRow == None:
            window = QMessageBox()
            window.setText("Please select a student first")
            x = window.exec_()
        else:
            #points,done = QInputDialog.getInt(self,"Add points to member","How much points you wanna add : ")
            points,done = QInputDialog.getText(self,"Add points to member","How much points you wanna add : ")
            if done:
                with open("Data/coding.csv") as f:
                    reader = csv.reader(f)
                    for i,stud in enumerate(reader):
                       if i==self.selectedRow+1:
                           id = stud[2]
                           break
                try:
                    AddPoint(float(points),id)
                except:
                    window = QMessageBox()
                    window.setText("Please provide a valid int or float number with .")
                    x = window.exec_()
                    raise ValueError('\033[1m'+'\033[91m'+"Please provide a valid int or float number with .")
                self.loadData()
    def goBack(self):
        widget = self.widget
        widget.setCurrentIndex(widget.currentIndex()-1)
        widget.setFixedHeight(550)
        widget.setFixedWidth(700)
    def loadData(self):
        with open("Data/presents.csv") as p:
            reader = csv.reader(p)
            presents = []
            for s in reader:
                presents.append(s[0])
        with open("Data/coding.csv") as f:
            f.readline()
            l=len(f.readlines())
        with open("Data/coding.csv") as f:
            f.readline()
            reader = csv.reader(f)
            self.tableWidget.setRowCount(l)
            for row,stud in enumerate(reader):
                for col in range(7):
                    self.tableWidget.setItem(row,col,QTableWidgetItem(stud[col]))
                if stud[2] in presents:
                    self.setColortoRow(row,QtGui.QColor(19,184,101))
    def resetSes(self):
        window = QMessageBox()
        window.setIcon(QMessageBox.Critical)
        window.setText("Are you sure you want to reset Session points?")
        window.setDetailedText("You should only do this at the start of the session if the central program didnt do it")
        window.setStandardButtons(QMessageBox.Abort|QMessageBox.Ok)
        window.buttonClicked.connect(self.resetSessionHandleButton)
        x = window.exec_()
    def resetSessionHandleButton(self,i):
        if i.text()=="&OK":
            subprocess.run(['./Handler.py',"3"])
            self.loadData()
    def resetAbsences(self):
        if self.selectedRow == None:
            window = QMessageBox()
            window.setText("Please select a student first")
            x = window.exec_()
        else:
            with open("Data/coding.csv") as f:
                reader = csv.reader(f)
                for i,stud in enumerate(reader):
                   if i==self.selectedRow+1:
                       self.currentSt = stud
            window = QMessageBox()
            window.setText(f"Are you sure you want to reset {self.currentSt[0]} {self.currentSt[1]} absences strike?")
            window.setStandardButtons(QMessageBox.Abort|QMessageBox.Ok)
            window.buttonClicked.connect(self.resetAbsencesHandler)
            x = window.exec_()
    def resetAbsencesHandler(self,i):
        if i.text()=="&OK":
            subprocess.run(["./Handler.py","4",self.currentSt[2]])
            self.loadData()
    def resetPresence(self):
        window = QMessageBox()
        window.setIcon(QMessageBox.Critical)
        window.setText("Are you sure you want to reset teh presents list of this session?")
        window.setDetailedText("You should only do this at the start of another session or the end if the program didnt do it for some reasons\nIt won't retrice the points given for presence")
        window.setStandardButtons(QMessageBox.Abort|QMessageBox.Ok)
        window.buttonClicked.connect(self.resetPresenceHandleButton)
        x = window.exec_()
    def resetPresenceHandleButton(self,i):
        if i.text()=="&OK":
            with open(os.path.join("Data","presents.csv"),"w") as f:
                f.write("ID,TIME")
            self.loadData()
def main():
    isLogin = True
    app = QApplication([])
    currentUi = QStackedWidget()
    table = TableGui(currentUi)
    mainWindow = MainGui(currentUi,table)
    login = LoginGui(currentUi) 
    currentUi.addWidget(login)
    currentUi.addWidget(mainWindow)
    currentUi.addWidget(table)
    currentUi.setFixedHeight(550)
    currentUi.setFixedWidth(700)
    currentUi.setWindowFlags(Qt.FramelessWindowHint)
    currentUi.setAttribute(Qt.WA_TranslucentBackground)
    currentUi.show()
    app.exec_()
if __name__ == '__main__':
    main()