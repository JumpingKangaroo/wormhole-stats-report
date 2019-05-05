# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json

def read_json(filename):
  with open(filename) as json_file:
    data = json.load(json_file)
  return data

def killAmountsData(namesData, stats):
    valuesData = []
    for key in stats:
        valuesData.append(stats[key]["totalKillsValue"])
    killData = [
        go.Bar(
            x=namesData,
            y=valuesData,
        )
    ]
    return killData

def killLossStackedData(namesData, stats):
    killsValues = []
    lossValues = []
    for key in stats:
        killsValues.append(stats[key]["totalKillsValue"])
        lossValues.append(stats[key]["totalLossesValue"])
    killData = [
        go.Bar(
            x=namesData,
            y=killsValues,
            name='Killed',
        ),
        go.Bar(
            x=namesData,
            y=lossValues,
            name='Lost',
        )
    ]
    return killData

def efficiencyData(namesData, stats):
    efficienciesValues = []
    killsValues = []
    lossValues = []
    for key in stats:
        killsValues.append(stats[key]["totalKillsValue"])
        lossValues.append(stats[key]["totalLossesValue"])
        efficienciesValues.append(stats[key]["efficiency"])
    efficiencyData = [
        go.Scatter(
            x = lossValues,
            y = killsValues,
            mode = 'markers'
        )
    ]
    return efficiencyData


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

if __name__ == '__main__':

    names = read_json("names.json")
    stats = read_json("stats.json")

    # Put the names into a list
    namesData = []
    for key in stats:
        namesData.append(names[key])
    
    app.layout = html.Div(children=[
        # Title
        html.H1('Hello Wormholes', style={'textAlign': 'center', 'color': 'black'}),
        # Blurb under title
        html.Div(children='''
            Wormhole stats
        '''),
        # Display sum of isk killed (bar graph)
        dcc.Graph(
            figure=go.Figure(
                data=killAmountsData(namesData, stats),
                layout=go.Layout(
                    title='Total Killed',
                )
            )
        ),
        # Display killed vs. lost graph (stacked bar chart)
        dcc.Graph(
            figure=go.Figure(
                data=killLossStackedData(namesData, stats),
                layout=go.Layout(
                    title='Killed vs. Lost',
                    barmode='stack'                
                )                
            )
        ),
        # Display efficiency (scatterplot)
        dcc.Graph(
            figure=go.Figure(
                data=efficiencyData(namesData, stats),
                layout=go.Layout(
                    title='Efficiency',
                )                
            )
        )
    ])





    app.run_server(debug=True)