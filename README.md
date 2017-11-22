# DeusCoNWeT

Universidad Politécnica de Madrid, Escuela de Informática

Grupo de trabajo de la Escuela Técnica Superior de Ingenieros Informáticos 
de la Universidad Politécnica de Madrid. 

Los miembros de este grupo son:

	· Gómez Yagüez, Sandra (sandragyaguez)
	· Lizcano Casas, David 
	· López Gómez, Genoveva
	· Ortega Moreno, Miguel (Mortega5)
	· Ruiz Ruiz, Luis (lruizr)

## Configuración


Antes de desplegar el portal es necesario configurar los dominios en los que se va a ejecutar, es decir, hay que especificar la direccion sobre la que la vamos a ejecutar. Para ello es necesario cambiar los siguientes ficheros:

### variable del entorno
HTTP_PATH --> Dominio principal
HTTP_PATH --> Dominio de prueba
VERSIOn --> proc or test  (default test)
#### secret.yaml

Es la configuración de las credenciales privadas de las redes sociales. La configuración actual es la siguiente:

```yaml
FACEBOOK_APP_ID: <app_id facebook>
FACEBOOK_APP_SECRET: <app_secret de facebook>
TWITTER_CONSUMER_KEY: <consumer key de twitter>
TWITTER_CONSUMER_SECRET: <consumer secret en twitter>
```

#### mongo.yaml

Fichero de configuración de la conexión con la base de datos. Por ejemplo:

```yaml
host: 10.10.1.88
port: 27017
pwd: pwdProduccion
user: userProduccion
database: dbProduccion
userTest: userTest
pwdTest: pwdTest
databaseTest: databaseTest
```

#### [App.yaml](https://github.com/polymer-spain/DeusCoNWeT/blob/develop/src/app.yaml)

Este fichero hace referencia a la configuración establecida en [Google App Engine (GAE)](https://cloud.google.com/appengine). Deberemos configurarlo de la manera adecuada en función de los datos ofrecidos por esta plataforma. En la variable `application` indicaremos el nombre de nuestro proyecto en GAE. Tambien indicaremos la versión sobre la que estamos desplegando, indicandolo en la variable `version`. Por ejemplo:

```yaml
    application: example-project-13
    version: stable
```

# Lista de componentes
 
Los componentes estan accesibles a través de un repositorio privado de bower. Si se quieren instalar mediente bower,
se tiene que modificar el fichero .bowerrc para que consulte también el servidor donde están alojados.

***.bowerrc***
```json
{
   "directory": "src/static/bower_components",
   "registry": {
        "search":["http://centauro.ls.fi.upm.es:5555", "https://bower.herokuapp.com"],
        "register":"http://centauro.ls.fi.upm.es:5555"
    }
}
```
## [facebook](https://github.com/Mortega5/facebook-wall)
 
Componente que realiza peticiones a la api de facebook para obtener los datos del muro de facebook. Realiza solo una petición
para obtener la información. Cada versión está desplegada en una rama y como una release bajo el nombre #vx.xx-version, por ejemplo
`#v0.9.3-usability`.
 
### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/facebook-wall/demo.html`.
 
 
#### *WARNING*
  * Solo puede usar tokens de usuarios que son developers en la cuenta de desarrollador de Deus. 
  * Introducir un token válido en el fichero demo.html en el atributo access_token del componente

### *NOTAS*
  * En caso de obtener un error por el token, el componente muestra datos mockeados
 
## [google+](https://github.com/ailopera/googleplus-timeline)
 
Componente que muestra la información de google+. Ejecuta dos pasos para mostrar la información. Por un lado pide la
información de a quien sigue el usuario. Una vez que se obtiene la lista de los usuarios a los que sigue, se piden uno a
uno la lista de posts públicos de cada uno de los usuarios a los que sigue. Los posts se piden hasta un cierto día, ya
que si se piden 10 posts de un usuario que publica mucho se obtendrán solo los de un día. En cambio,si es de un usuario
que publica poco se mostrarán de 1 mes atrás. Para simular el comportamiento de un timeline (los datos más recientes)
se piden en función de una fecha.
 
### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/facebook-wall/demo.html`.
 
En la demo sale un botón de login, utilizarlo para utilizar un token válido.
 
### *NOTAS*
  * En caso de obtener un error por el token, el componente muestra datos mockeados
## [twitter](https://github.com/JuanFryS/twitter-timeline)
 
Componente que muestra un timeline con todos los tweet que aparecen en el twitter de un usuario. Se realiza solo una
petición a la api de twitter, a la que se le piden el máximo de tweets posibles. Estos tweets están paginados.

### *NOTAS*
  * La api de twitter tiene limitaciones de 15 peticiones por 15 minutos.
  * En caso de superar este rátio se muestran datos mockeados.

### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/twitter-timeline/static/demo.html`.

 
## [pinterest](https://github.com/Mortega5/pinterest-timeline)

Componente que muestra los tablones a los que sigue un usuario en pinterest. Se realizan varias peticiones. Por un lado
se realizan las peticiones de los tablones a los que sigue un usuario y los dueños de estos tablones. Con estos datos
se obtienen las direcciones de los tablones. **A través de la interacción del usuario** se van mostrando los tablones
a los que va pulsando.

Para simular esta interación en las métricas, en las demos se va pulsando los botones correspondientes a los diferentes
dashboard para recorrerlos todos.

### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/pinterest-timeline/demo/index.html`.

## [finance](https://github.com/Mortega5/finance-search)

Componente que muestra los valores en bolsa de una empresa. Tiene dos fases, por un lado tiene un buscador de empresas
para traducirlo en el simbolo con el cotiza en bolsa. Con ese simbolo se ralizan dos peticiones, una para obtener los
datos actuales  en bolsa y otro para obtener los datos históricos. Los datos históricos son mostrados en una gráfica. 
Las peticiones pasan por un proxy situado en centauro.

Utiliza otros componentes desarrollados por nosotros para ĺa información de los datos historicos, para buscar las empresas
o para obtener los datos actuales.

### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/finance-search/demo/index.html`.

## [weather](https://github.com/Mortega5/open-weather)

Muestra los datos del tiempo en la localización actual del navegador (necesita permisos para conocer la localización). 
Solo realzia una petición que devuelve los datos de ahora más las previsiones cada 3 horas durante los próximos 4 días.
Las peticiones pasan por un proxy situado en centauro.

### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/open-weather/demo/index.html`.

## [traffic](https://github.com/Mortega5/traffic-incidents)

Componente que pide datos de tráfico de una determinada lugar. Los datos que recopila estan dentro de un rango
determinado (100km a la redonda). Realiza dos peticiones: una para localizar el punto, a través de google, y otra para 
localizar las incidencias de tráfico encontradas para ese punto.

Las incidencias son mostradas en el idioma del lugar en el que se producen, es decir, si consultamos incidencias en 
Madrid, estarán en castellano; si las buscamos en Londres, estarán en inglés.

### *NOTAS*
  * Al utilizar la api de google para localizar la busqueda, muestra la localización de donde encuentre la API, exista o no.

### Ejecutar
 
Para poder ver el componente ejecutar primero se debe instalar las dependencias de bower `$ bower install`  y despues 
desplegar un servidor con `$ polyserve` en la raíz del proyecto (si no se tiene se puede instalar de manera global con
 `$ npm install -g polyserve`). Una vez desplegado el servidor, acceder acceder `http://localhost:8080/components/traffic-incidents/demo/index.html`.


