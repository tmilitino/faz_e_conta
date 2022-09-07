import pandas as pd
import requests
import zipfile
import urllib.parse
import os


class BasicExtract:
    file_name = 'Ano-{ano}.csv.zip'
    url_base = 'http://www.camara.leg.br/cotas/'
    base_dir = './data_transform/ETL/extract/files'

    def executor(self, ano):

        self.__get_file(ano)
        self.__extract_file(ano)
        df_desp = self.__load_file(ano)
        return df_desp

    def __get_file(self, ano):
        file_name = self.file_name.format(ano=ano)
        url_final = urllib.parse.urljoin(self.url_base, file_name)
        base_dir_final = os.path.join(self.base_dir, file_name)

        if os.path.exists(base_dir_final.replace('.zip','')):
            return True

        response = requests.get(url_final, stream=True)
        with open(base_dir_final, 'wb') as fd:
            for chunk in response.iter_content(chunk_size=256):
                fd.write(chunk)

    def __extract_file(self, ano):
        file_name = self.file_name.format(ano=ano)
        base_dir_final = os.path.join(self.base_dir, file_name)

        if os.path.exists(base_dir_final.replace('.zip','')):
            return True

        zip_file = zipfile.ZipFile(base_dir_final)
        zip_file.extractall(self.base_dir)

    def __load_file(self, ano):
        file_name = self.file_name.replace('.zip', '')
        file_name = file_name.format(ano=ano)
        base_dir_final = os.path.join(self.base_dir, file_name)

        return pd.read_csv(base_dir_final, sep=';')
