import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import base64
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
from collections import Counter
import dash_bootstrap_components as dbc
import dash_table
from django_plotly_dash import DjangoDash

app = dash.Dash(name='Text_Generation_Using_Markov_Chain', external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.css.append_css({"external_url": "/static/assets/01_first.css"})


chapters = [file for file in os.listdir(os.path.join(os.getcwd(), 'Data\\sherlock\\'))]
available_categories = ['dg', 'g']

# Define App Layout
app.layout = html.Div([
    html.Div(
        [html.H3('Text Generation Using Markov Chains')], style={'text-align': 'center'}
    ),

    html.Div(className='dropdowns', children=[
        # company dropdown
        html.Div(id='chapter', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H6('Select Chapter to see text')]),
            dcc.Dropdown(id='pick_chapter',
                         options=[{'label': i, 'value': i} for i in chapters], value='Amazon')
        ]),

        # job category dropdown
        html.Div(id='Text_Input', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H6('Write two words')]),
            dcc.Dropdown(id='choose_words',
                         options=[{'label': i, 'value': i} for i in available_categories], value='Data Science'),
        ]),

        # Submit Button
        html.Div(id='Submit', children=[
            html.Div(className="btn btn-primary", children=[
                html.H6('Submit')
            ])
        ])
    ]),

    html.Div(className='text_area', children=[
        html.Div(id='chapter-text', children=[
            dcc.Textarea(
                value='Text from the selected chapter will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ]),
        html.Div(id='generated-text', children=[
            dcc.Textarea(
                value='Text generated using Markov Chain with given input will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ])
    ])

])



app.run_server()
