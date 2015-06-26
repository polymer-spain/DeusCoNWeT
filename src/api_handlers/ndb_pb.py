#!/usr/bin/python
# -*- coding: utf-8 -*-

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
import json
import webapp2

# Definimos la lista de redes sociales con las que trabajamos

rs_list = [
    'twitter',
    'facebook',
    'stackoverflow',
    'instagram',
    'linkedin',
    'google',
    'github',
    ]


# class Tag(ndb.Model):
#   name_tag = ndb.StringProperty()
#   date_tag = ndb.StringProperty()
#   author = ndb.StringProperty()
#   zipball_url = ndb.StringProperty()
#   tarball_url = ndb.StringProperty()

# class Release(ndb.Model):
#   tag_name = ndb.StringProperty()
#   html_url = ndb.StringProperty()
#   name_release = ndb.StringProperty()
#   description = ndb.TextProperty()
#   publish_date = ndb.StringProperty()
#   zipball_url = ndb.StringProperty()
#   tarball_url = ndb.StringProperty()

# class Autor(ndb.Model):
#   login = ndb.StringProperty()
#   user_id = ndb.IntegerProperty()
#   html_url = ndb.StringProperty()
#   followers = ndb.IntegerProperty()
#   following = ndb.IntegerProperty()

# class Componente(ndb.Model):
#   full_name = ndb.StringProperty() # Format: ":author/:repo"
#   repo_id = ndb.IntegerProperty() # Id of the repo in Github
#   name_repo = ndb.StringProperty()
#   # ComponentID for the repo. It's the id for the repo managed by polymer_bricks
#   full_name_id = ndb.StringProperty() # Format: ":author_:repo"
#   autor = ndb.StructuredProperty(Autor)
#   html_url = ndb.StringProperty()
#   description = ndb.StringProperty()
#   stars = ndb.IntegerProperty()
#   forks = ndb.IntegerProperty()
#   languages = ndb.StringProperty(repeated=True)
#   #tags = ndb.StructuredProperty(Tag, repeated=True)
#   #releases = ndb.StructuredProperty(Release, repeated=True)
#   # Reputation related fields
#   reputation = ndb.FloatProperty()
#   ratingsCount = ndb.IntegerProperty()
#   reputation_sum = ndb.FloatProperty()
#   # SHA-256 string that identifies the repo
#   #repo_hash = ndb.StringProperty()
#   # Lowercased names in order to obtain a properly ordering in ndb queries
#   #name_repo_lower_case = ndb.StringProperty()
#   #full_name_repo_lower_case = ndb.StringProperty()

  # Returns the rounded value corresponding to the reputation of the repo
  # def roundReputation(self):
  #   repValue = float(self.reputation)
  #   roundRep = round(repValue, 2)
  #   decRep = roundRep - int(roundRep)
  #   if decRep < 0.26:
  #     roundRep = roundRep - decRep
  #   elif decRep >= 0.26 and decRep<= 0.76:
  #     roundRep = int(roundRep) + 0.5
  #   else:
  #     roundRep = float(int(roundRep) + 1)
  #   return roundRep

  # """Methods to generate RPC Messages returned by Polymer Bricks API"""
  # # type: basic/detailed
  # def toRPCMessage(self, type):
  #   if type=="basic":
  #     # We set the user rating to 0, then we will set the proper value (in getUserRating)
  #     return ComponentBasicInfo(name=self.name_repo, author=self.owner.login
  #               ,description=self.description, nStars=self.stars,
  #               starRate=self.roundReputation(), nForks=self.forks, userRating = 0.0,
  #               componentId=self.full_name_id)
  #   elif type=="detailed":
  #     # We set the user rating to 0, then we will set the proper value (in getUserRating)
  #     return ComponentDetails(name=self.name_repo, author=self.owner.login
  #               ,description=self.description, nStars=self.stars,
  #               starRate=self.roundReputation(), nForks=self.forks, userRating = 0.0,
  #               componentId=self.full_name_id)

class UsuarioBeta(ndb.Model):

    email = ndb.StringProperty(required=True)
    nombre = ndb.StringProperty()
    apellidos = ndb.StringProperty()


class Component(ndb.Model):
  component_id = ndb.StringProperty()
  url = ndb.StringProperty()
  input_type = ndb.StringProperty()
  output_type = ndb.StringProperty()
  rs = ndb.StringProperty()
  description = ndb.StringProperty()

class ComponenteUsuario(ndb.Model):
  id_componente = ndb.StringProperty(required=True)
  x = ndb.FloatProperty()
  y = ndb.FloatProperty()
  height = ndb.StringProperty()
  width = ndb.StringProperty()
  listening = ndb.StringProperty()


