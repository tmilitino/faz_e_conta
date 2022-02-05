from dash import Input, Output, State, callback
from dash import dcc, html
import dash


class TabCallback:
    @callback(
        Output('page-1-display-value', 'children'),
        Input('page-1-dropdown', 'value'))
    def display_value(value):
        ctx = dash.callback_context
        return f'You have selected {value}'

    @callback(
        Output('page-2-display-value', 'children'),
        Input('page-2-dropdown', 'value'))
    def display_value(value):
        return f'You have selected {value}'

    @callback(
        Output("tabs-59", "children"),
        [Input("tabs-59", "values")],
        # [State("integer", "value")],
    )
    def render_tabs(values):
        output = [2019, 2020, 2021]
        tabs = []
        for num in output:
            tabs.append(
                dcc.Tab(
                    label=f"Tab {num + 1}",
                    value=f"tab{num + 1}",
                    children=[html.Div(num)],
                )
            )
        return tabs
