import pandas as pd
import numpy as np
from ETL.transform import BaseTransform

BaseTransform
class DespesasTotais(BaseTransform):

    def __init__(self, df_desp):
        self.df_desp = df_desp

    def executor(self):
        df_dept = self.df_desp[[
            'nuLegislatura','codLegislatura', 'sgPartido', 'sgUF', 'vlrLiquido', 'txNomeParlamentar']]
        df_dept = df_dept.groupby(['nuLegislatura','codLegislatura', 'sgPartido', 'sgUF', 'txNomeParlamentar'],).agg(
            {'vlrLiquido': np.sum}).reset_index()

        df_dept['vlrLiquido'] = df_dept['vlrLiquido']

        df_dept.rename(columns={
            'nuLegislatura':'ano',
            'txNomeParlamentar': 'nome',
            'sgPartido': 'sg_partido',
            'sgUF': 'sg_uf',
            'vlrLiquido': 'valor_liquido',
            'codLegislatura': 'cod_legislacao'
        }, inplace=True)

        return df_dept
