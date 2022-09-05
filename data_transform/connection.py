
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


class connection():

    @staticmethod
    def get_engine():
        string_connetion = os.environ.get('CONNECTION_DB')
        db = create_engine('postgresql://argus:argus@0.0.0.0:5432/faz_e_conta')
        return db

    @staticmethod
    def db_connect():
        engine = connection.get_engine()
        conn = engine.connect()
        return conn

    @staticmethod
    def get_base():
        base = declarative_base()
        return base

    @staticmethod
    def create_tables(base):
        engine = connection.get_engine()
        base.metadata.create_all(engine)

    def __enter__(self):
        self.__conn = connection.db_connect()
        return self.__conn
    
    def __exit__(self, exc_type, exc_value, tb):
        self.__conn.close()