#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:09:48 2020

@author: randon
"""

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np

import dash
from sklearn import preprocessing

from sklearn.decomposition import PCA

app = dash.Dash(__name__, suppress_callback_exceptions=True)
# choix du nombre de composantes à calculer
n_comp = 8

# import de l'échantillon
data = pd.read_csv("timesData.csv")

data = data[data.year==2016].iloc[:50,:]

data.income = pd.to_numeric(data.income, errors='coerce')
data.num_students  = [str(each).replace(',', '') for each in data.num_students]
data.num_students =  pd.to_numeric(data.num_students, errors='coerce')
data.international =  pd.to_numeric(data.international, errors='coerce')
data.total_score =  pd.to_numeric(data.total_score, errors='coerce')

X=data.values
# selection des colonnes à prendre en compte dans l'ACP
data_pca = data[["teaching","international","research","citations","income","total_score","num_students","student_staff_ratio"]]

# préparation des données pour l'ACP
data_pca = data_pca.fillna(data_pca.mean()) # Il est fréquent de remplacer les valeurs inconnues par la moyenne de la variable
X = data_pca.values
names = data["university_name"] # ou data.index pour avoir les intitulés
features = data.columns

# Centrage et Réduction
std_scale = preprocessing.StandardScaler().fit(X)
X_scaled = std_scale.transform(X)

# Calcul des composantes principales
pca = PCA(n_components=n_comp)
pca.fit(X_scaled)

# Eboulis des valeurs propres
scree = pca.explained_variance_ratio_*100
fig = px.line(X_scaled, x=np.arange(len(scree))+1,
             y=scree.cumsum())

# Visualize all the principal components
components = pca.fit_transform(X_scaled)
labels = {
    str(i): f"PC {i+1} ({var:.1f}%)"
    for i, var in enumerate(pca.explained_variance_ratio_ * 100)
}

fig2 = px.scatter_matrix(
    components,
    labels=labels,
    dimensions=range(4),
    color=data["university_name"]
)
fig2.update_traces(diagonal_visible=False)

#Projection orthogonal
# loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

# fig3 = px.scatter(components, x=0, y=1, color=X_scaled['university_name'])

# for i, feature in enumerate(features):
#     fig.add_shape(
#         type='line',
#         x0=0, y0=0,
#         x1=loadings[i, 0],
#         y1=loadings[i, 1]
#     )
#     fig.add_annotation(
#         x=loadings[i, 0],
#         y=loadings[i, 1],
#         ax=0, ay=0,
#         xanchor="center",
#         yanchor="bottom",
#         text=feature,
#     )

layout2 = html.Div([
    dcc.Link('Première analyse des données', href='/apps/app1'),
    html.Div([
    html.H3('Eboulis des valeurs propres'),
    dcc.Graph(
        id='Eboulis-VP',
        figure=fig
    )
    ]),
    html.Div([   
    html.H3('Visualisation des composantes principales'),
    dcc.Graph(     
        id='PCA_components',
        figure=fig2
    )
    ]), 
    html.Div(dcc.Markdown('''### Corrélations des CP''')),
    html.Div(style = {"float":"left"},children = [
        html.Img(src=app.get_asset_url('Correlation_F1_F2.png')),
        html.Img(src=app.get_asset_url('Correlation_F3_F4.png'))]),
    html.Div(style = {"float":"left"},children = [
        html.Img(src=app.get_asset_url('Correlation_F5_F6.png')),
        html.Img(src=app.get_asset_url('Correlation_F7_F8.png'))])
    # html.Div([
    # dcc.Graph(
    #     id='PCA_loadings',
    #     figure=fig3
    # )
    # ])
])

