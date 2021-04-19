"""created by barthk12"""
from itertools import zip_longest
import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory
from flask_session import Session
from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(os.getcwd(),"static/photos")
# create the upload folder should it not exist yet
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


# Configure app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Reload templates automatically
app.config['TEMPLATES_AUTO_RELOAD'] = True

breeds = ['Abyssinian',
 'american_bulldog',
 'american_pit_bull_terrier',
 'basset_hound',
 'beagle',
 'Bengal',
 'Birman',
 'Bombay',
 'boxer',
 'British_Shorthair',
 'chihuahua',
 'Egyptian_Mau',
 'english_cocker_spaniel',
 'english_setter',
 'german_shorthaired',
 'great_pyrenees',
 'havanese',
 'japanese_chin',
 'keeshond',
 'leonberger',
 'Maine_Coon',
 'miniature_pinscher',
 'newfoundland',
 'Persian',
 'pomeranian',
 'pug',
 'Ragdoll',
 'Russian_Blue',
 'saint_bernard',
 'samoyed',
 'scottish_terrier',
 'shiba_inu',
 'Siamese',
 'Sphynx',
 'staffordshire_bull_terrier',
 'wheaten_terrier',
 'yorkshire_terrier']
# Set up the interpreter 
interpreter = tflite.Interpreter(model_path=os.path.join(os.getcwd(), "tf_model/model.tflite"), num_threads=1)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response
    
# Configure session to use filesystem (instead of signed cookie)
app.config['SESSION_FILE_DIR'] = mkdtemp()
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = "filesystem"
Session(app)

# Check if file should be allowed to upload
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    cats = [pet for pet in breeds if pet[0].isupper()]
    dogs = [pet for pet in breeds if pet[0].islower()]

    return render_template("index.html", cats=cats, dogs=dogs)

@app.route("/classifier", methods=['GET', 'POST'])
def classifier():
    if request.method == "POST":
         # check if the post request has the file part
         if "file" not in request.files:
             flash("No file part")
             return redirect((request.url))
         file = request.files["file"]
         if file.filename == "":
             flash("No selected file")
             return redirect(request.url)
         if file and allowed_file(file.filename):
             filename = secure_filename(file.filename)
             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
             # open and convert the image
             img = Image.open(file).resize((width, height))
             input_data = np.expand_dims(img, axis=0)
             input_data = input_data / 255.0
             ## as it gave an error (expecting float 32, change dtype)
             input_data = input_data.astype(np.float32)
             # run the interpreter
             interpreter.set_tensor(input_details[0]['index'], input_data)
             interpreter.invoke()
             output_data = interpreter.get_tensor(output_details[0]['index'])
             results = np.squeeze(output_data)
             top = results.argsort()[-1:][::-1][0]
             prediction = breeds[top]
             probability = f'{results[top]*100:.2f}'
             if results[top] < 0.70:
                 prediction = "Sorry, cannot classify."
                 probability = ""
             return render_template("result.html", filename=filename, prediction=prediction, probability=probability)
         else:
             flash("Filetype not supported")
             return redirect(request.url)
         
    return render_template("classifier.html")

@app.route("/about")
def about_me():
    return render_template("about.html")


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

