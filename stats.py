from flask import Flask, request, jsonify
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
import matplotlib.pyplot as plt

st.markdown("# Bienvenue dans votre application de scoring")
st.markdown("## Nous allons commencer avec quelques statistiques pour votre client.")
st.sidebar.markdown("# Statistiques client")

@st.cache
def load_data():
    data = pd.read_csv("X_tract.csv")  #should be data_lean; too big for github
    return data

data = load_data()

descr = pd.read_csv("HomeCredit_columns_description.csv")

st.write("""
Quelques Statistiques sur l'ensemble des clients
""")

X_tract = pd.read_csv("X_tract.csv")

idx = X_tract.index

option = st.selectbox(
    'Client n°',
     idx+1)

line = X_tract.loc[option]

variable = st.selectbox(
    'Variable',
    data.columns)


#ax.hist(X_tract[variable], edgecolor='black', linewidth=0.7, align='mid')  #, bins=20
#plt.axvline(x=line[variable], color='red', label='Client', ymax=0.95)

fig, ax = plt.subplots()
n, bins, patches = plt.hist(X_tract[variable], edgecolor='black', linewidth=0.7, align='mid')  
plt.axvline(x=line[variable], color='red', label='Client', ymax=0.95)
#ticks = [(patch._x0 + patch._x1)/2 for patch in patches]
#plt.xticks(ticks, rotation = -90)
st.pyplot(fig)

listres = []
for name in descr["Row"]:
    if name in variable:
        listres += [name]
var_ext = listres[-1]

st.write("The variable {} refers to :".format(var_ext))
st.write(descr[descr["Row"]==var_ext]["Description"].iloc[0])