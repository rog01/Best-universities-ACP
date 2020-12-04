#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 10:23:54 2020

@author: roger
"""

import dash

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server