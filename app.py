from flask import Flask, render_template, request, jsonify
#import jsonify
import os
import requests
from wsgiref import simple_server
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('regression_rf1.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        age = int(request.form['Age'])
        bmi = float(request.form['BMI'])
        
        region_northwest=request.form['Region']
        if(region_northwest=='NorthWest'):
                region_northwest=1
                region_southeast=0
                region_southwest=0
        
        elif(region_northwest=='SouthEast'):
                region_northwest=0
                region_southeast=1
                region_southwest=0
        elif(region_northwest=='SouthEast'):
                region_northwest=0
                region_southeast=1
                region_southwest=0
        else:
            region_northwest=0
            region_southeast=0
            region_southwest=0
            
        children=request.form['Child']
        if(children==0):
                children=0
        elif(children==1):
                children=1
        elif(children==2):
                children=2
        elif(children==3):
                children=3
        elif(children==4):
                children=4
        else:
            children=5  
        
        smoker_yes=request.form['smoker']
        if(smoker_yes=='Yes'):
            smoker_yes=1
        else:
            smoker_yes=0
            
        gender_male=request.form['gender']
        if(gender_male=='Male'):
            gender_male=1
        else:
            gender_male=0   
            
            
            
        prediction=model.predict([[age,bmi,children,smoker_yes,region_northwest,region_southeast,region_southwest,gender_male]])
        output=round(prediction[0],2)
       
        if output<0:
            return render_template('index.html',prediction_texts="Sorry Your Estimated Insurance Premium is invalid.Please try again!!")
        else:
            return render_template('index.html',prediction_text="Your Estimated Insurance Premium should be Rs.{}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    #clApp = ClientApp()
    port = int(os.getenv("PORT"))
    host = '0.0.0.0'
    httpd = simple_server.make_server(host=host, port=port, app=app)
    httpd.serve_forever()

