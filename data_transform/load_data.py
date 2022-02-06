import pandas as pd
import geopandas as gpd


class LoadData:
    df_desp = pd.DataFrame()
    df_desp_dept = pd.DataFrame()

    df_desp_20 = pd.read_csv('./files/Ano-2020.csv', sep=';')
    df_desp_19 = pd.read_csv('./files/Ano-2019.csv', sep=';')
    df_pos = pd.read_csv('./files/posicao-partidos.csv', sep=';')
    df_cota = pd.read_csv('./files/cota_por_estado.csv', sep=';')
    brasil_map = gpd.read_file('/dash_app/files/brasil.geojson')

    brasil_map['center'] = brasil_map['geometry'].apply(lambda x: x.centroid)
