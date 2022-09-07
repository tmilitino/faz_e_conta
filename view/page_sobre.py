from dash import dcc, html


class PageSobre:

    layout1 = html.Div([
        html.H3('Page 1'),
        dcc.Dropdown(
            id='page-1-dropdown',
            options=[
                {'label': f'App 1 - {i}', 'value': i} for i in [
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
                {'label': f'App 1 - {i}', 'value': i} for i in [
                    'NYC', 'MTL', 'LA'
                ]],
            id='page-2-dropdown'
        ),
        html.Div(id='page-2-display-value'),
        dcc.Link('Go to Page 1', href='/page1')
    ])
