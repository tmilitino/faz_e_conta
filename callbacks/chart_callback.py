from dash import Input, Output, State, callback
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash
from view import ChartYear
import plotly.express as px
from data_transform import LocalData


class ChartCallback:
    local_data = ''

    def __init__(self, ):
        self.local_data = LocalData()

    @callback(Output('tabs-content-graph-ranking', 'children'),
              Input('tabs-59', 'value'))
    def render_content(self, tab):

        year = ChartYear().get_geral_chart(tab)
        return year

    @callback(
        Output('treemap_classificacao', 'figure'),
        [Input('graph-ranking', 'clickData')])
    def get_treemap(self, click_event):
        df = self.local_data.df_treemap(
            click_event.get('points')[0].get('label'))

        list_color = []
        for cor in px.colors.qualitative.Pastel1:
            list_color.append(cor)
        for cor in px.colors.qualitative.Pastel2:
            list_color.append(cor)

        fig = px.treemap(df, values="vlrLiquido", path=[px.Constant(" "),
                                                        "txtDescricao"], maxdepth=2, color_discrete_sequence=list_color)

        fig.update_layout(
            margin=dict(
                l=5,
                r=0,
                b=0,
                t=0,)
        )

        return fig

    @callback(
        Output('bublle-candidato', 'figure'),
        [Input('dropdown-bubble', 'value')])
    def update_bubble(self, type_chart):
        df_bubble = self.local_data.bubble()
        y_title = 'Valor - R$'
        y_axis = 'vlrLiquido'
        if type_chart == 'vlrLiquido':
            y_title = 'Quantidade'
            y_axis = 'txNomeParlamentar'

        fig = px.scatter(df_bubble, x='partido', color_discrete_sequence=df_bubble.cores.tolist(), y=y_axis, size=type_chart, color='partido',
                         hover_name='partido',)

        fig.update_layout(yaxis_title=y_title,
                          xaxis_title="Partido",
                          legend_title='Partido',
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')

        return fig

    @callback(
        Output('comparativo-candidato', 'figure'),
        [Input('dropdown-candidato', 'value')])
    def update_comparativo(self, cand):
        df_comparativo = self.local_data.comparativo(cand)
        fig = px.line(df_comparativo, x="mes_ano",
                      y="total", color='txNomeParlamentar', line_shape='spline')
        fig.update_traces(mode="markers+lines", hovertemplate=None)
        fig.update_layout(hovermode="x")
        fig.update_traces(mode="markers+lines")
        fig.update_layout(yaxis_title="Valor - R$",
                          xaxis_title="Mês",
                          legend_title='Parlamentar',
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')

        return fig

    @callback(
        Output('graph-ranking', 'figure'),
        [Input('dropdown-ranking', 'value')])
    def update_output(self, value):
        df_sum_legenda = self.local_data.ranking_partidos()
        df_sum_legenda.sort_values(value, ascending=False, inplace=True)

        fig = px.bar(df_sum_legenda,
                     x=df_sum_legenda.partido,
                     y=value,
                     color=df_sum_legenda.partido, barmode="overlay",
                     color_discrete_sequence=df_sum_legenda.cores.tolist(),)

        fig.update_layout(yaxis_title="Valor - R$",
                          xaxis_title="Partido",
                          legend_title='Partido',
                          plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')
    # layout = Layout(
    #     paper_bgcolor='rgba(0,0,0,0)',
    #     yaxis_color='rgba(0,0,0,0)'
    # )

        return fig

    @callback(
        Output('map-sum-partido', 'figure'),
        [Input('graph-ranking', 'clickData'),
         Input('dropdown-tipo-map', 'value')])
    def update_map_output(self, value, tipo_mapa):
        merged = self.local_data.get_chart_map(
            value.get('points')[0].get('label'))

        fig_map = px.choropleth_mapbox(merged, geojson=merged.geometry, mapbox_style="carto-positron",
                                       locations=merged.index, color=tipo_mapa, color_continuous_scale=px.colors.sequential.Agsunset_r, zoom=2.3, center={"lat": -15.3889, "lon": -52.882778},)
        fig_map.update_layout(
            margin=dict(
                l=5,
                r=50,
                pad=4), coloraxis_colorbar_title="Valor - R$")

        return fig_map

    @callback(
        Output('h3-cota', 'children'),
        [Input('graph-ranking', 'clickData')])
    def update_map_output(self, value):
        return f"Cota Parlamenta - {value.get('points','Todos os Pardidos')[0].get('label','Todos os Pardidos')}"

    @callback(
        Output('h3-tipo', 'children'),
        [Input('graph-ranking', 'clickData')])
    def update_map_output(self, value):
        return f"Tipos de Despesas - {value.get('points','Todos os Pardidos')[0].get('label','Todos os Pardidos')}"
