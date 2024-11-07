from sqlalchemy import create_engine
from sqlalchemy import text
import psycopg2
import datetime


class  SQLInitializer:
      def __init__(self):
            # connection_string = 'postgresql://root:root@localhost:5432/root'
            connection_string = 'postgresql://root:root@flask-db:5432/root'
            self.engine = create_engine(connection_string, echo=True)    

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
