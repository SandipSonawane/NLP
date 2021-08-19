import dash
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from collections import Counter
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash
import json
import random
from nltk.tokenize import word_tokenize

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
                         options=[{'label': i, 'value': i} for i in chapters], value='')
        ]),

        # job category dropdown
        html.Div(id='Text_Input', children=[
            html.Div(className="btn btn-secondary btn-lg", children=[
                html.H6('Write two words')]),
            dcc.Input(id='choose_words',
                      value='the adventure '),
        ]),

        # Submit Button
        html.Div(id='Submit', children=[
            html.Div(className="btn btn-primary", children=[
                html.H6('Submit')
            ])
        ])
    ]),

    html.Div(className='text_area', children=[
        html.Div(children=[
            dcc.Textarea(
                id='chapter-text',
                value='Text from the selected chapter will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ]),
        html.Div(children=[
            dcc.Textarea(
                id='generated-text',
                value='Text generated using Markov Chain with given input will appear here.',
                style={'width': '99%', 'height': 600},
            )
        ])
    ])

])


# Combine all text files
def combine_txt_files(text_files, path=os.path.join(os.getcwd(), f'Data\\sherlock\\')):
    corpus = []
    for file in text_files:
        with open(os.path.join(path, file)) as f:
            for line in f:
                line = line.strip()
                if line != '':
                    corpus.append(line)
    return corpus


txt_files = os.listdir(os.path.join(os.getcwd(), 'Data\\sherlock\\'))
all_text = combine_txt_files(txt_files)


# Tokenizing text
def tokenize_text(text):
    tokenized_text = []
    for line in text:
        line = line.lower()
        tokens = word_tokenize(line)
        tokenized_text.extend([w for w in tokens if w.isalpha()])
    return tokenized_text


tokenized_text = tokenize_text(all_text)


# Markov Model

def build_morkov_model(text, n_gram=2):
    markov_model = {}

    # create dictionary having no. of transitions from current state to next state
    for i in range(len(text) - n_gram - 1):
        state_zero, state_one = "", ""
        for j in range(n_gram):
            state_zero += text[i + j] + " "
            state_one += text[i + j + n_gram] + " "
        if not state_zero in markov_model:
            markov_model[state_zero] = {}
            markov_model[state_zero][state_one] = 1
        else:
            if state_one in markov_model[state_zero]:
                markov_model[state_zero][state_one] += 1
            else:
                markov_model[state_zero][state_one] = 1

    # calculate transition probabilities based on transition frequencies
    for state_zero, transition in markov_model.items():
        total_transitions = sum(transition.values())
        for state, transition_count in transition.items():
            markov_model[state_zero][state] = transition_count / total_transitions

    return markov_model


markov_model = build_morkov_model(tokenized_text)


# generating text based on text input
def generate_text(markov_model_input, limit=50, start='the adventure '):
    state_zero = start
    state_one = None
    text = ''
    text = state_zero + ' '
    for i in range(limit):
        state_one_dictionary = Counter(markov_model_input[state_zero])
        try:
            state_one = state_one_dictionary.most_common(10)[random.randint(0, 5)][0]
        except:
            state_one = state_one_dictionary.most_common(10)[0][0]
        text += state_one + ' '
        state_zero = state_one
    return text


# show chapter text based on input
@app.callback(Output('chapter-text', 'value'),
              [Input('pick_chapter', 'value')])
def update_chapter_text(chapter):
    chapter_text_list = open(os.path.join(os.getcwd(), f'Data\\sherlock\\{chapter}')).readlines()
    chapter_text = ''.join(chapter_text_list)
    return chapter_text


@app.callback(Output('generated-text', 'value'),
              [Input('choose_words', 'value')])
def update_chapter_text(words):
    # markov_model = {}
    # with open(os.path.join(os.getcwd(), f'Data\\markov_model_JSON.txt')) as f:
    #     for line in f:
    #         (key, val) = line.split()
    #         markov_model[int(key)] = val
    #
    # # with open(os.path.join(os.getcwd(), f'Data\\markov_model_JSON.txt')) as json_file:
    # #     markov_model = json.load(json_file)
    words = words.lower().strip()
    words = words + ' '

    generated_text = ''
    for i in range(10):
        generated_text += f's_{i}' + ': ' + generate_text(markov_model, start=words, limit=10) + '\n \n'
    return generated_text


app.run_server()
