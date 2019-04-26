# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import json

def read_json(filename):
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

if __name__ == '__main__':

    names = read_json("names.json")
    stats = read_json("stats.json")

    killAmounts = []
    namesData = []
    valuesData = []
    for key in stats:
        namesData.append(names[key])
        valuesData.append(stats[key]["totalKillsValue"])
    killAmounts = [ { "y": namesData, "x": valuesData, 'type': 'bar', 'orientation': 'h'} ]

    app.layout = html.Div(children=[
        html.H1('Hello Wormholes', style={'textAlign': 'center', 'color': 'black'}),

        html.Div(children='''
            Wormhole stats
        '''),

        dcc.Graph(
            id='kill-amounts',
            figure={
                'data': killAmounts,
                'layout': {
                    'title': 'Febuary Kill Stats'
                }
            }
        )
    ])

    app.run_server(debug=True)