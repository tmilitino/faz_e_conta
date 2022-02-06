from re import I
import pandas as pd
import plotly.express as px
import numpy as np
from data_transform import LoadData

class LocalData:

    df_desp_dept = pd.DataFrame()
    df_bases = LoadData()

    def get_df_desp(self, ano):

        self.df_desp_dept = pd.DataFrame()

        if ano.replace("tab-", "") == "2020":
            df_desp = self.df_bases.df_desp_20
        elif ano.replace("tab-", "") == "2019":
            df_desp = self.df_bases.df_desp_19

        df_desp = df_desp[df_desp['codLegislatura'] == 56]
        df_desp = df_desp[df_desp['vlrLiquido'] > 0]
        df_desp['mes_ano'] = df_desp.apply(
            lambda x: f"{x.numMes}-{x.numAno}", axis=1)
        self.self.df_desp_dept = df_desp[~df_desp['cpf'].isna()]

    def pie(self,):
        df_dept_pie = self.df_desp_dept[[
            'sgPartido', 'sgUF', 'vlrLiquido', 'txNomeParlamentar']]
        df_dept_pie = df_dept_pie.groupby(['sgPartido', 'sgUF', 'txNomeParlamentar'],).agg(
            {'vlrLiquido': np.sum}).reset_index()

        df_dept_pie['vlrLiquido'] = df_dept_pie['vlrLiquido']

        self.df_bases.df_pos.nome = self.df_bases.df_pos.nome.str.lower()
        df_dept_pie.sgPartido = df_dept_pie.sgPartido.str.lower()

        df_dept_pie = df_dept_pie.merge(
            self.df_bases.df_pos, left_on='sgPartido', right_on='nome')

        df_dept_pie.sort_values('classificacao', inplace=True)
        df_dept_pie = df_dept_pie.reset_index()

        return df_dept_pie

    def bubble(self,):
        df_dept_scatter = self.df_desp_dept[[
            'sgPartido', 'vlrLiquido', 'txNomeParlamentar']]
        df_dept_scatter = df_dept_scatter.groupby(['sgPartido'],).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()
        df_dept_scatter['vlrLiquido'] = df_dept_scatter['vlrLiquido']

        self.df_bases.df_pos.nome = self.df_bases.df_pos.nome.str.lower()
        df_dept_scatter.sgPartido = df_dept_scatter.sgPartido.str.lower()

        df_dept_scatter = df_dept_scatter.merge(
            self.df_bases.df_pos, left_on='sgPartido', right_on='nome')

        df_dept_scatter.sort_values('classificacao', inplace=True)

        return df_dept_scatter

    def comparativo(self, cand):
        df_compatativo = self.df_desp_dept[self.df_desp_dept['txNomeParlamentar'].isin(
            cand)]
        df_compatativo = df_compatativo[['txNomeParlamentar', 'mes_ano', 'vlrLiquido', 'numMes']].groupby(
            ['txNomeParlamentar', 'mes_ano', 'numMes']).sum().sort_index(
            level=['numMes', 'txNomeParlamentar', ]).reset_index().rename(columns={
                'vlrLiquido': 'total'})
        df_compatativo.drop('numMes', inplace=True, axis=1)
        df_compatativo['total'] = df_compatativo['total']/1000
        return df_compatativo

    def ranking_partidos(self,):
        df_sum_legenda = self.df_desp_dept[['sgPartido', 'vlrLiquido', 'txNomeParlamentar']].groupby(
            ['sgPartido']).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()

        df_sum_legenda['valor_medio'] = df_sum_legenda['vlrLiquido'] / \
            df_sum_legenda['txNomeParlamentar']

        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']

        self.df_bases.df_pos.nome = self.df_bases.df_pos.nome.str.lower()
        df_sum_legenda.sgPartido = df_sum_legenda.sgPartido.str.lower()

        df_sum_legenda = df_sum_legenda.merge(
            self.df_bases.df_pos, left_on='sgPartido', right_on='nome')

        print(df_sum_legenda.head())
        return df_sum_legenda

    def get_chart_map(self, sgPartido):
        self.df_desp_dept_vl_map = self.df_desp_dept
        if sgPartido:
            if sgPartido == 'SDD':
                sgPartido = 'SOLIDARIEDADE'
            self.df_desp_dept_vl_map = self.df_desp_dept[self.df_desp_dept['sgPartido'] == sgPartido]

        self.df_bases.df_cota[['UF', 'VALOR']].groupby(['UF']).sum().sort_values(
            ['VALOR'], ascending=False).reset_index().rename(columns={'VALOR': 'total_cota'})

        self.df_desp_dept_vl_map = self.df_desp_dept_vl_map[['sgUF', 'vlrLiquido', 'txNomeParlamentar']].groupby(
            ['sgUF']).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).sort_values(['vlrLiquido'],
                                                                                        ascending=False).reset_index()
        self.df_desp_dept_vl_map['des_percapt'] = (
            self.df_desp_dept_vl_map['vlrLiquido']/self.df_desp_dept_vl_map['txNomeParlamentar'])/12

        self.df_desp_dept_vl_map['vlrLiquido'] = self.df_desp_dept_vl_map['vlrLiquido']

        merged = self.df_bases.brasil_map.set_index('UF_05').join(
            self.df_desp_dept_vl_map.set_index('sgUF'))

        merged = merged.merge(
            self.df_bases.df_cota, left_on=merged.index, right_on='UF')
        merged = merged.set_index('UF')
        merged.vlrLiquido = merged.vlrLiquido.fillna(0)
        merged.txNomeParlamentar = merged.txNomeParlamentar.fillna(0)
        merged.VALOR = merged.VALOR.fillna(0)
        merged.des_percapt = merged.des_percapt.fillna(0)

        return merged

    def get_options_candidato(self,):
        return [{"label": f"{x['txNomeParlamentar']} - {x['sgUF']} - {x['sgPartido']} ", "value": x['txNomeParlamentar']} for _, x in self.df_desp_dept[['txNomeParlamentar', 'sgPartido', 'sgUF']].drop_duplicates().iterrows()]

    def df_treemap(self, click_event):

        df_sum_legenda = self.df_desp_dept
        if click_event:
            if click_event == 'SDD':
                click_event = 'SOLIDARIEDADE'
            df_sum_legenda = self.df_desp_dept[self.df_desp_dept['sgPartido'] == click_event]

        df_sum_legenda = df_sum_legenda[['sgPartido', 'txtDescricao', 'vlrLiquido']].groupby(
            ['sgPartido', 'txtDescricao']).sum().sort_values('vlrLiquido', ascending=False).reset_index()
        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']
        return df_sum_legenda

    def get_pie(self,):
        df_pie = self.pie()

        dict_cores = pd.Series(df_pie.cores.values,
                               index=df_pie.partido).to_dict()
        dict_cores['(?)'] = '#FFFF'

        fig = px.sunburst(df_pie, path=[px.Constant(" "), 'partido', 'sgUF', 'txNomeParlamentar'],
                          values='vlrLiquido', color='partido',  maxdepth=2, color_discrete_map=dict_cores)

        return fig
