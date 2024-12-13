
from flask import Flask,request,render_template,Response, jsonify
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
# from config import Config
from http import HTTPStatus
from sqlalchemy import text
import json
import psycopg2
from Tiempo import Resumen_factory, Resumen_meteorologico
import datetime
from database_ops import DatabaseManager,InsertSQLManager
import matplotlib.pyplot as plt
import io
import base64
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from logica_css import get_css
import logging

import logging

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

app = Flask(__name__,template_folder="template",static_folder="static",static_url_path="/")
# connection_string = 'postgresql://root:root@flask-db:5432/root'
# connection_string = 'postgresql://root:root@localhost:5432/root'
# engine = create_engine(connection_string, echo=True)
CIUDADES = ["madrid","alcala_heranes","getafe","collado_villalba","navalcarnero"]

     

            
@app.route('/',methods=["GET","POST"]) 
def home(): 
    factory = Resumen_factory()
    resumen = factory.crear_resumen()
    ciudades = CIUDADES
    logger.info("pagina inicial")
    # insertar_datos_ciudades(resumen=resumen, ciudades=CIUDADES)
    return render_template("index.html",resumen=resumen,ciudades=ciudades, get_css =get_css)

@app.template_filter('formato_nombre_ciudad')
def formato_nombre_ciudad(s:str):
    temp = s.replace("_"," ")
    return ' '.join(word.capitalize() for word in temp.split())


# def insertar_datos_ciudades( resumen:Resumen_meteorologico, ciudades:list = None ):
#         insert_SQL_instance = InsertSQLManager()
#         for ciudad in ciudades:
#              t_min, t_max = resumen.get_dato_ciudad(nombre_ciudad=ciudad)
#              insert_SQL_instance.insert_row_db(ciudad,t_min,t_max)


@app.template_filter('b64encode')
def b64encode(s):
    return base64.b64encode(s)

@app.route('/ciudad/<ciudad>', methods=['GET'])
def ciudad_url(ciudad):
    if request.method == "GET":
        if ciudad not in CIUDADES:
            return render_template('404.html'), 404
        
    # return f"ciudad {ciudad} no implementada"
        

        now = datetime.datetime.now()
        day = now.date().strftime("%d-%m-%Y")
        # dato
        logger.info(f"ciudad: {ciudad} \t dia: {day}")

        dbm = DatabaseManager()
        dato = dbm.contar_numeros_ciudad(ciudad=ciudad)
        logger.info(f"dato sql: {dato}")
        return render_template("ciudad.html",ciudad = ciudad, dia=day,dato=dato)



@app.route('/plot/<ciudad>')
def plot_png(ciudad):
    fig = create_figure(ciudad)
    output = io.BytesIO()
    plt.savefig(output, format='png',bbox_inches='tight')
    output.seek(0)
    return Response(output.getvalue(), mimetype='image/png')


# def create_figure(nombre_ciudad:str):
#     pass
def create_figure(nombre_ciudad:str):
     
     dm = DatabaseManager()
     result = dm.query_ciudad_db(nombre_ciudad)
     logger.info(f"resultados query: {result[:3]}")
     fecha,ciudad,description, t_min, t_max = zip(*result)

     f, ax = plt.subplots(figsize=(12, 7))
     ax.set_title(f'Evolucion Temperaturas a lo largo del tiempo en {nombre_ciudad}',fontsize=15,fontweight='bold')

     ax.set_xlabel('Fecha',fontsize=20, fontweight='bold')
     ax.set_ylabel('Temperatura (ºC)',fontsize=20, fontweight='bold')
     ax.plot(fecha,t_min, label = "Temperatura Minima")
     ax.plot(fecha, t_max, label = "Temperatura Maxima")
     ax.legend(bbox_to_anchor=(1.25, 1),loc = 'upper right')
     ax.tick_params(axis='x', labelsize=12, labelrotation=45)
     ax.tick_params(axis='y', labelsize=20)
     ax.grid(color='gray', linestyle=':', linewidth=1)

     return f
