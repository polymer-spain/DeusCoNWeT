""" Copyright 2014 Luis Ruiz Ruiz
    Copyright 2014 Ana Isabel Lopera Martinez
    Copyright 2014 Miguel Ortega Moreno
    Copyright 2014 Juan Francisco Salamanca Carmona

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from google.appengine.ext import ndb
import webapp2
import json
"""NDB Instances """

class Usuario(ndb.Model):
  # "Usuario"
  email_usuario = ndb.StringProperty()
  telefono_usuario = ndb.IntegerProperty()
  descripcion_usuario = ndb.TextProperty()
    #"Lista de redes"
  nombre_rs_pertenece_usuario = ndb.StringProperty(repeated=True)
  siguiendo_rs_pertenece_usuario = ndb.IntegerProperty(repeated=True)
  seguidores_rs_pertenece_usuario = ndb.IntegerProperty(repeated=True)
  url_sig_rs_pertenece_usuario = ndb.StringProperty(repeated=True)
  url_seg_rs_pertenece_usuario = ndb.StringProperty(repeated=True)
    # "lista_Grupos"
  nombre_grupo_pertenece_usuario = ndb.StringProperty(repeated=True)
  lista_Usuarios_grupo_pertenece_usuario = ndb.StringProperty(repeated=True)
  descripcion_grupo_pertenece_usuario = ndb.StringProperty(repeated=True)
    # "Valoracion"
  name_valorada = ndb.StringProperty(repeated=True)
  rating_value_valorada = ndb.FloatProperty(repeated=True)
    # "componentes_usuario"
  nombre_componente_usuario = ndb.StringProperty(repeated=True)
  x_componente_usuario = ndb.FloatProperty(repeated=True)
  y_componente_usuario = ndb.FloatProperty(repeated=True)
  url_componente_usuario = ndb.StringProperty(repeated=True)
  height_componente_usuario = ndb.StringProperty(repeated=True)
  width_componente_usuario = ndb.StringProperty(repeated=True)
    # "token_usuario"
  id_fb_usuario = ndb.StringProperty()
  token_fb_usuario = ndb.StringProperty()
  id_tw_usuario = ndb.StringProperty()
  token_tw_usuario = ndb.StringProperty()
  id_sof_usuario = ndb.StringProperty()
  token_sof_usuario = ndb.StringProperty()
  id_li_usuario = ndb.StringProperty()
  token_li_usuario = ndb.StringProperty()
  id_ins_usuario = ndb.StringProperty()
  token_ins_usuario = ndb.StringProperty()
  id_git_usuario = ndb.StringProperty()
  token_git_usuario = ndb.StringProperty()
  id_google_usuario = ndb.StringProperty()
  token_google_usuario = ndb.StringProperty()

# Definicion de metodos para manejar la base de datos
#Comprobado
@ndb.transactional
def insertarUsuario(datos=None):
  usuario = Usuario()
  if not datos == None:
    if datos.has_key("email"):
      usuario.email_usuario = datos["email"]
    if datos.has_key("telefono"):
      usuario.telefono_usuario = datos["telefono"]
    if datos.has_key("descripcion"):
      usuario.descripcion_usuario = datos["descripcion"]
  user_key = usuario.put()

  return user_key  
#Comprobado
def actualizarUsuario(user_key, datos):
  usuario = user_key.get()
  if not datos == None: 
    if datos.has_key("email"):
      usuario.email_usuario = datos["email"]
    if datos.has_key("telefono"):
      usuario.telefono_usuario = datos["telefono"]
    if datos.has_key("descripcion"):
      usuario.descripcion_usuario = datos["descripcion"]
  
  usuario.put()
#Comprobado
def buscarUsuario(user_key):
  usuario = user_key.get()
  datos = {"email": usuario.email_usuario,
            "telefono": usuario.telefono_usuario,
            "descripcion":usuario.descripcion,
            "grupos": usuario.nombre_grupo_pertenece_usuario,
            "redes": usuario.nombre_rs_pertenece_usuario}
  datos = json.dumps(datos)

  return datos
#Comprobado
def insertaToken(user_key, rs, token):
  usuario = user_key.get()
  if rs == "facebook":
    usuario.token_fb_usuario = token
  elif rs == "twitter":
    usuario.token_tw_usuario = token
  elif rs == "instagram":
    usuario.token_ins_usuario = token
  elif rs == "github":
    usuario.token_git_usuario = token
  elif rs == "stack-overflow":
    usuario.token_sof_usuario = token
  elif rs == "linkedin":
    usuario.token_li_usuario = token
  elif rs == "google":
    usuario.token_google_usuario = token
  else:
    return "La red social solicitada no esta contemplada"

  usuario.put()
#Comprobado
def getToken(user_key, rs):
  usuario = user_key.get()
  res = ''
  if rs == "facebook":
    res = usuario.token_fb_usuario
  elif rs == "twitter":
    res = usuario.token_tw_usuario
  elif rs == "stack-overflow":
    res = usuario.token_sof_usuario
  elif rs == "linkedin":
    res = usuario.token_li_usuario
  elif rs == "instagram":
    res = usuario.token_ins_usuario
  elif rs == "github":
    res = usuario.token_git_usuario
  elif rs == "google":
    res = usuario.token_goolge_usuario
  else:
    return "La red social solicitada no esta contemplada"
  return res
#Comprobado
def insertaIdRS(user_key, rs, id_user):
  usuario = user_key.get()
  if rs == "facebook":
    usuario.id_fb_usuario = id_user
  elif rs == "twitter":
    usuario.id_tw_usuario = id_user
  elif rs == "instagram":
    usuario.id_ins_usuario = id_user
  elif rs == "github":
    usuario.id_git_usuario = id_user
  elif rs == "stack-overflow":
    usuario.id_sof_usuario = id_user
  elif rs == "linkedin":
    usuario.id_li_usuario = id_user
  elif rs == "google":
    usuario.id_google_usuario = id_user
  else:
    return "La red social solicitada no esta contemplada"
  
  usuario.put()
#Comprobado
def getIdRS(user_key, rs):
  usuario = user_key.get()
  if rs == "facebook":
    identificador = usuario.id_fb_usuario
  elif rs == "twitter":
    identificador = usuario.id_tw_usuario
  elif rs == "stack-overflow":
    identificador = usuario.id_sof_usuario
  elif rs == "linkedin":
    identificador = usuario.id_li_usuario
  elif rs == "instagram":
    identificador = usuario.id_ins_usuario
  elif rs == "github":
    identificador = usuario.id_git_usuario
  elif rs == "google":
    identificador = usuario.id_google_usuario
  else:
    return "La red social solicitada no esta contemplada"

  return identificador
#Comprobado
def insertaGrupo(user_key, grupos=[]):
  usuario = user_key.get()
  if len(grupos) > 0:
    for grupo in grupos:
      usuario.nombre_grupo_pertenece_usuario.append(grupo)
  else:
    return "No se especifica ningun grupo que anadir"
#Comprobado
def buscarGrupo(user_key):
  usuario = user_key.get()
  datos = {}
  contador = 0
  res = {} 
  # Diferente opcion, diferente funcionalidad
  # res = [None]*len(usuario.nombre_grupo_pertenece_usuario)
  if len(usuario.nombre_grupo_pertenece_usuario) > 0:
    for grupo in usuario.nombre_grupo_pertenece_usuario:
      res[contador] = grupo
      contador += 1

  return json.dumps(res)
#Comprobado
def insertaRed(user_key, redes=[]):
  usuario = user_key.get()
  if len(redes) > 0:
    for red in redes:
      usuario.nombre_rs_pertenece_usuario.append(red)
  else:
    return "No se especifica ninguna red que anadir"
#Comprobado
def buscarRed(user_key):
  usuario = user_key.get()
  res = {}
  contador = 1
  if len(usuario.nombre_rs_pertenece_usuario) > 0:
    for red in usuario.nombre_rs_pertenece_usuario:
      res[contador] = red
      contador += 1

  return json.dumps(res)

def insertarComponente(user_key, nombre, coord_x=0.0, coord_y=0.0, url="", height="", width=""):
  usuario = user_key.get()

  usuario.nombre_componente_usuario.append(nombre)
  usuario.x_componente_usuario.append(coord_x)
  usuario.y_componente_usuario.append(coord_y)
  usuario.url_componente_usuario.append(url)
  usuario.height_componente_usuario.append(height)
  usuario.width_componente_usuario.append(width)

  usuario.put()

def modificarComponente(user_key, nombre, datos):
  usuario = user_key.get()
  encontrado = False
  for i in range(0,len(usuario.nombre_componente_usuario)):
    if(usuario.nombre_componente_usuario[i] == nombre):
      encontrado = True
      if datos.has_key("coord_x"):
        usuario.x_componente_usuario[i] = datos["coord_x"]
      if datos.has_key("coord_y"):
        usuario.y_componente_usuario[i] = datos["coord_y"]
      if datos.has_key("url"):
        usuario.url_componente_usuario[i] = datos["url"]
      if datos.has_key("height"):
        usuario.height_componente_usuario[i] = datos["height"]
      if datos.has_key("width"):
        usuario.width_componente_usuario[i] = datos["width"]
      return ""
  if encontrado == False:
    return "No existe un componente con ese nombre"
  usuario.put()