#!/usr/bin/env python3
from datetime import datetime
from texttable import Texttable
import cv2 as cv
import numpy as np
import os
import csv
from numpy.core.numeric import outer
from playsound import playsound
from pyzbar.pyzbar import decode
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
class student:
    def __init__(self,fname,lname,id,role,points,spoints,astrikes,nid):
        self.fname = fname
        self.lname = lname
        self.id = id
        self.points = points
        self.spoints = spoints
        self.role = role
        self.astrikes = astrikes
        self.nid = nid
    def myId(self):
        return self.id

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
def AbsencesSetToZero(id):
    with open(os.path.join("Data","coding.csv")) as f:
        all = []
        reader = csv.reader(f)
        for stud in reader:
            all.append(stud)
    for i in range(1,len(all)):
        if all[i][2] == id:
            all[i][6] = "0"
    with open(os.path.join("Data","coding.csv"),"w") as f:
        writer = csv.writer(f)
        writer.writerows(all)
    with open(os.path.join("Data","coding.csv"),"r") as f:
        all = f.readlines()
        all[-1] = all[-1][:-1]
    with open(os.path.join("Data","coding.csv"),"w") as f:
        f.writelines(all)
def AbsencesAdd(id):
    with open(os.path.join("Data","coding.csv")) as f:
        all = []
        reader = csv.reader(f)
        for stud in reader:
            all.append(stud)
    for i in range(1,len(all)):
        if all[i][2] == id:
            all[i][6] = str(int(all[i][6])+1)
    with open(os.path.join("Data","coding.csv"),"w") as f:
        writer = csv.writer(f)
        writer.writerows(all)
    with open(os.path.join("Data","coding.csv"),"r") as f:
        all = f.readlines()
        all[-1] = all[-1][:-1]
    with open(os.path.join("Data","coding.csv"),"w") as f:
        f.writelines(all)
def MarkAbsents(presents,oh,om):
    if oh >19 or (oh==19 and om>30):
        return False
    with open(os.path.join("Data","coding.csv")) as f:
        f.readline()
        all = []
        reader = csv.reader(f)
        for stud in reader:
            all.append(stud[2])
    current = datetime.now()
    h,m = current.hour,current.minute
    if (h == 15 and m > 30) or (h > 16):
        for id in all:
            if id not in presents:
                AbsencesAdd(id)
        with open(os.path.join("Data","presents.csv"),"w") as f:
            f.write("ID,TIME")
        return True
    return False
def ResetSessionPoints():
    current = datetime.now()
    h,m = current.hour,current.minute
    if (h == 2 and m > 8) or (h > 2):
        with open(os.path.join("Data","coding.csv")) as f:
            all = []
            reader = csv.reader(f)
            for stud in reader:
                all.append(stud)
        for i in range(1,len(all)):
                all[i][5] = "0"
        with open(os.path.join("Data","coding.csv"),"w") as f:
            writer = csv.writer(f)
            writer.writerows(all)
        with open(os.path.join("Data","coding.csv"),"r") as f:
            all = f.readlines()
            all[-1] = all[-1][:-1]
        with open(os.path.join("Data","coding.csv"),"w") as f:
            f.writelines(all)
def ScanWithShowing():
    current = datetime.now()
    oh,om = current.hour,current.minute
    #if oh > 5 or (oh==5 and om>30):
    #    raise TimeoutError(f"{bcolors.FAIL} Wach la7bib 7ab ta3milna data? afta7 brk 9bal 7isa wla during {bcolors.BOLD}hada 9adar yakhrab system des absences aghla9 aghla9")
    presents = []
    with open(os.path.join("Data/presents.csv")) as f:
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            presents.append(row[0])
    names = {}
    with open(os.path.join("Data","coding.csv")) as cdata:
        cdata.readline()
        reader = csv.reader(cdata)
        for el in reader:
            names[el[2]] = el[0]+" "+ el[1]
    cam = cv.VideoCapture(0)
    while True:
            ret,frame = cam.read()
            for code in decode(frame):
                data = code.data.decode('utf-8')
                if data in names.keys() and data not in presents:
                    AddPoint(1,data)
                    presents.append(data)
                    with open(os.path.join("Data/presents.csv"),"a") as f:
                        f.write("\n"+data+","+datetime.now().strftime("%H:%M"))
                    playsound(os.path.join("Data","Sounds","ver.mp3"))
                    output = "Authorized"
                    AbsencesSetToZero(data)
                    color = (0,255,0)
                elif data not in names.keys():
                    output = "Not Authorized"
                    playsound(os.path.join("Data","Sounds","warning_fx.mp3"))
                    color = (0,0,255)
                if data in presents and data in names.keys():
                    color = (0,255,0)
                    output = "Authorized"
                points =np.array([code.polygon],np.int32)
                points = points.reshape((-1,1,2))
                rect = code.rect
                cv.polylines(frame,[points],True,(255,0,255),5)
                if output=="Authorized":
                    cv.putText(frame,output+" : "+names[data]+" - "+data,(rect[0],rect[1]-10),cv.FONT_HERSHEY_SIMPLEX,0.9,color,2)
                else:
                    cv.putText(frame,output+" : "+data,(rect[0],rect[1]-10),cv.FONT_HERSHEY_SIMPLEX,0.9,color,2)
            cv.imshow("Scanner",frame)
            if MarkAbsents(presents,oh,om)==True:
                break
            cv.waitKey(1)
