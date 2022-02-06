import pandas as pd


class LocalData:

    def get_df_desp(ano):
        global df_desp_dept
        df_desp_dept = pd.DataFrame()

        if ano.replace("tab-","") == "2020":
            df_desp = df_desp_20
        elif ano.replace("tab-","") == "2019":
            df_desp = df_desp_19

        df_desp = df_desp[df_desp['codLegislatura']==56]
        df_desp = df_desp[df_desp['vlrLiquido'] > 0]
        df_desp['mes_ano'] = df_desp.apply(lambda x: f"{x.numMes}-{x.numAno}", axis=1)
        df_desp_dept = df_desp[~df_desp['cpf'].isna()]


    def pie():
        df_dept_pie = df_desp_dept[[
            'sgPartido', 'sgUF', 'vlrLiquido', 'txNomeParlamentar']]
        df_dept_pie = df_dept_pie.groupby(['sgPartido', 'sgUF', 'txNomeParlamentar'],).agg(
            {'vlrLiquido': np.sum}).reset_index()

        df_dept_pie['vlrLiquido'] = df_dept_pie['vlrLiquido']

        df_pos.nome = df_pos.nome.str.lower()
        df_dept_pie.sgPartido = df_dept_pie.sgPartido.str.lower()

        df_dept_pie = df_dept_pie.merge(
            df_pos, left_on='sgPartido', right_on='nome')

        df_dept_pie.sort_values('classificacao', inplace=True)
        df_dept_pie = df_dept_pie.reset_index()

        return df_dept_pie


    def bubble():
        df_dept_scatter = df_desp_dept[[
            'sgPartido', 'vlrLiquido', 'txNomeParlamentar']]
        df_dept_scatter = df_dept_scatter.groupby(['sgPartido'],).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()
        df_dept_scatter['vlrLiquido'] = df_dept_scatter['vlrLiquido']

        df_pos.nome = df_pos.nome.str.lower()
        df_dept_scatter.sgPartido = df_dept_scatter.sgPartido.str.lower()

        df_dept_scatter = df_dept_scatter.merge(
            df_pos, left_on='sgPartido', right_on='nome')

        df_dept_scatter.sort_values('classificacao', inplace=True)

        return df_dept_scatter


    def comparativo(cand):
        df_compatativo = df_desp_dept[df_desp_dept['txNomeParlamentar'].isin(
            cand)]
        df_compatativo = df_compatativo[['txNomeParlamentar', 'mes_ano', 'vlrLiquido', 'numMes']].groupby(
            ['txNomeParlamentar', 'mes_ano', 'numMes']).sum().sort_index(
            level=['numMes', 'txNomeParlamentar', ]).reset_index().rename(columns={
                'vlrLiquido': 'total'})
        df_compatativo.drop('numMes', inplace=True, axis=1)
        df_compatativo['total'] = df_compatativo['total']/1000
        return df_compatativo


    def ranking_partidos():
        df_sum_legenda = df_desp_dept[['sgPartido', 'vlrLiquido', 'txNomeParlamentar']].groupby(
            ['sgPartido']).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).reset_index()

        df_sum_legenda['valor_medio'] = df_sum_legenda['vlrLiquido'] / \
            df_sum_legenda['txNomeParlamentar']

        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']

        df_pos.nome = df_pos.nome.str.lower()
        df_sum_legenda.sgPartido = df_sum_legenda.sgPartido.str.lower()

        df_sum_legenda = df_sum_legenda.merge(
        df_pos, left_on='sgPartido', right_on='nome')


        print(df_sum_legenda.head())
        return df_sum_legenda


    def get_chart_map(sgPartido):
        df_desp_dept_vl_map = df_desp_dept
        if sgPartido:
            if sgPartido=='SDD':
                sgPartido='SOLIDARIEDADE'
            df_desp_dept_vl_map = df_desp_dept[df_desp_dept['sgPartido'] == sgPartido]

        df_cota[['UF', 'VALOR']].groupby(['UF']).sum().sort_values(
            ['VALOR'], ascending=False).reset_index().rename(columns={'VALOR': 'total_cota'})

        df_desp_dept_vl_map = df_desp_dept_vl_map[['sgUF', 'vlrLiquido', 'txNomeParlamentar']].groupby(
            ['sgUF']).agg(
            {'vlrLiquido': np.sum, 'txNomeParlamentar': pd.Series.nunique}).sort_values(['vlrLiquido'],
                                                                                        ascending=False).reset_index()
        df_desp_dept_vl_map['des_percapt'] = (
            df_desp_dept_vl_map['vlrLiquido']/df_desp_dept_vl_map['txNomeParlamentar'])/12

        df_desp_dept_vl_map['vlrLiquido'] = df_desp_dept_vl_map['vlrLiquido']

        merged = brasil_map.set_index('UF_05').join(
            df_desp_dept_vl_map.set_index('sgUF'))

        merged = merged.merge(
            df_cota, left_on=merged.index, right_on='UF')
        merged = merged.set_index('UF')
        merged.vlrLiquido = merged.vlrLiquido.fillna(0)
        merged.txNomeParlamentar = merged.txNomeParlamentar.fillna(0)
        merged.VALOR = merged.VALOR.fillna(0)
        merged.des_percapt = merged.des_percapt.fillna(0)

        return merged


    def get_options_candidato():
        return [{"label": f"{x['txNomeParlamentar']} - {x['sgUF']} - {x['sgPartido']} ", "value": x['txNomeParlamentar']} for _, x in df_desp_dept[['txNomeParlamentar', 'sgPartido', 'sgUF']].drop_duplicates().iterrows()]


    def df_treemap(click_event):

        df_sum_legenda = df_desp_dept
        if click_event:
            if click_event=='SDD':
                click_event='SOLIDARIEDADE'
            df_sum_legenda = df_desp_dept[df_desp_dept['sgPartido'] == click_event ]
        
        df_sum_legenda = df_sum_legenda[['sgPartido', 'txtDescricao', 'vlrLiquido']].groupby(
            ['sgPartido', 'txtDescricao']).sum().sort_values('vlrLiquido', ascending=False).reset_index()
        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']
        return df_sum_legenda