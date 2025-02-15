import requests
from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class Parte_diario:
    resumen: str 

@dataclass
class Ciudad:
    nombre: str
    descripcion : str
    t_min: float
    t_max: float 

    def get_data(self, atributo:str):
        if atributo not in ["nombre", "description", "t_min", "t_max"]:
            TypeError("atributo desconocido")
        atr_dict = {
        "description":self.descripcion,
         "t_min": self.t_min,
         "t_max": self.t_max
         }
        return atr_dict[atributo]

class Resumen_factory:
    def __init__(self):
        CIUDADES = {
        "madrid": 0,
        "alcala_heranes": 1,
        "getafe": 2,
        "collado_villalba": 3,
        "navalcarnero":4}
        self.CIUDADES = CIUDADES
        URL = "https://www.el-tiempo.net/api/json/v2/provincias/28"
        response_ = requests.get(url=URL)
        self.response = response_.json()

    def get_parte_madrid(self):    
        resumen_general_madrid =  self.response["today"]["p"]
        return Parte_diario(resumen=resumen_general_madrid)
    
    def get_datos_ciudad(self,nombre_ciudad:str): 


        ciudad_id = self.CIUDADES[nombre_ciudad]
        temp = self.response["ciudades"][ciudad_id]
        descript = temp["stateSky"]["description"]
        t_min = temp["temperatures"]["min"]
        t_max = temp["temperatures"]["max"]
        return Ciudad(nombre=nombre_ciudad, descripcion=descript, t_min=t_min, t_max=t_max)
        
    def crear_resumen(self):

        resumen = Resumen_meteorologico(parte_diario=self.get_parte_madrid())
        for nombre_ciudad in list(self.CIUDADES.keys()):
            ciudad = self.get_datos_ciudad(nombre_ciudad)
        
            resumen.append_ciudad(nombre_ciudad,ciudad)
        return resumen

@dataclass
class Resumen_meteorologico:
    parte_diario: Parte_diario
    ciudades: dict = field(default_factory=dict)

    def append_ciudad(self,nombre_ciudad:str, ciudad:  Ciudad):
        self.ciudades.update({nombre_ciudad:ciudad})

    def get_dato_ciudad_atributo(self, nombre_ciudad,atributo):
        if atributo not in ["nombre", "description", "t_min", "t_max"]:
            TypeError("atributo desconocido")

        ciudad= self.ciudades[nombre_ciudad]
        return ciudad.get_data(atributo)
    
    def get_dato_ciudad(self, nombre_ciudad):


        ciudad= self.ciudades[nombre_ciudad]
        return (ciudad.get_data("t_min"),ciudad.get_data("t_max")  )  
    def get_parte_diario(self):
        return self.parte_diario.resumen

if __name__ == "__main__":

    factory = Resumen_factory()
    resumen = factory.crear_resumen()
    print(resumen.ciudades)
