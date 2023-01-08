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

st.markdown("# Estimation du risque de défaut de crédit")
st.sidebar.markdown("# Estimateur")

st.write("### Bienvenue !")
st.write("### Nous allons voir si vous êtes prêt pour un prêt !")

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
#st.write(prediction.text)
proba = requests.post("http://127.0.0.1:12345/proba",json = query)

if ast.literal_eval(ast.literal_eval(prediction.text)["prediction"])[0]:
    st.write("Malheureusement, vous n'êtes pas prêt")
    st.write("Quelques explications :")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = float(ast.literal_eval(proba.text)["proba"]),
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Probabilité de non-remboursement"}, 
        gauge = {'axis': {'range': [None, 1]},'bar': {'color': "black"}
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
        gauge = {'axis': {'range': [None, 1]},'bar': {'color': "blue"}
                }))
    st.write(fig)
    
st.write("### Impact des variables les plus importantes :")

#shap_val = requests.post("http://127.0.0.1:12345/SHAP",json = query)
#st.write(ast.literal_eval((ast.literal_eval(shap_val.text)["shap"]).replace('. ' , ',').replace('.\n' , ',')))

X_ltrain = pd.read_csv("X_ltrain.csv")
y_ltrain = pd.read_csv("y_ltrain.csv")

def probas(data):
    proba_temp = requests.post("http://127.0.0.1:12345/proba_lime",json = pd.DataFrame(data).to_dict("records"))
    #st.write(np.array(ast.literal_eval((ast.literal_eval(proba_temp.text)["proba_lime"]).replace('\n ' , ',').replace(' ' , ','))))
    return np.array(ast.literal_eval((ast.literal_eval(proba_temp.text)["proba_lime"]).replace('\n ' , ',').replace(' ' , ',')))

st.write("Mesure de l'impact des variables les plus influentes sur la probabilité de non-remboursement :")
explainer = lime.lime_tabular.LimeTabularExplainer(np.array(X_ltrain),training_labels=np.array(y_ltrain),
                                                   feature_names=list(X_ltrain.columns))
exp = explainer.explain_instance(line.values, probas, num_features=5)
st.write(exp.as_pyplot_figure(label=1))
st.write("_Attention : dans ce graphique, les barres vertes, qui correspondent à une augmentation du résultat, sont un élément négatif : elle correspondent à une augmentation de la probabilité que le client ait des problèmes pour rembourser son prêt_")