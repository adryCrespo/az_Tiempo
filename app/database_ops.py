from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2
import datetime
import os

import pyodbc
import struct
from azure import identity

class  SQLInitializer:
      def __init__(self):
            # connection_string = 'postgresql://root:root@flask-db:5432/root'
            # connection_string = 'Server=tcp:server201124.database.windows.net,1433;Initial Catalog=db201124;Persist Security Info=False;User ID=8718f41f-38f7-4fb9-ba85-aabe535ec5f1;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Authentication="Active Directory Managed Identity";'
            self.connString = os.environ["AZURE_SQL_CONNECTIONSTRING"]
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
                
class DatabaseManager(SQLInitializer):

    def query_ciudad_db(self,ciudad:str):
            sql = text(f"select * from public.ciudades where ciudad='{ciudad}'")
            with self.engine.connect() as connection:
                result = connection.execute(sql).fetchall()
            return result
    def query_ciudad_fecha_db(self,ciudad:str, fecha:str):
            sql = text(f"select * from public.ciudades where ciudad='{ciudad}'and fecha='{fecha}' order by '{fecha}' asc ")
            with self.engine.connect() as connection:
                result = connection.execute(sql).fetchall()
            return result

    def contar_numeros_ciudad(self, ciudad:str):
            sql_query = f"select count(*) from public.ciudades where ciudad='{ciudad}'"
            return self.query_data(sql_query)
            
            with self.engine.connect() as connection:
                result = connection.execute(sql).fetchall()
            return result
class InsertSQLManager(SQLInitializer):


    def insert_row_db(self,ciudad:str, t_min:float, t_max:float, fecha=None):
          #### fecha malll is NOne
          if fecha is None:
               now = datetime.datetime.now()
               fecha = now.date().strftime("%d-%m-%Y")

          if self.have_data_ciudad_fecha_bool(ciudad,fecha) is True:
                print(f"ya hay datos ciudad {ciudad} para la fecha {fecha}")
                return None

          self._insert_row_db(ciudad, t_min, t_max, fecha=fecha)
          print(f"insertado datos ciudad: {ciudad} fecha: {fecha}")

    def have_data_ciudad_fecha_bool(self,ciudad:str,fecha:str):
            sql = text(f"select count(*) from public.ciudades where ciudad='{ciudad}' and fecha='{fecha}'")
            with self.engine.connect() as connection:
                conteo_filas = connection.execute(sql).fetchone()[0]
            return True if conteo_filas > 0 else False

    def _insert_row_db(self,ciudad:str, t_min:float, t_max:float, fecha:str):
        sql_query = f"INSERT INTO public.ciudades(ciudad,fecha, t_min, t_max) VALUES ('{ciudad}','{fecha}', {t_min}, {t_max}  );"
        sql = text(sql_query)
        with self.engine.connect() as connection:
             result = connection.execute(sql)
             connection.commit()
             
class SQLAnalyzer(SQLInitializer):
    pass