def ScanWithNoShowing():
    current = datetime.now()
    oh,om = current.hour,current.minute
    presents = []
    ids = []
    with open(os.path.join("Data/presents.csv")) as f:
        f.readline()
        reader = csv.reader(f)
        for row in reader:
            presents.append(row[0])
    with open(os.path.join("Data","coding.csv")) as cdata:
        cdata.readline()
        reader = csv.reader(cdata)
        for el in reader:
            ids.append(el[2])
    cam = cv.VideoCapture(0)
    while True:
        try:
            ret,frame = cam.read()
            for code in decode(frame):
                data = code.data.decode('utf-8')
                if data in ids and data not in presents:
                    print(data)
                    AddPoint(1,data)
                    presents.append(data)
                    with open(os.path.join("Data/presents.csv"),"a") as f:
                        f.write("\n"+data+","+datetime.now().strftime("%H:%M"))
                    playsound(os.path.join("Data","Sounds","ver.mp3"))
                    AbsencesSetToZero(data)
                elif data not in ids:
                    playsound(os.path.join("Data","Sounds","warning_fx.mp3"))
            if MarkAbsents(presents,oh,om)==True:
                break
            cv.waitKey(1)
        except IndexError:
            print("Program crashed retrying")
def PrintClass(list):
    t = Texttable()
    t.add_row(['Num ID','First Name','Last Name','ID',"Role",'Points','Session Points','Absences Strike'])
    t.set_cols_dtype(['t','t','t','t','t','t','t','t'])
    for stud in list:
        t.add_row([stud.nid,stud.fname,stud.lname,stud.id,stud.role,stud.points,stud.spoints,stud.astrikes])
    print(t.draw())
def main():
    StudentClasses = []
    with open(os.path.join("Data","coding.csv")) as f:
        f.readline()
        reader = csv.reader(f)
        for i,stud in enumerate(reader):
            StudentClasses.append(student(stud[0],stud[1],stud[2],stud[3],stud[4],stud[5],stud[6],i+1))
    print("\n\n")
    print("\t\tTeam Leaders Interface")
    print("\t\tCoded for ByteCraft")
    print("\n\n")
    print("Please select what task to perform\n")
    print("  1. Launch the scanner with showing to register presences and absences")
    print("  2. Launch the scanner without showing to register presences and absences")
    print("  3. Add points to a student")
    print("  4. Set abcences of a member to 0")
    print("  555. Force Reset Sessions points (You should only run this before a session (if somehow program didnt reset them))")
    print("  6. Reset presents file (only do when the program didnt reset it for some reaosns")
    print("  7. Show Class List\n")
    print("Note : Don't launch the main program after the end of sessions to avoid adding extra absences")
    print("If you want to do that please make a copy of .csv file before")
    SelectedOption = input("\n Selection : ")
    if SelectedOption == "1":
        ScanWithShowing()
    elif SelectedOption == "2":
        ScanWithNoShowing()
    elif SelectedOption == "3":
        PrintClass(StudentClasses)
        print("Note : Points are doubled for leaders and co.leaders")
        nid = int(input("\n Numeric ID of the student : "))
        p = float(input(" Please specify how much points you wanna add : "))
        AddPoint(p,str(StudentClasses[nid-1].myId()))
        if StudentClasses[nid-1].role.lower() == "leader" or StudentClasses[nid-1].role.lower() == "co.leader":
            StudentClasses[nid-1].points = str(float(StudentClasses[nid-1].points)+2*p)
            StudentClasses[nid-1].spoints = str(float(StudentClasses[nid-1].spoints)+2*p)
        else:
            StudentClasses[nid-1].points = str(float(StudentClasses[nid-1].points)+p)
            StudentClasses[nid-1].spoints = str(float(StudentClasses[nid-1].spoints)+p)
        PrintClass(StudentClasses)
        print("Done!")
    elif SelectedOption == "4":
        PrintClass(StudentClasses)
        nid = int(input("\n Numeric ID of the student : "))
        AbsencesSetToZero(StudentClasses[nid-1].id)
        StudentClasses[nid-1].astrikes = '0'
        PrintClass(StudentClasses)
        print("Done!")
    elif SelectedOption == "555":
        conf = input("Are you sure you wanna reset the session points? (type yes/no) : ")
        if conf=="yes":
            ResetSessionPoints()
        else :
            print("Operation abandoned")
    elif SelectedOption =="6":
        conf = input("Are you sure you wanna reset the presents? (type yes/no) : ")
        if conf=="yes":
            with open(os.path.join("Data","presents.csv"),"w") as f:
                f.write("ID,TIME")
        else :
            print("Operation abandoned")
    elif SelectedOption == '7':
        PrintClass(StudentClasses)
    else: 
        raise ValueError("\n\033[91m"+'\033[1m'+"Invalid option please select either 1,2,3,4")
if __name__ =="__main__":
    main()