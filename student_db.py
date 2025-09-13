import json
import math
from collections import namedtuple
from enum import Enum
from dataclasses import dataclass
import pydantic 
import os
import uuid

student = namedtuple('student',["name","id","avg","major"])

class LibraryDatabase :

    def __init__(self):
        self._records: list[student]=[]
    #CRUD - create - read - update - delete 


    def create_std (self,name,id,major,avg):
        if avg <0 or avg >100 :
            print("The avg you entered is incorrect ,You should enter a number higher than 0 and lower than 100 ")
            return
        try:
            student_obj = Student(name=name, id=id, avg=avg, major=major)
            std = student(student_obj.name, student_obj.id, student_obj.avg, student_obj.major.value)
            self._records.append(std)
            print(f"The student name is {std.name}")

        except pydantic.ValidationError as e:
            print("Error in student data:")
            print(e)

    def find_std(self,id:int):
        for ss in self._records:
            if ss.id ==id:
                return ss    
        print(f"Student with {id} not found")


    def update_std(self,name,id,major,avg):
        for index,stud in enumerate(self._records):
            if stud.id ==id :
                dic_data = stud._asdict()  #nametuple is immutable
                if name is not None:
                    dic_data["name"]=name
                if avg is not None:
                    if 100>=avg>=0 :
                        dic_data["avg"]=avg
                    else:
                        print("The avg you entered is incorrect ,You should enter a number higher than 0 and lower than 100 ")
                        return
                if major is not None:
                    if isinstance(major,Major):   #type major is Major ?
                        major=major.value
                    else:
                        try:
                            major_enum = Major(major)
                            dic_data["major"]=major_enum.value
                        except ValueError:
                            print("invalid major")
                            return
            self._records[index]=student(**dic_data)

        print(f"student with id ={id} not found")

    def del_std(self,id):
        for index , stud in enumerate(self._records):
            if stud.id==id:
                deleted = self._records.pop(index)
                print(f"Deleted {deleted}")
                return
        print(f"Student with {id} not found")

    def display(self):
        if not self._records:
            print("No record found")
            return
        for stud in self._records:
            print(f"Name {stud.name} , AVG {stud.avg} , ID {stud.id} , Major {stud.major}")
    def calc(self):
        if not self._records:
            print("No record to calculate average")
            return
        list_avg = []
        for stud in self._records:
            list_avg.append(stud.avg)
        total = sum(list_avg)
        avg = total / len( list_avg)
        print(f" Average of all students = {avg}")
    def save_as_json_file(self,filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True )
        with open(filename,"w",encoding="utf-8") as f :
            data_dic =[]
            for s in self._records:
                data_dic.append(s._asdict())
            json.dump(data_dic,f,indent=2,sort_keys=True)
    def load_json(self,filename):
        with open(filename,"r",encoding="utf-8") as f :
            data_dic=json.load(f)
            records_list=[]
            for d in data_dic:
                stud = student(**d)
                records_list.append(stud)
            self._records = records_list

class Major(str ,Enum):
    AI = "artifical intelligence"
    CS = "computer science"
    DS = "data science"
    CIS = "computer information system"

class Student(pydantic.BaseModel):
    name: str
    id : str = None
    avg : float
    major : Major


    
db = LibraryDatabase()

while True:
    print("\n1. Add student")
    print("2. Find student")
    print("3. Update student")
    print("4. Delete student")
    print("5. Display all students")
    print("6. Calculate average")
    print("7. To save file json ")
    print("8. To load file json ")
    print("0. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter name: ")
        id = input("Enter ID: ")
        major = input("Enter major (AI, CS, DS, CIS): ")
        avg = float(input("Enter avg: "))
        db.create_std(name, id, major, avg)

    elif choice == "2":
        id = input("Enter ID to find: ")
        student = db.find_std(id)
        if student:
            print(student)

    elif choice == "3":
        id = input("Enter ID to update: ")
        name = input("Enter new name (or leave empty): ") or None
        major = input("Enter new major (or leave empty): ") or None
        avg_input = input("Enter new avg (or leave empty): ")
        avg = float(avg_input) if avg_input else None
        db.update_std(name, id, major, avg)

    elif choice == "4":
        id = input("Enter ID to delete: ")
        db.del_std(id)

    elif choice == "5":
        db.display()

    elif choice == "6":
        db.calc()
    elif choice =="7":
        filename= input("Enter file name")
        db.save_as_json_file(filename)
    elif choice =="8":
        filename= input("Enter file name")
        db.load_json(filename)

    elif choice == "0":
        break

    else:
        print("Invalid choice")