class UserRating(ndb.Model):
  component_id = ndb.StringProperty()
  rating_value = ndb.FloatProperty()


# Entidad Grupo

class Grupo(ndb.Model):

  nombre_grupo = ndb.StringProperty(required=True)
  lista_Usuarios = ndb.StringProperty()
  descripcion = ndb.StringProperty()


# Entidad Token

class Token(ndb.Model):

  identificador = ndb.StringProperty()
  token = ndb.StringProperty()
  nombre_rs = ndb.StringProperty()


# Entidad UsuarioSocial

class UsuarioSocial(ndb.Model):

  nombre_rs = ndb.StringProperty(required=True)
  siguiendo = ndb.IntegerProperty()
  seguidores = ndb.IntegerProperty()
  url_sig = ndb.StringProperty()
  url_seg = ndb.StringProperty()

# Entidad usuario

class Usuario(ndb.Model):
  id_usuario = ndb.StringProperty()
  email = ndb.StringProperty()
  private_email = ndb.BooleanProperty()
  telefono = ndb.IntegerProperty()
  private_phone = ndb.BooleanProperty()
  descripcion = ndb.TextProperty()
  sitio_web = ndb.StringProperty()
  imagen = ndb.StringProperty()
  tokens = ndb.StructuredProperty(Token, repeated=True)
  lista_Redes = ndb.StructuredProperty(UsuarioSocial, repeated=True)
  lista_Grupos = ndb.StructuredProperty(Grupo, repeated=True)
  rates = ndb.StructuredProperty(UserRating, repeated=True)
  componentes = ndb.StructuredProperty(ComponenteUsuario, repeated=True)


  # tarjeta = ndb.StructuredProperty(Tarjeta)

#####################################################################################
# Definicion de metodos para insertar, obtener o actualizar datos de la base de datos
#####################################################################################

def getToken(entity_key, rs):  # FUNCIONA
    user = entity_key.get()
    tokens = user.tokens
    res = None
    if not rs in rs_list:
      return 'La red social no esta contemplada'
    for token in tokens:
      print "DEBUG: TOKEN ACTUAL ", token.nombre_rs 
      if token.nombre_rs == rs:
        res = token

    return res

def getUser(entity_key): #FUNCIONA
  user = entity_key.get()
  rates = user.rates; redes = user.lista_Redes
  rates_list = []; nombres_redes = []
  for rate in rates:
    comp = rate.component_id
    value = rate.rating_value
    tup = (comp, value)
    rates_list.append(tup)
  for red in redes:
    nombres_redes.append(red.nombre_rs)
  usuario = {"id_usuario": user.id_usuario,
              "descripcion": user.descripcion,
              "imagen": user.imagen,
              "sitio_web": user.sitio_web,
              "private_email"_ user.private_email,
              "email": user.email,
              "private_phone": user.private_phone,
              "telefono": user.telefono,
              "redes": nombres_redes,
              "components": rates_list}
  usuario = json.dumps(usuario)
  return usuario

@ndb.transactional(xg=True)

def insertaUsuario(rs, ide, token, datos=None): #FUNCIONA
  usuario = Usuario()
  token = Token(identificador=ide, token=token, nombre_rs=rs)
  token.put()
  usuario.tokens.append(token)
  if not datos == None:
    if datos.has_key("email"):
      usuario.email = datos["email"]
    if datos.has_key("private_email"):
      usuario.private_email = datos["private_email"]
    if datos.has_key("telefono"):
      usuario.telefono = datos["telefono"]
    if datos.has_key("private_phone"):
      usuario.private_phone = datos["private_phone"]
    if datos.has_key("descripcion"):
      usuario.descripcion = datos["descripcion"]
    if datos.has_key("imagen"):
      usuario.imagen = datos["imagen"]

  user_key = usuario.put()

  return user_key


def actualizaUsuario(entity_key, datos): #FUNCIONA
  usuario = entity_key.get()
  if datos.has_key("email"):
    usuario.email = datos["email"]
  if datos.has_key("private_email"):
    usuario.private_email = datos["private_email"]
  if datos.has_key("telefono"):
    usuario.telefono = datos["telefono"]
  if datos.has_key("private_phone"):
    usuario.private_phone = datos["private_phone"]
  if datos.has_key("descripcion"):
    usuario.descripcion = datos["descripcion"]
  if datos.has_key("imagen"):
    usuario.imagen = datos["imagen"]
  if datos.has_key("sitio_web"):
    usuario.imagen = datos["sitio_web"]
  if datos.has_key("componente"):
    nom_comp = datos["componente"]
    if datos.has_key("valoracion"):
      rate = datos["valoracion"]
      rating = UserRating(component_id=nom_comp, rating_value=rate)
      usuario.rates.append(rating)

  usuario.put()

