import logging
import azure.functions as func
from Tiempo import Resumen_factory, Resumen_meteorologico
import datetime
CIUDADES = ["madrid","alcala_heranes","getafe","collado_villalba","navalcarnero"]



app = func.FunctionApp()
@app.function_name(name="dbTimer")
@app.timer_trigger(schedule="0 10,20 9 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False) 
@app.generic_output_binding(arg_name="itemCiudad", type="sql", CommandText="dbo.ciudades", ConnectionStringSetting="SqlConnectionString")
def timer_trigger(myTimer: func.TimerRequest,itemCiudad: func.Out[func.SqlRow]) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    factory = Resumen_factory()
    resumen = factory.crear_resumen()


    # print(resumen.ciudades)

    # for ciudad in resumen.ciudades:
        # tupla_ciudad = ciudad.__dict__
    sql_rows = []
    for ciudad in resumen.ciudades:
        ciudad_dict = resumen.ciudades[ciudad].toSQL()
        temp_fecha = ciudad_dict["fecha"]
        ciudad_dict["fecha"] = cambio_fecha(temp_fecha)
        logging.info(ciudad_dict)
        sql_rows.append(func.SqlRow(ciudad_dict) )
        logging.info(f'{ciudad} preparada en db')
    itemCiudad.set(sql_rows)

        # print(type(ciudad))
        # fecha_dict = {"Fecha":fecha_formateada}


    logging.info('Python timer trigger function executed.')

def cambio_fecha(fecha:str):
    dia, mes, year = fecha.split("-")
    return f"{year}-{mes}-{dia}"