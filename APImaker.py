#Install Libraries
from flask import Flask, request, jsonify
import streamlit as st
import joblib
import pickle
import traceback
import pandas as pd
import numpy as np
import shap

application = Flask(__name__)

@application.route("/prediction", methods=["POST"])
def prediction():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            return jsonify({"prediction": str(lr.predict(query))})
        except:
            return jsonify({"trace": traceback.format_exc()})
    else:
        print ("Model not good")
        return ("Model is not good")
    
@application.route("/proba", methods=["POST"])    
def proba():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            return jsonify({"proba": str(lr.predict_proba(query)[0,1])})
        except:
            return jsonify({"trace": traceback.format_exc()})
    else:
        print ("Model not good")
        return ("Model is not good")

@application.route("/prob", methods=["POST"])    
def prob():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            return jsonify({"prob": str(lr.predict_proba(query)[0,1])})
        except:
            return jsonify({"trace": traceback.format_exc()})
    else:
        print ("Model not good")
        return ("Model is not good")
    
@application.route("/SHAP", methods=["POST"])
def SHAP():
    if lr:
        try:
            json_ = request.json
            query = pd.DataFrame(json_)
            explainer = shap.Explainer(lr.predict,query)
            shap_values = explainer(query)
            return jsonify({"shap": str(shap_values.values)})
        except:
            return jsonify({"trace": traceback.format_exc()})
    else:
        print ("Model not good")
        return ("Model is not good")
    
if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 12345
    lr = joblib.load("pipeline_final.pkl")
    print ("Model loaded")
    
application.run(port=port, debug=True)