def insertaToken(entity_key, rs, token, id_usuario): #FUNCIONA
  user = entity_key.get()
  tok_aux = Token(identificador=id_usuario, token=token, nombre_rs=rs)
  user.tokens.append(tok_aux)
  user.put()

def insertaGrupo(entity_key, nombre, datos=None): #FUNCIONA
  usuario = entity_key.get()
  grupo = Grupo(nombre_grupo=nombre)
  users = ""
  
  if not datos == None:
    if datos.has_key("descripcion"): grupo.descripcion = datos["descripcion"]
    if datos.has_key("usuarios"):
      for user in datos["usuarios"]:
        users += user + ", "

  grupo.lista_Usuarios = users
  usuario.lista_Grupos.append(grupo)
  usuario.put()

def addUsuarioAGrupo(entity_key, nombre_grupo, usuario): #FUNCIONA
  user = entity_key.get()
  grupos = user.lista_Grupos

  for grupo in grupos:
    if grupo.nombre_grupo == nombre_grupo:
      grupo.lista_Usuarios += usuario

def addDescripcionAGrupo(entity_key, nombre, descripcion): #FUNCIONA
  usuario = entity_key.get()
  grupos = usuario.lista_Grupos

  for grupo in grupos:
    if grupo.nombre_grupo == nombre:
      grupo.descripcion = descripcion

  usuario.put()

def buscaGrupos(entity_key): #FUNCIONA
  user = entity_key.get()
  res = {}
  contador = 1
  if user.lista_Grupos:
    for grupo in user.lista_Grupos:
      res[contador] = grupo.nombre_grupo
      contador += 1

  return json.dumps(res)

def insertaRed(entity_key, nombre, datos=None): # FUNCIONA
  usuario = entity_key.get()
  user_social = UsuarioSocial(nombre_rs=nombre)
  if not datos == None:
    if datos.has_key("siguiendo"):
      user_social.siguiendo = datos["siguiendo"]
    if datos.has_key("seguidores"):
      user_social.seguidores = datos["seguidores"]
    if datos.has_key("url_seg"):
      user_social.url_seg = datos["url_seg"]
    if datos.has_key("url_sig"):
      user_social.url_sig = datos["url_sig"]

  usuario.lista_Redes.append(user_social)
  usuario.put()
    

def buscaRed(entity_key): # FUNCIONA
  usuario = entity_key.get()
  res = {}
  contador = 1
  if usuario.lista_Redes:
    for red in usuario.lista_Redes:
      res[contador] = red.nombre_rs
      contador += 1

  return json.dumps(res)

def insertComponent(name, url, description, rs, input_t, output):
  comp = Component(component_id=name, url=url, input_type=input_t, output_type=output, rs=rs, description=description)
  comp.put()

def insertarUserComponent(entity_key, nombre, coord_x=0, coord_y=0, height="", width="", listening=""): # FUNCIONA
  usuario = entity_key.get()
  componente = ComponenteUsuario(nombre=nombre, x=coord_x, y=coord_y, height=height, width=width, listening=listening)
  usuario.componentes.append(componente)

  usuario.put()

def modificarComponente(entity_key, nombre, datos): #FUNCIONA
  usuario = entity_key.get()
  comps = usuario.componentes
  for comp in comps:
    if comp.nombre == nombre:
      if datos.has_key("x"):
        comp.x = datos["x"]
      if datos.has_key("y"):
        comp.y = datos["y"]
      if datos.has_key("height"):
        comp.height = datos["height"]
      if datos.has_key("width"):
        comp.width = datos["width"]
      
  usuario.put()

def addListening(entity_key, nombre, events):
    usuario = entity_key.get()
    comps = usuario.componentes
    for comp in comps:
        if comp.nombre == nombre:
            for event in events:
                comp.listening += event + ''

    usuario.put()

def getComponente(entity_key, nombre, format="reduced"): # FUNCIONA
  user = entity_key.get()
  comps = user.componentes
  res = {"nombre": nombre,
          "x": 0,
          "y": 0,
          "url": "",
          "height": "",
          "width": ""}
  for comp in comps:
    if comp.nombre == nombre:
      res["x"] = comp.x
      res["y"] = comp.y
      res["url"] = comp.url
      res["height"] = comp.height
      res["width"] = comp.width
      res["entrada"] = comp.input_type
      res["salida"] = comp.output_type
      res["escuchando"] = comp.listening

    usuario.put()
    return usuario.key

