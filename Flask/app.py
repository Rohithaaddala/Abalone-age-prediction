# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 16:43:40 2021

@author: rincy
"""
import numpy as np
import pickle
from flask import Flask,request, render_template
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "WUzKWUPzFMMiKG8MxA1E0WY7ivhdPWH1zu8dEeqgcCyl"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line


app=Flask(__name__,template_folder="templates")
model = pickle.load(open('abalone.pkl', 'rb'))
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/home', methods=['GET'])
def about():
    return render_template('home.html')
@app.route('/pred',methods=['GET'])
def page():
    return render_template('upload.html')
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    input_features = [float(x) for x in request.form.values()]
    features_value = [np.array(input_features)]
    print(features_value)
    
    payload_scoring = {"input_data": [{"field": [["Sex","Length","Height","Whole weight","Shucked weight","Viscera weight","Shell weight"]],
                                       "values": [features_value]}]}
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/095fd9ce-8575-417f-b4e4-2db7d9d50dba/predictions?version=2022-08-07', json=payload_scoring,
                                     headers={'Authorization': 'Bearer ' + mltoken})
    print("response_scoring")
    predictions=response_scoring.json()
    pred=predictions['predictions'][0]['values'][0][0]
    if(pred==1):
        output="it will not get exited"
        print("it will not get exited")
    else:
        output="it gets exited"
        print("it gets exited")
        return render_template('upload.html', prediction_text='The predicted age of abalone is {} years.'.format((output+1.5)))
   
if __name__ == '__main__':
      app.run(debug=False)