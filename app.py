import os
from flask import Flask, redirect, render_template, request, url_for
import pickle
import numpy as np
import mysql.connector
import datetime

conn = mysql.connector.connect(
  host="frwahxxknm9kwy6c.cbetxkdyhwsb.us-east-1.rds.amazonaws.com",
  user="j6qbx3bgjysst4jr",
  password="mcbsdk2s27ldf37t",
  database="nkw2tiuvgv6ufu1z"
)

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
        return redirect(url_for('kidneyPage', patient_id=patient_id))
    else:
        return render_template('home.html')


@app.route("/kidney/<int:patient_id>", methods=['GET','POST'])
def kidneyPage(patient_id):
    cursor = conn.cursor()
    query = "SELECT * FROM physical_test_ck WHERE patient_id = %s"
    cursor.execute(query, (patient_id,))
    document = cursor.fetchone()
    cursor.close()
    if document:
        print(document[3])  # Debug statement
        return render_template('kidney.html', document=document)
    else:
        print("No document found for patient_id:", patient_id)  # Debug statement
        return "Document not found."


@app.route("/predict/<int:patient_id>", methods=['POST'])
def predictPage(patient_id):
    to_predict_list = list(map(float, request.form.values()))
    pred = predict(to_predict_list, {})
    print('to_predict_list:', to_predict_list)
    print('pred:', pred)

    # Save prediction details to database
    cursor = conn.cursor()
    query = "INSERT INTO chronic_kidney (patient_id, prediction_date, prediction, accuracy, record_type, record_id) VALUES (%s, NOW(), %s, %s, 'physical_test_ck', %s) ON DUPLICATE KEY UPDATE prediction=VALUES(prediction), prediction_date=VALUES(prediction_date)"
    if pred == 0:
        pred_str = "Patient is healthy"
    else:
        pred_str = "Patient has Chronic Kidney Disease"
    cursor.execute(query, (patient_id, str(pred_str), 'NA', 'physical_test_ck'))
    conn.commit()
    cursor.close()

    return render_template('predict.html', pred=pred)





if __name__ == '__main__':
    app.run(debug=True)
    conn.close()
