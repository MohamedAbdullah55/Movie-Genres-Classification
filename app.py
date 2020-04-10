from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from tensorflow import keras
from keras.preprocessing import image
from werkzeug.utils import secure_filename

import os
import numpy as np
from random import random

app = Flask(__name__)

UPLOAD_FOLDER = "static/img"
if not os.path.exists(UPLOAD_FOLDER) :
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'jpg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html" )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/api", methods=["POST"])
def api():
     if request.method == "POST":

        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file'] 

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):

            for imagefile in os.listdir(UPLOAD_FOLDER):
                os.remove(UPLOAD_FOLDER+"/"+imagefile)

            filename = secure_filename(file.filename)

            filename = filename.split('.')[0]+str(random())+"."+filename.split('.')[1]       
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            path = UPLOAD_FOLDER+"\\"+filename
            img = image.load_img(path, target_size = (350,350,3))
            img = np.array(img)
            img = img/255
           
            img = img.reshape(1,350,350,3)
            model = keras.models.load_model('AlexNetModel.h5')
            y_prob = model.predict(img)

            classes = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime',
                       'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror',
                       'Music', 'Musical', 'Mystery', 'N/A', 'News', 'Reality-TV', 'Romance',
                       'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

            y_prob = list(y_prob[0]) 
             

            sorted_y = sorted(y_prob,reverse=True)
            top3 = []
            for i in range(4):
                top3.append(classes[y_prob.index(sorted_y[i])] ) 
                                  
            return render_template("index.html",
                                   filename=str(filename),
                                   classes=classes,
                                   sorted_y=sorted_y,
                                   y_prob=y_prob,
                                   len = len(sorted_y)-14,
                                   top3 = top3)    
         

if __name__ == '__main__':
    app.run(debug=True)
