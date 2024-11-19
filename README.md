# az_Tiempo

## objetivo del proyecto

El proyecto az_Tiempo dará un parte meteorológico de algunos de los municipios de la comunidad de Madrid. En particular de Madrid, Alcala de Henares, Getafe, Navalcarnero, y Collado villalba.
La app mostrará información meteorológica del dia de hoy y también dara información histórica sobre la temperatura máxima y mínima.

## Diseño
La app corre en la nube de Azure. Como es una aplicación pequeña se ha elegido el framework de Flask para el desarrollo.
La aplicación se ha desarrollado en Flask que corre en un contenedor de docker. Este a su vez corre sobre el servicio de Azure Container Instances. 
Se ha implementado un sistema de CI/CD usando github actions más los templates de Azure Resource Manager con los que se consigue un despliegue e integración automática.



