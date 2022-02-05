from dash import Dash, dcc, html, Input, Output, callback
from view import PageBase, TabYear
from callbacks import TabCallback


app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server
base = PageBase()
tabs = TabYear()

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/Sobre':
         return base.layout1
    elif pathname == '/TabAnos':
         return tabs.layout2
    else:
        return '404'


if __name__ == '__main__':
    app.run_server(debug=True)