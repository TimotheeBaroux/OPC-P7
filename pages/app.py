from flask import Flask, request, jsonify
import sys
import streamlit as st
import joblib
import traceback
import pandas as pd
import numpy as np
import ast
from sklearn.inspection import permutation_importance
import subprocess
import requests
import plotly.graph_objects as go
import shap
import pickle
import lime

st.markdown("# Application")
st.sidebar.markdown("# Application")

st.write("""
Bienvenue !
Nous allons voir si vous êtes prêt pour un prêt !
""")

X_tract = pd.read_csv("X_tract.csv")
idx = X_tract.index

option = st.selectbox(
    'Client n°',
     idx+1)

line = X_tract.loc[option]

subprocess.run([sys.executable, "APImaker.py"]) 

query = [dict(line)]    #[ast.literal_eval(line)]

#st.write(query)

prediction = requests.post("http://127.0.0.1:12345/prediction",json = query)
proba = requests.post("http://127.0.0.1:12345/proba",json = query)

if ast.literal_eval(ast.literal_eval(prediction.text)["prediction"])[0]:
    st.write("Malheureusement, vous n'êtes pas prêt")
    st.write("Quelques explications :")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(ast.literal_eval(proba.text)["proba"]),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilité de non-remboursement"}, 
        gauge = {'axis': {'range': [None, 1]},'bar': {'color': "red"}
                }))
    st.write(fig)
else :
    st.write("Vous êtes éligible à un prêt !")
    st.write("Quelques explications :")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(ast.literal_eval(proba.text)["proba"]),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilité de non-remboursement"}, 
        gauge = {'axis': {'range': [None, 1]},'bar': {'color': "green"}
                }))
    st.write(fig)
    
#shap_val = requests.post("http://127.0.0.1:12345/SHAP",json = query)
#st.write(ast.literal_eval((ast.literal_eval(shap_val.text)["shap"]).replace('. ' , ',').replace('.\n' , ',')))

pipe = joblib.load("pipeline_final.pkl")
explainer = shap.Explainer(pipe.predict,pd.DataFrame(line))
shap_values = explainer(pd.DataFrame(line))