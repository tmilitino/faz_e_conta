import pandas as pd
import numpy as np
from ETL.transform import BaseTransform


class TimeSeriesCandidato(BaseTransform):

    def __init__(self, df_desp):
        self.df_desp = df_desp

    def executor(self):
        self.df_desp['mes_ano'] = self.df_desp.apply(
            lambda x: f"{x.numMes}-{x.numAno}", axis=1)
        df_compatativo = self.df_desp
        df_compatativo = df_compatativo[['nuLegislatura', 'codLegislatura',
                                         'txNomeParlamentar', 'mes_ano',
                                         'vlrLiquido', 'numMes']]\
            .groupby(['nuLegislatura', 'codLegislatura',
                      'txNomeParlamentar', 'mes_ano', 'numMes'])\
            .sum()\
            .sort_index(level=['numMes', 'txNomeParlamentar', ])\
            .reset_index()\
            .rename(columns={'vlrLiquido': 'total'})

        df_compatativo.drop('numMes', inplace=True, axis=1)

        df_compatativo.rename(columns={
            'nuLegislatura':'ano',
            'txNomeParlamentar': 'nome',
            'total': 'valor_liquido',
            'codLegislatura': 'cod_legislacao'
        }, inplace=True)

        return df_compatativo
