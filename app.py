import os
from flask import Flask, redirect, render_template, request, url_for
import pickle
import numpy as np
from pymongo import MongoClient
import pymongo
client = pymongo.MongoClient("mongodb+srv://manorama:manorama@cluster0.sntkvlc.mongodb.net/?retryWrites=true&w=majority")
db = client["Kidney_Patients"]
collection = db["Kidney_result"]



app = Flask(__name__)

def predict(values, dic):
    # diabetes
    
    # kidney disease
    if len(values) == 24:
        model = pickle.load(open('models/kidney.pkl','rb'))
        values = np.asarray(values)
        print('values shape:', values.shape)
        print('values:', values)
        pred = model.predict(values.reshape(1, -1))[0]
        print('pred:', pred)
        return pred


    

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        return redirect(url_for('kidneyPage', patient=patient_id))
    else:
        return render_template('home.html')



@app.route("/kidney/<string:patient>", methods=['GET','POST'])
def kidneyPage(patient):
    document = collection.find_one({'patient': patient})
    if document:
        return render_template('kidney.html', document=document)
    else:
        return "Document not found."


@app.route("/predict", methods=['POST'])
def predictPage():
    
        to_predict_list = list(map(float, request.form.values()))
        pred = predict(to_predict_list, {})
        print('to_predict_list:', to_predict_list)
        print('pred:', pred)
    
        

        return render_template('predict.html', pred=pred)



if __name__ == '__main__':
    app.run(debug = True)