def getComponents(rs="", user_id="", all_info=False):
  res = []
  if user_id == "" and not all_info: # The general information of the components must be returned
    components = Component.query()
    comp = {}
    for component in components:
      comp["id_componente"] = component.id_componente
      comp["url"] = component.url
      comp["rs"] = component.rs
      comp["description"] = component.description
      comp["input_type"] = component.input_type
      comp["output_type"] = component.output_type
      comp["listening"] = component.listening
      res.append(json.dumps(comp))
  elif not user_id == "":
    if all_info:
      user = Usuario.query(Usuario.id_usuario == user_id).get()
      # Info for the components used by the specified user
      user_comps = user.componentes
      for comp in user_comps:
        # General info for components
        comp = {}
        info_comp = Component.query(Component.component_id == comp.id_componente).get()
        comp["component_id"] = 

    return res

def buscaToken(id_usuario, rs): #FUNCIONA
  token_aux = Token(identificador=id_usuario, nombre_rs=rs)
  tokens = Token.query()
  token = tokens.filter(Token.identificador==id_usuario).filter(Token.nombre_rs==rs).get() 
  if token:
    return token.token
  else:
    return None

def modificaToken(id_usuario, nuevo_token, rs): #FUNCIONA
  token_aux = Token(identificador=id_usuario, nombre_rs=rs)
  usuario = Usuario.query(Usuario.tokens==token_aux).get()
  tokens = usuario.tokens
  for token in tokens:
    if token.identificador==id_usuario and token.nombre_rs==rs:
      token.token = nuevo_token
      token_aux.token = nuevo_token
      token_aux.put()

def nuevoUsuarioBeta(email, nombre, apellidos):  # FUNCIONA
    user_beta = UsuarioBeta(email=email, nombre=nombre,
                            apellidos=apellidos)
    user_beta.put()


def getEmails():  # FUNCIONA
    users_beta = UsuarioBeta.query().fetch(100)
    lista_emails = []
    for user in users_beta:
        lista_emails.append(user.email)

    return lista_emails

def usuarioSuscrito(email):
  emails = getEmails()
  if email in emails:
    return True
  else:
    return False


def addRate(entity_key, component_id, value):
  user = entity_key.get()
  rate = UserRating(component_id=component_id, rating_value=value)
  user.rates.append(rate)

def deleteUser(entity_key):
  entity_key.delete()

def deleteComponent(component_name): 
  component = Component.query(Component.id_componente==component_name).get()
  component.key.delete()

  # Now, it's necessary to delete this component from all the users
  comp = Component(component_id=component_name)
  users = Usuario.query(Usuario.componentes==component).fetch(100)

  [user.componentes.remove(comp) for user in users]

def deleteCredentials(entity_key, rs, id_rs):
  token_aux = Token(identificador=id_rs, nombre_rs=rs)
  tok = Token.query(token_aux).get()
  tok.key.delete()
  user = entity_key.get()
  user.tokens.remove(token_aux)

def getUsers():
  users = Usuario.query()
  users_list = []
  for user in users:
    groups = user.lista_Grupos; networks = user.lista_Redes
    group_names = []; net_names = []
    [group_names.append(group.nombre_grupo) for group in groups]
    [net_names.append(net.nombre_rs) for net in networks]
    usuario = {"email": user.email,
              "telefono": user.telefono,
              "descripcion": user.descripcion,
              "grupos": nombres_grupos,
              "redes": nombres_redes}
    usuario = json.dumps(usuario)
    users_list.append(usuario)

def searchUserById(user_id):
  user = Usuario.query(id_usuario=user_id).get()
  if user:
    return True
  else:
    return False

# class MainPage(webapp2.RequestHandler):
#   def get(self):
#     self.response.headers['Content-Type'] = 'text/plain'
#     #PARTE 1: INSERCION DE 1 USUARIO, INSERCION 1 TOKEN, MOSTRAR TOKENS
#     datos = {"email":"lruiz@conwet.com", 
#               "telefono": 61472589, 
#               "descripcion":"Este es mi perfil personal", 
#               "imagen": "www.example.com/mi-foto.jpg"}
#     key = insertaUsuario("twitter", "lrr9204", "asdfghjklm159753", datos)

#     tok = getToken(key, "twitter")
#     self.response.write(tok.nombre_rs + "--> identificador: " + tok.identificador + "; token: " + tok.token)
#     self.response.write("\n")

