import pandas as pd
import numpy as np
from dash import Dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output, State
import sqlite3

conn = sqlite3.connect('dsc465.db')  # open the connection
cursor = conn.cursor()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1(children='DSC 465 MLB Pitch Analysis'),
        html.Table(
            [
                html.Tr(
                    [
                        html.Td(
                            [
                                dcc.Dropdown(
                                    id='player-drop',
                                    options=[
                                        {'label': f'{x[2]}, {x[1]}', 'value': x[0]}
                                        for x in cursor.execute(
                                            'Select * From players limit 100'
                                        )
                                        if x[0] != 'id'
                                    ],
                                    style={'width': 200},
                                )
                            ]
                        ),
                        html.Td([html.Button(id='submit-button', children='Submit')]),
                    ]
                )
            ]
        ),
        html.Div(id='output-section'),
    ]
)


@app.callback(
    Output('output-section', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('player-drop', 'value')],
)
def create_scatters(n_clicks, player_id):
    if n_clicks is not None:
        conn = sqlite3.connect('dsc465.db')  # open the connection
        cursor = conn.cursor()

        get_abs = cursor.execute(
            f'Select * From atbats where batter_id={player_id} limit 10'
        )

        # for t in get_abs:
        #     print(t)

        # tmp = cursor.execute(f'Select * From pitches where ab_id={2015000019}')

        # for r in tmp:
        #     print(r)

        ab_ids = [x[0] for x in get_abs]

        # print(f'Select * From pitches where ab_id in {tuple(ab_ids)}')

        # get_pitches = cursor.execute(
        #     f'Select * From pitches where ab_id in {tuple(ab_ids)}'
        # )

        # for x in get_pitches:
        #     print(x)
        df = pd.read_sql_query(
            f'Select * From pitches where ab_id in {tuple(ab_ids)}', conn
        )

        print(df)
        scatter = go.Figure()

        scatter.add_trace(go.Scattergl(x=df['px'], y=df['pz'], mode='markers'))

        scatter.add_shape(
            # unfilled Rectangle
            type="rect",
            x0=-0.7,
            y0=1.5,
            x1=0.7,
            y1=4,
            line=dict(color="Black",),
        )

        scatter.update_layout(
            xaxis=dict(range=[-3, 3]),
            yaxis=dict(range=[-1, 5]),
            width=700,
            height=700,
            autosize=False,
        )

        return html.Div([dcc.Graph(id='chart', figure=scatter),])


if __name__ == '__main__':
    app.run_server(debug=True)
