from ETL.transform import BaseTransform


class DespesasPartidos(BaseTransform):

    def __init__(self, df_desp):
        self.df_desp = df_desp

    def executor(self):
        df_sum_legenda = self.df_desp

        df_sum_legenda = df_sum_legenda[['nuLegislatura', 'codLegislatura',
                                         'sgPartido', 'txtDescricao', 'vlrLiquido']]\
            .groupby(['nuLegislatura', 'codLegislatura',
                      'sgPartido', 'txtDescricao'])\
            .sum()\
            .sort_values('vlrLiquido', ascending=False)\
            .reset_index()

        df_sum_legenda['vlrLiquido'] = df_sum_legenda['vlrLiquido']

        df_sum_legenda.rename(columns={
            'nuLegislatura':'ano',
            'sgPartido': 'sg_partido',
            'txtDescricao': 'descricao_despesa',
            'vlrLiquido': 'valor_liquido',
            'codLegislatura': 'cod_legislacao'
        }, inplace=True)

        return df_sum_legenda
