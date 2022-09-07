from dash import Dash, dcc, html, Input, Output, callback
from view import PageSobre, TabYear
from callbacks import TabCallback, chart_callback
import dash_bootstrap_components as dbc

app = Dash(__name__, suppress_callback_exceptions=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
sobre = PageSobre()
tabs = TabYear()

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


sidebar = html.Div(
    [
        html.H2("Faz e Conta", className="display-6"),
        html.Hr(),
        html.P(
            "Raio-X dos Candidatos", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Sobre", href="/Sobre", active="exact"),
                dbc.NavLink("Anos", href="/TabAnos", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content', style=CONTENT_STYLE)
])


@callback(Output('page-content', 'children'),
          Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/Sobre':
        return sobre.layout1
    elif pathname == '/TabAnos':
        return tabs.tab_year
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)
