from dash import dcc, html
import dash_bootstrap_components as dbc
from data_transform import LocalData


class ChartYear:
    local_data = object

    def __init__(self, ):
        self.local_data = LocalData()

    def get_geral_chart(self, tab):
        return html.Div(style={'margin': '50px', 'background-color': '#f8f8ff'}, children=[
            html.H3(f'Ano {tab.replace("tab-","")}',),
            dbc.Col([
                dbc.Card([
                    dbc.Col([
                        html.Div(
                            children=f'Despesas por Legenda - {tab.replace("tab-","")}', style={'margin': '10px'}),
                        dcc.Dropdown(
                            id='dropdown-ranking',
                            options=[{"label": "Valor Líquido Acumulado por partido", "value": "vlrLiquido"},
                                     {"label": "Valor Médio por deputado", "value": "valor_medio"}],
                            value='valor_medio',
                            multi=False,
                            style={'margin': '30px'}
                        )
                    ], width=4),
                    dcc.Graph(
                        id='graph-ranking',
                        clickData={'points': [{'customdata': 'all'}]}
                    )
                ])
            ]),
            dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            html.H3(id='h3-cota',
                                    style={'margin': '10px'}),
                            html.Div(style={'margin': '10px'}, children=[
                                dcc.Dropdown(
                                    id='dropdown-tipo-map',
                                    options=[{"label": "Valor Líquido médio por estado", "value": "des_percapt"},
                                             {"label": "Valor da Cota por estado",
                                             "value": "VALOR"},
                                             {"label": "Valor Liquido Acumulado por estado",
                                             "value": "vlrLiquido"},
                                             {"label": "Quantidade de Deputados por estado", "value": "txNomeParlamentar"}],
                                    value='vlrLiquido'
                                ),
                                dcc.Graph(
                                    id='map-sum-partido')
                            ])
                        ])
                    ], width=6),
                    dbc.Col(
                        dbc.Card([
                            html.Div([
                                dbc.Row([
                                    html.H3(f"Tipos de Despesas", id='h3-tipo',
                                            style={'margin': '10px'}),
                                    dbc.Col(
                                        html.Div(
                                            dcc.Graph(
                                                id='treemap_classificacao',
                                            )
                                        ),
                                    )
                                ])
                            ])
                        ]),
                        width=6)
                    ]),
            dbc.Card([
                html.Div([
                    dbc.Row([
                        html.H3(f"Histórico de Gastos",
                                style={'margin': '10px'}),
                        dbc.Col(
                            html.Div(
                                dcc.Dropdown(
                                    id='dropdown-candidato',
                                    multi=True,
                                    options=self.local_data.get_options_candidato(),
                                    value=[self.local_data.get_options_candidato()[
                                        0]['value']]
                                )
                            ), width=6)
                    ]),
                    html.Div(
                        dcc.Graph(
                            id='comparativo-candidato',
                        )
                    )
                ])
            ]),
            dbc.Card([
                html.Div([
                    html.H3("Visão Geral"),
                    dbc.Row([
                            dbc.Col(
                                dcc.Dropdown(
                                    id='dropdown-bubble',
                                    multi=False,
                                    options=[{"label": "Tamanho pela quantidade de deputados", "value": "txNomeParlamentar"},
                                             {"label": "Tamanho pelo Valor Liquido", "value": "vlrLiquido"}],
                                    value='txNomeParlamentar'
                                ),
                                width=6),
                            ]),
                    dbc.Row([
                            dbc.Col(
                                html.Div(
                                    dcc.Graph(
                                        id='bublle-candidato',)
                                ),
                            )
                            ])
                ])
            ]),
            dbc.Card([
                html.H3("Cota Por Legenda"),
                html.Div(
                    dcc.Graph(
                        id='pie-resumo',
                        figure=self.local_data.get_pie()))
            ])
        ])

    #    __ranking_partido =  dbc.Col([
    #             dbc.Card([
    #                 dbc.Col([
    #                     html.Div(
    #                         children=f'Despesas por Legenda - {tab.replace("tab-","")}', style={'margin': '10px'}),
    #                     dcc.Dropdown(
    #                         id='dropdown-ranking',
    #                         options=[{"label": "Valor Líquido Acumulado por partido", "value": "vlrLiquido"},
    #                                  {"label": "Valor Médio por deputado", "value": "valor_medio"}],
    #                         value='valor_medio',
    #                         multi=False,
    #                         style={'margin': '30px'}
    #                     )
    #                 ], width=4),
    #                 dcc.Graph(
    #                     id='graph-ranking',
    #                     clickData={'points': [{'customdata': 'all'}]}
    #                 )
    #             ])
    #             ]
