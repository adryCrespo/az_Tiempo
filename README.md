# az_Tiempo: Demostración de desarrollo full-stack en Azure con Flask y CI/CD

az_Tiempo es una aplicación web que proporciona pronósticos meteorológicos personalizados para varios municipios de la Comunidad de Madrid. Desarrollada íntegramente en Azure, esta aplicación sirve como demostración de un flujo de trabajo completo, desde el desarrollo hasta la implementación.



## Arquitectura:


![Diseño del proyecto](documentacion\diseno.png)

Tecnologías clave:

- **Frontend**: HTML, CSS
- **Backend**: Flask (Python), Pyodbc
- **Base de datos**: Azure SQL Database (Serverless)  
- **Cloud**: Microsoft Azure (App Service Standard, Azure Functions, Azure Container Registry, Azure Entra ID, Azure Application Insights)
- **CI/CD**: GitHub Actions
- **Contenedores**: Docker
- **API**: el-tiempo.net

Flujo de la aplicación:

    El usuario accede a la aplicación a través de un navegador web.
    La petición llega al Azure App Service, que ejecuta el contenedor Docker de la aplicación Flask.
    Flask consulta la base de datos Azure SQL para obtener los datos históricos y la API de el-tiempo.net para los datos en tiempo real.
    Flask procesa los datos y genera la respuesta HTML, que se envía al navegador del usuario.

Los datos de la base de datos se guardan diariamente mediante una azure function app

### Desarrollo y despliegue:

    El código se desarrolla en GitHub y se utiliza un flujo de trabajo de CI/CD basado en GitHub Actions para automatizar la construcción, las pruebas y el despliegue.
    Las pruebas unitarias y de integración se ejecutan en cada commit para garantizar la calidad del código.
    La aplicación se despliega en Azure App Service como un contenedor Docker, lo que facilita la gestión y el escalado.



## Pagina principal 

La aplicacion tiene dos partes diferenciadas. La página principal, y las páginas propias de cada municipio.
En la página principal se puede ver los valores de meteorológicos de la fecha actual para los distintos municipios.

![pagina_home](documentacion\web_home.png)

El color de fondo de municipios cambia segun el valor de la **temperatura maxima**. Cada uno de los municipios tiene un link para acceder al historico de temperaturas.

## Página municipio

Por ejemplo para el municipio de alcala de henares tenemos
un grafico donde se muestra la evolucion de las temperaturas máximas y mínimas según el tiempo.


![pagina_historico](documentacion\web_historico.png)





