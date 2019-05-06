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

# def efficiencyData(namesData, stats):
#     efficienciesValues = []
#     killsValues = []
#     lossValues = []
#     for key in stats:
#         killsValues.append(stats[key]["totalKillsValue"])
#         lossValues.append(stats[key]["totalLossesValue"])
#         efficienciesValues.append(stats[key]["efficiency"])
#     efficiencyData = [
#         go.Scatter(
#             x = lossValues,
#             y = killsValues,
#             mode = 'markers'
#         )
#     ]
#     return efficiencyData

def efficiencyData(names, stats):
    efficiencyData = []
    for key in stats:
        efficiencyData.append(
            go.Scatter(
                x=(stats[key]["totalLossesValue"],),
                y=(stats[key]["totalKillsValue"],),
                marker= dict(
                    size=14,
                    # line=dict(width=1),
                    opacity=0.8
                ),
                text=str(stats[key]["efficiency"]) + '%',
                name=names[key]
            )
        )
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
        html.H1('Wormhole Corp Stats', style={'textAlign': 'center', 'color': 'black'}),
        # Blurb under title
        html.Div(children='''
            A basic project using mysql, DASH, and web APIs. This data is from March of 2019, and is a demonstration of DASH and sqlite database manipulation.
        '''),
        # Display killed vs. lost graph (stacked bar chart)
        dcc.Graph(
            figure=go.Figure(
                data=killLossStackedData(namesData, stats),
                layout=go.Layout(
                    title='Killed vs. Lost',
                    barmode='stack',
                    xaxis= dict(
                        title='Corp Ticker'
                    ),
                    yaxis= dict(
                        title="Amount (ISK)"
                    )                
                )                
            )
        ),

        # Display efficiency labeled (scatterplot)
        dcc.Graph(
            figure=go.Figure(
                data=efficiencyData(names, stats),
                layout=go.Layout(
                    title='Efficiency',
                    hovermode='closest',
                    xaxis= dict(
                        title='Amount lost (ISK)'
                    ),
                    yaxis= dict(
                        title="Amount killed (ISK)"
                    ),
                    shapes= [
                        dict(
                            type="line",
                            xref='x',
                            yref='y',
                            x0=0,
                            y0=0,
                            x1=500000000000,
                            y1=500000000000,
                            line = dict(
                                color="rgb(255,0,0)",
                                width=3,
                                dash="dashdot"
                            )
                        )
                    ]
                )
            )
        )
    ])





    app.run_server(debug=True)