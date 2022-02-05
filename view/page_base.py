from dash import dcc, html


class PageBase:

    layout1 = html.Div([
        html.H3('Page 1'),
        dcc.Dropdown(
            id='page-1-dropdown',
            options=[
                {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                    'NYC', 'MTL', 'LA'
                ]],
        ),
        html.Div(id='page-1-display-value'),
        dcc.Link('Go to Page 2', href='/page2')
    ])

    layout2 = html.Div([
        html.H3('Page 2'),
        dcc.Dropdown(
            options=[
                {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                    'NYC', 'MTL', 'LA'
                ]],
            id='page-2-dropdown'
        ),
        html.Div(id='page-2-display-value'),
        dcc.Link('Go to Page 1', href='/page1')
    ])
