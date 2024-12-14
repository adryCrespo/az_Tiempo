# from sqlalchemy import create_engine
# from sqlalchemy import text
# import psycopg2
import datetime
import os

import pyodbc
import struct
from azure import identity

class  SQLInitializer:
      def __init__(self):
            # connection_string = 'postgresql://root:root@flask-db:5432/root'
            # connection_string = 'Server=tcp:server201124.database.windows.net,1433;Initial Catalog=db201124;Persist Security Info=False;User ID=8718f41f-38f7-4fb9-ba85-aabe535ec5f1;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Authentication="Active Directory Managed Identity";'
            self.connString = os.environ["SQLAZURECONNSTR_"+"AZURE_SQL_CONNECTIONSTRING"]
            #sql authen- connection_string = 'Server=tcp:server201124.database.windows.net,1433;Database=db201124;Uid=admin112;Pwd=Lololo112;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
            # connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:server201124.database.windows.net,1433;Database=db201124;Uid=admin112;Pwd=Lololo112;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
            # self.engine = create_engine(connection_string, echo=True)    


      def get_conn(self):
            # credential = identity.ManagedIdentityCredential(client_id="8718f41f-38f7-4fb9-ba85-aabe535ec5f1")
            credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)
            # token_bytes = credential.get_token("https://database.windows.net/").token.encode("UTF-16-LE")
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
                
class DatabaseManager:

    def query_ciudad_db(self,ciudad:str):
            import pandas as pd
            data = pd.read_csv("app\\datos_nuevos.csv")
            df = data.query("ciudad=='madrid'")
            return df.apply(tuple,axis=1).to_list()
            # sql_query = f"select * from dbo.ciudades where ciudad='{ciudad}' order by fecha asc"
            # resultados = self.query_data(sql_query)

            # return resultados
            with self.engine.connect() as connection:
                result = connection.execute(sql).fetchall()
            return result
    def query_ciudad_fecha_db(self,ciudad:str, fecha:str):
            # sql_query = f"select * from dbo.ciudades where ciudad='{ciudad}'and fecha='{fecha}' order by fecha asc "
            # resultados = self.query_data(sql_query)
            # return resultados
            pass
            # with self.engine.connect() as connection:
            #     result = connection.execute(sql).fetchall()

    def contar_numeros_ciudad(self, ciudad:str):
            return 2
            # sql_query = f"select count(*) from dbo.ciudades where ciudad='{ciudad}'"
            # resultados = self.query_data(sql_query)
            # resultados = resultados[0][0]

            # if not isinstance(resultados,int):
            #       raise TypeError
            
            # return resultados

if "__main__" == __name__:
     dm = DatabaseManager()
     x = dm.query_ciudad_db(ciudad="ma") 
     print(x)