from connection import connection


class BaseLoad():

    def __init__(self, table_name, df_target) -> None:
        self.table_name = table_name
        self.df_target = df_target
    
    def executor(self,):
        with connection() as conn:
            self.df_target.to_sql(self.table_name, con=conn, if_exists='append',
            index=False,)
