import cv2
import face_recognition
import os
from pathlib import Path
def loadImage(path):
    return cv2.imread(path)

def processImage(frame, knownFaceEncodings, knownFaceNames):

#Resizes the image so it is faster to read
    downSizedFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
#Changes to RGB 
    rgbSmallFrame = downSizedFrame[:, :, ::-1]
#Finds location of face in a photo
    faceLocations = face_recognition.face_locations(downSizedFrame)
#Detects unique features of the face
    encodings = face_recognition.face_encodings(downSizedFrame,faceLocations)
#List of names
    faceNames = []
#Loop to see if a face is alreadu in the data or if it is a new face
    for face_encoding in encodings:
        matches = face_recognition.compare_faces(face_encoding, knownFaceEncodings)
        name = "unknown"
        #If face is already in the data, matches it to a name in the data
        if True in matches:
            faceMatchIndex = matches.index(True)
            name = knownFaceNames[faceMatchIndex]
        faceNames.append(name)
    
    return faceNames, faceLocations

#Function which builds a display with picture and name
def displayFaces(frame, names, locations):
    for (top,right,bottom,left), name in zip(locations,names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame,(left, top), (right, bottom), (0, 0, 255), 2)
        #Builds frame around picture 
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
        #cv2.FILLED fills in entire area, replaces thickness
        font = cv2.FONT_HERSHEY_TRIPLEX
        cv2.putText(frame, name, (left+6, bottom-6), font, 1, (255, 255, 255), 1)    
        cv2.imshow("image", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        #Adds text in bottom rectangle of the name
    return frame

#Test Function
def displayFaceCard(frame):
    cv2.imshow("image", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#Loads face + name
def loadFaces():
    #lists for faces and names 
    faceEncodingList = []
    faceNames = []
    #creates path for file with img of faces
    faces_dir = "faces/"
    #creates a list of everything insde a file
    imageFiles = os.listdir(faces_dir)
    #for loop to create path, load path, encode image, find name, add to lists
    for person in imageFiles:
        imagePath = os.path.join(faces_dir, person)
        faceImage = face_recognition.load_image_file(imagePath)
        faceEncoding = face_recognition.face_encodings(faceImage)[0]
        faceEncodingList.append(faceEncoding)
        #splits text to remove file extension, seperates strings by a period 
        name = os.path.splitext(person)[0].upper()
        faceNames.append(name)
    return faceEncodingList, faceNames

def faceDetection(image, show = False):
    knownFaceEncodings, knownFaceNames = loadFaces()
    frame = loadImage(image)
    faceNames, faceLocations = processImage(frame, knownFaceEncodings, knownFaceNames)
    faces = displayFaces(frame, faceNames, faceLocations)
    filename = f'{Path(image).stem}.jpeg'
    cv2.imwrite(filename, faces)
    if show:
        displayFaceCard(faces)
    return filename, faceNames
 
if __name__ == "__main__":
    faceDetection("woman.jpg", show = True)    