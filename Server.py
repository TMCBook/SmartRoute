#imports all needed functions
from flask import Flask, request, jsonify
from Face_Detection import faceDetection 
import base64
import os
import Database
#starts up flask
app = Flask(__name__)
#creates path for link
@app.route("/analyze/<document>")


def analyze(document):
    #forces and image to run code 
    uploadImage = request.files.get("image")
    #gives an error if there is no image
    if not uploadImage:
        return jsonify({"error":"no file uploaded"}), 400
    #gives the image a path and saves the data
    image_path = uploadImage.filename
    uploadImage.save(image_path)
    #uses the face detection function from Face_Detection
    fileName, studentName = faceDetection(image_path)
    #opens image 
    with open(fileName, "rb") as imageFile:
        imageBytes = imageFile.read()
    base64_str = base64.b64encode(imageBytes).decode('utf-8') 
    #removes information after to avoid clutter
    if os.path.exists(fileName):
        os.remove(fileName)
    if os.path.exists(image_path):
        os.remove(image_path)
    #runs updateStatis from Database
    Database.updateStatus(document, True)
    #allows the code to be used in other languages or turn into file
    return jsonify({"result":base64_str})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    