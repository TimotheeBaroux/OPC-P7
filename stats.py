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

st.markdown("# Main page")
st.sidebar.markdown("# Main page")

@st.cache
def load_data():
    data = pd.read_csv("X_tract.csv")  #should be data_lean; too big for github
    return data

data = load_data()

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
    data.columns.drop(['TARGET']))

fig, ax = plt.subplots()
ax.hist(X_tract[variable], edgecolor='black', linewidth=0.7)  #, bins=20
plt.axvline(x=line[variable], color='red', label='Client', ymax=0.95)
st.pyplot(fig)