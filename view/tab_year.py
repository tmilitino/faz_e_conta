from dash import dcc, html


class TabYear:

    tab_year = html.Div([
        html.H1('Raio-x Deputados Brasil'),
        dcc.Tabs(id="tabs-59",),
        html.Div(id='tabs-content-graph-ranking',
                 style={'backgroundColor': '#f8f8ff'})
    ], style={'backgroundColor': '#f8f8ff'})
