# Sherpa

El proyecto funciona usando Django junto a django rest framework y como base de datos PostgreSQL.
El proyecto por comodida esta usando el servidor de django, pero para producción se deberia usar otro, como por ejemplo gunicorn.

## Prerequisitos

* Se necesita tener docker y docker compose instalado para poder ejecutar el proyecto en local.
* Antes de arrancarlo hay que crear el fichero.env. Para ello duplciarlo del fichero .evn.local y se ha de rellenar la variable de entorno **GEONAMES_USERNAME** con el nombre de usuario de https://www.geonames.org si no se podra acceder a la api.
* Se ha de tener libre los puertos **8086** y **5452** para que django y la base de datos puedan arrancar. Si estan ocupados se pueden cambiar en el docker compose.

## Iniciar 

Para iniciar el proyecto solo se tienes que estar en el directorio y ejecutar `make local.start`

Una vez iniciado el proyecto este tiene swagger instalado y se pueden hacer pruebas usando dicha interfaz. La ruta es la siguiente: http://localhost:8086/swagger

## Ejecucion de test

Los test funciona usando pytest, para ejecutarlos se tiene que entrar dentro del contenedor usando el comando: `docker exec -it sherpa bash`
Una vez dentro se ha de ejecutar el comando `pytest`.
