# az_Tiempo

## objetivo del proyecto

El proyecto az_Tiempo dará un parte meteorológico de algunos de los municipios de la comunidad de Madrid. En particular de Madrid, Alcala de Henares, Getafe, Navalcarnero, y Collado villalba.
La app mostrará información meteorológica del dia de hoy y también dara información histórica sobre la temperatura máxima y mínima.

## Diseño
La app corre en la nube de Azure, utilizando un framework de Flask para su desarrollo.
Esta aplicación consta de dos contenedores de docker, uno que actua como servidor de la app y en el cual está la aplicación Flask, y el otro que contiene un servicio de base de datos Postgres, dedicado a almacenar el histórico de los datos. Estos contendores se ejecutan dentro de Azure mediante el servicio de Azure Container Instances. 
Además, se ha implementado un sistema de CI/CD usando una combinación de github actions y Azure Resource Manager con los que se consigue un despliegue e integración automática.


```
http://az-tiempo-project.uksouth.azurecontainer.io:8000/
```
