from sqlalchemy import text
import datetime
import os

import pyodbc
import struct
from azure import identity

class  SQLInitializer:
      def __init__(self):
            self.connString = os.environ["SQLAZURECONNSTR_"+"AZURE_SQL_CONNECTIONSTRING"]


      def get_conn(self):
            credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
            token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
            token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
            SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
            conn = pyodbc.connect(self.connString, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
            return conn

      def query_data(self,sql_query:str):
           with self.get_conn() as connection:
                cursor = connection.cursor()
                cursor.execute(sql_query)
                return cursor.fetchall()
                
class DatabaseManager(SQLInitializer):

    def query_ciudad_db(self,ciudad:str):
            
            sql_query = f"select * from dbo.ciudades where ciudad='{ciudad}' order by fecha asc"
            resultados = self.query_data(sql_query)

            return resultados
    
    def query_ciudad_fecha_db(self,ciudad:str, fecha:str):
            sql_query = f"select * from dbo.ciudades where ciudad='{ciudad}'and fecha='{fecha}' order by fecha asc "
            resultados = self.query_data(sql_query)
            return resultados

    def contar_numeros_ciudad(self, ciudad:str):
            sql_query = f"select count(*) from dbo.ciudades where ciudad='{ciudad}'"
            resultados = self.query_data(sql_query)
            resultados = resultados[0][0]

            if not isinstance(resultados,int):
                  raise TypeError
            
            return resultados

