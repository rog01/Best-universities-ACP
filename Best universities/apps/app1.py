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
import plotly.express as px
import numpy as np

timesData = pd.read_csv("timesData.csv")

df2016 = timesData[timesData.year == 2016].iloc[:20,:]
num_students_size  = [float(each.replace(',', '.')) for each in df2016.num_students]

num_students_size  = [float(each.replace(',', '.')) for each in df2016.num_students]

international_color = [float(each) for each in df2016.international]
df2016 = timesData[timesData.year == 2016].iloc[:20,:]
num_students_size  = [float(each.replace(',', '.')) for each in df2016.num_students]

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
    html.H3('Teaching and world_rank for each university in 2016'),
    # dcc.Dropdown(
    #     id='app-1-dropdown',
    #     options=[
    #         {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
    #             'NYC', 'MTL', 'LA'
    #         ]
    #     ]
    # ),
    html.Div([dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df2016.columns],
        data=df2016.to_dict('records'),
    )]),
    html.Div([
    dcc.Graph(
        id='Teaching-world_rank-vs-university',
        figure=fig1
    ) ])  
])
