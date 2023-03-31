import os
from flask import Flask, render_template, request
import pickle
import numpy as np



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


    

@app.route("/")
def home():
    return render_template('home.html')



@app.route("/kidney", methods=['GET', 'POST'])
def kidneyPage():
    return render_template('kidney.html')



@app.route("/predict", methods=['POST'])
def predictPage():
    
        to_predict_list = list(map(float, request.form.values()))
        pred = predict(to_predict_list, {})
        print('to_predict_list:', to_predict_list)
        print('pred:', pred)
    
        

        return render_template('predict.html', pred=pred)



if __name__ == '__main__':
    app.run(debug = True)