#     insertaToken(key, "facebook", "poiuytrewq12345", "Luis Ruiz")

#     tok_f = getToken(key, "facebook")
#     self.response.write(tok_f.nombre_rs + "--> identificador: " + tok_f.identificador + "; token: " + tok_f.token)
#     self.response.write("\n")

#     #PARTE 2: INSERTAR GRUPO, RED Y COMPONENTE, MOSTRAR TODOS
#     datos_grupo = {"descripcion": "Grupo de prueba para usuario 1",
#                     "usuarios": ["luis", "ana", "miguel", "enrique"]}

#     insertaGrupo(key, "DEUS", datos_grupo)

#     grupo = buscaGrupos(key)
#     grupo = json.loads(grupo)
#     keys = grupo.keys()
#     for key_group in keys:
#       self.response.write("Grupo " + key_group + ": " + grupo[key_group] + "\n")

#     datos_red = {"siguiendo": 134,
#                   "seguidores": 50,
#                   "url_seg": "api.twitter.com/get_followers",
#                   "url_sig": "api.twitter.com/get_following"}

#     insertaRed(key, "twitter", datos_red)

#     red = buscaRed(key)
#     red = json.loads(red)
#     red_keys = red.keys()
#     for key_network in keys:
#       self.response.write("Redes " + key_network + ": " + red[key_network] + "\n")

#     insertarComponente(key, "login_twitter", coord_x=12, coord_y=15, url="https://github.com/deus/login_twitter", height="120px", width="50px", entrada="entero", salida="string")

#     comp = getComponente(key, "login_twitter")
#     comp = json.loads(comp)
#     keys = comp.keys()
#     self.response.write("Componente " + comp["nombre"] + ":\n")
#     for key_comp in keys:
#       if not key_comp == "nombre":
#         self.response.write("\t" + key_comp + ": " + str(comp[key_comp]) + "\n")

#     #PARTE 3: MODIFICACION DE ENTIDADES
#     new_key = modificaToken("lrr9204", "mnbvcxzmnbvcxz1234", "twitter")
#     tok = getToken(key, "twitter")
#     self.response.write(tok.nombre_rs + "--> identificador: " + tok.identificador + "; token: " + tok.token)
#     self.response.write("\n")

#     token_param = buscaToken("lrr9204", "twitter")
#     self.response.write(token_param)
#     self.response.write("\n")

#     info_user = buscaUsuario(key)
#     info_user = json.loads(info_user)
#     keys = info_user.keys()
#     for key_user in keys:
#       self.response.write("Datos usuario --> " + str(key_user) + ": " + str(info_user[key_user]) + "\n")

#     addUsuarioAGrupo(key, "DEUS", "pepe")
#     addDescripcionAGrupo(key, "DEUS", "Grupo UPM")
#     grupo = buscaGrupos(key)
#     grupo = json.loads(grupo)
#     keys = grupo.keys()
#     for key_group in keys:
#       self.response.write("Grupo " + key_group + ": " + grupo[key_group] + "\n")

#     datos_act = {"x": 19}
#     modificarComponente(key, "login_twitter", datos_act)
#     comp = getComponente(key, "login_twitter")
#     comp = json.loads(comp)
#     keys = comp.keys()
#     self.response.write("Componente " + comp["nombre"] + ":\n")
#     for key_comp in keys:
#       if not key_comp == "nombre":
#         self.response.write("\t" + key_comp + ": " + str(comp[key_comp]) + "\n")

#     nuevos_datos_us = {"email": "l.ruizr04@gmail.com",
#                         "telefono": 614526893}
#     actualizaUsuario(key, nuevos_datos_us)
#     info_user = buscaUsuario(key)
#     info_user = json.loads(info_user)
#     keys = info_user.keys()
#     for key_user in keys:
#       self.response.write("Datos usuario --> " + str(key_user) + ": " + str(info_user[key_user]) + "\n")

#     nuevoUsuarioBeta("luis@ruiz", "Luis", "Ruiz Ruiz")
#     nuevoUsuarioBeta("ana@lopera", "Ana", "Lopera Martinez")
#     nuevoUsuarioBeta("juanfran@salamanca", "Juanfran", "Salamanca Carmona")
#     nuevoUsuarioBeta("miguel@ortega", "Miguel", "Ortega Moreno")

#     emails = getEmails()
#     for email in emails:
#       self.response.write("\t email: " + email + "\n")

#     self.response.write(str(usuarioSuscrito("enrique@madridejos")) + "\n")

# app = webapp2.WSGIApplication([
#       ('/', MainPage),
# ], debug=True)