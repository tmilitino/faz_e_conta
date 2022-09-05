import pandas as pd
import numpy as np
from ETL.transform import BaseTransform

class DistribuicaoPartido(BaseTransform):

    def __init__(self, df_desp):
        self.df_desp = df_desp

    def executor(self):
        df_dept_scatter = self.df_desp[['nuLegislatura','codLegislatura',
                                        'sgPartido', 'vlrLiquido',
                                        'txNomeParlamentar']]

        df_dept_scatter = df_dept_scatter.groupby(['nuLegislatura','codLegislatura', 'sgPartido'],)\
            .agg({'vlrLiquido': np.sum,
                  'txNomeParlamentar': pd.Series.nunique})\
            .reset_index()

        df_dept_scatter['vlrLiquido'] = df_dept_scatter['vlrLiquido']
        
        df_dept_scatter.rename(columns={
            'nuLegislatura':'ano',
            'txNomeParlamentar': 'total_parlamentar',
            'sgPartido': 'sg_partido',
            'vlrLiquido': 'valor_liquido',
            'codLegislatura': 'cod_legislacao'
        }, inplace=True)

        return df_dept_scatter
