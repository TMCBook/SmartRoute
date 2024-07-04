import os
from pathlib import Path
import firebase_admin
from firebase_admin import credentials, firestore
import studentLocationMap

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def addStudents(Data, name):
    student = db.collection("busRoute").document(name)
    student.set({"students":Data}, merge = True)

def updateStatus(document, name, onBoard = "On The Bus"):
    student = db.collection("busRoute").document(document)
    student.update({f"students.{name}.status":onBoard})
# Can only be run directly
if '__main__' == __name__:
    #lists directory for faces
    imageFiles = os.listdir("faces/")
    #Makes name equals to all image file names in all caps and removes suffix
    for imageFile in imageFiles:
        name = Path(imageFile).stem.upper()
        #Retrieves info based on student name in database
        data = studentLocationMap.data[imageFile]
        studentData = {name:{"location":data["location"], "status":"Not On The Bus"}}
        addStudents(name = data["routeName"], Data = studentData)