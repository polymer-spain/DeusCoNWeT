# DeusCoNWeT
 Universidad Politécnica de Madrid, Escuela de Informática

Grupo de trabajo de la Escuela Técnica Superior de Ingenieros Informáticos 
de la Universidad Politécnica de Madrid. 

Los miembros de este grupo son:

    · Arato, Razvan (rarato)
	· Castaño Burgos, Alberto (acburgos)
	· Herranz Fernández, David (dh1118)
	· Lizcano Casas, David 
	· Lopera Martínez, Ana Isabel (ailopera)
	· López Gómez, Genoveva
	· Madridejos Zamorano, Enrique (EnriqueMZ)
	· Ortega Moreno, Miguel (Mortega5)
	· Ruiz Ruiz, Luis (lruizr)
	· Salamanca Carmona, Juan Francisco (JuanFryS)

## Configuración

Antes de desplegar el portal es necesario configurar los dominios en los que se va a ejecutar, es decir, hay que especificar la direccion sobre la que la vamos a ejecutar. Para ello es necesario cambiar los siguientes ficheros:


#### [Config.yaml](https://github.com/polymer-spain/DeusCoNWeT/blob/develop/src/api_handlers/config.yaml)

Indicaremos en la variable `domain` el mismo dominio que se indico en Services.js. Esta variable hace referencia a la direccion de nuestro servicio de backend. En este caso no indicaremos el protocolo:
```yaml
    domain: example-project-13.appspot.com
```

#### [App.yaml](https://github.com/polymer-spain/DeusCoNWeT/blob/develop/src/app.yaml)

Este fichero hace referencia a la configuración establecida en [Google App Engine (GAE)](https://cloud.google.com/appengine). Deberemos configurarlo de la manera adecuada en función de los datos ofrecidos por esta plataforma. En la variable `application` indicaremos el nombre de nuestro proyecto en GAE. Tambien indicaremos la versión sobre la que estamos desplegando, indicandolo en la variable `version`. Por ejemplo:

```yaml
    application: example-project-13
    version: stable
```
