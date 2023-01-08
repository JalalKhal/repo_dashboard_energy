import pandas as pd
import urllib
from sqlalchemy import create_engine
from sqlalchemy import inspect

class ProcessSQL:
    database_name="energy_dbs"
    #connection to the SQL Server in docker container
    params=urllib.parse.quote_plus('Driver={ODBC Driver 18 for SQL Server};'
                                   'Server=localhost;'
                                   f"Database={database_name};"
                                   "UID=sa;"
                                   "PWD=Stackover75;"
                                   'Trusted_Connection=no;'
                                   "TrustServerCertificate=yes;")
    engine=create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    #connection to the database created before by docker container with sqlalchemy
    def __init__(self,table_name,data_json_str=""):
        """
        :param data_json_str: json str given by mongoDB queries into mongoDB server,
                if data_json_str="": for dash dashboards for push_sql_server method
        :param table_name:name of the SQL table for the specific energy
        """
        self.data_json_str=data_json_str
        self.table_name=table_name

    def process_data(self):
        """
        :return: DataFrame for data_json_str for insertion to SQL Server
        """
        raise NotImplementedError(f"This method should be implemented for the processing of data{self.data_json_str}")


    def get_mask(self,df,df_inserver):
        """
        :param df: dataframe for the table of the specific energy
        :return: mask for don't insert duplicates in the table.
        """
        raise NotImplementedError(f"This method should be implemented for getting mask condition for don't add duplicates")


    def push_sqlserver(self):
        """
        push the dataframe given by process_data in SQL Server in the table specified by self.table_name
        """
        df=self.process_data()
        if not inspect(ProcessSQL.engine).has_table(self.table_name):
            df.to_sql(self.table_name,con=ProcessSQL.engine,if_exists="replace",index=False)
        else:
            df_inserver=pd.read_sql(f"SELECT * FROM dbo.{self.table_name}",con=ProcessSQL.engine)
            df.loc[self.get_mask(df,df_inserver)].to_sql(self.table_name,con=ProcessSQL.engine,\
                                                               if_exists="append",index=False)

    def get_sqlserver(self):
        """
        get the dataframe stored in the SQL Server for dash Applications to create dashboards
        """
        return pd.read_sql(f"SELECT * FROM dbo.{self.table_name}",con=ProcessSQL.engine)










