import pandas as pd
import numpy as np
from ETL.transform import BaseTransform

BaseTransform


class RankingPartido(BaseTransform):

    def __init__(self, df_desp):
        self.df_desp = df_desp

    def executor(self):
        df_sum_legenda = self.df_desp[['nuLegislatura','codLegislatura', 'sgPartido',
                                       'vlrLiquido', 'txNomeParlamentar']]\
            .groupby(['nuLegislatura','codLegislatura', 'sgPartido'])\
            .agg({'vlrLiquido': np.sum,
                  'txNomeParlamentar': pd.Series.nunique}).reset_index()


        df_sum_legenda['valor_medio'] = df_sum_legenda['vlrLiquido'] / \
            df_sum_legenda['txNomeParlamentar']

        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']

        df_sum_legenda.rename(columns={
            'nuLegislatura':'ano',
            'sgPartido': 'sg_partido',
            'vlrLiquido': 'valor_liquido',
            'codLegislatura': 'cod_legislacao'
        }, inplace=True)

        df_sum_legenda.drop('txNomeParlamentar', axis=1, inplace=True)
        return df_sum_legenda
