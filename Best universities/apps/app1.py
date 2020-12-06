#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 11:05:53 2020

@author: randon
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import dash
import urllib.parse

app = dash.Dash(__name__, suppress_callback_exceptions=True)

timesData = pd.read_csv("timesData.csv")

df2016 = timesData[timesData.year==2016].iloc[:50,:]
num_students_size  = [str(each).replace(',', '.') for each in df2016.num_students]
international_color = [float(each) for each in df2016.international]

fig1 = {
  "data": [
    {
        'y': df2016.teaching,
        'x': df2016.world_rank,
        'mode': 'markers',
        'marker': {
            'color': international_color,
            'size': num_students_size,
            'showscale': True
        },
        "text" :  df2016.university_name
    }
],
  "layout": {
        "title":"Teaching and world_rank for each university",
        "yaxis_title":"Teaching",
        "xaxis_title":"World rank"
    }
}

layout1 = html.Div([
    dcc.Link('Résultats de l\'ACP', href='/apps/app2'),    
    html.Br(),
    html.Br(),
    html.A(html.Button('Chargement des données'),
           id='data_download',
           download='timesData.csv',
           href="data:text/csv;charset=utf-8," + urllib.parse.quote(df2016.to_csv(index=False)),
           target="_blank"),
    html.Br(),
    html.H3('Teaching and world_rank for each university in 2016'),
    html.Div([dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df2016.columns],
        data=df2016.to_dict('records'),
    )]),
    html.Div([
    dcc.Graph(
        id='Teaching-world_rank-vs-university',
        figure=fig1
    ) ]),
    html.Div(dcc.Markdown('''### Matrice de corrélation''')),
    html.Div(style = {"float":"left"},children = [
        html.Img(src=app.get_asset_url('correlation_matrix.png'))]) 
 ])
