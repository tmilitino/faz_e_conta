import pandas as pd

class BasicExtract:

    def executor(self):
        df_desp = pd.read_csv('data_transform/ETL/extract/files/Ano-2020.csv', sep=';')
        return df_desp