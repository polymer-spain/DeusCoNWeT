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
from Crypto.Cipher import AES
import base64
import os

# Definimos la lista de redes sociales con las que trabajamos

social_list = [
    'twitter',
    'facebook',
    'stackoverflow',
    'instagram',
    'linkedin',
    'google',
    'github',
    ]

# TODO: almacenar secret!!
# Definicion de metodos y variables para el cifrado de claves

# Tamaño de bloque
BLOCK_SIZE = 32

# caracter para realizar un padding del mensaje a cifrar 
# (para que sea multiplo del tamaño del bloque)
PADDING = '{'
#Funcion de padding del mensaje a cifrar
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# Funciones de encode y decode utilizando AES, con codec base64
encodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
decodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# genera una secret key aleatoria
secret = os.urandom(BLOCK_SIZE)
# Crea un objeto cipher
cipher = AES.new(secret)

#####################################################################################
# Definicion de entidades de la base de datos
#####################################################################################

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

class BetaUser(ndb.Model):
  email = ndb.StringProperty(required=True)
  name = ndb.StringProperty()
  surname = ndb.StringProperty()

class Component(ndb.Model):
  component_id = ndb.StringProperty()
  url = ndb.StringProperty()
  input_type = ndb.StringProperty()
  output_type = ndb.StringProperty()
  rs = ndb.StringProperty()
  description = ndb.StringProperty()

class UserComponent(ndb.Model):
  component_id = ndb.StringProperty(required=True)
  x = ndb.FloatProperty()
  y = ndb.FloatProperty()
  height = ndb.StringProperty()
  width = ndb.StringProperty()
  listening = ndb.StringProperty()


class UserRating(ndb.Model):
  component_id = ndb.StringProperty()
  rating_value = ndb.FloatProperty()

class Group(ndb.Model):
  group_name = ndb.StringProperty(required=True)
  user_list = ndb.StringProperty()
  description = ndb.StringProperty()

class Token(ndb.Model):
  identifier = ndb.StringProperty()
  token = ndb.StringProperty()
  social_name = ndb.StringProperty()

class SocialUser(ndb.Model):
  social_name = ndb.StringProperty(required=True)
  following = ndb.IntegerProperty()
  followers = ndb.IntegerProperty()
  following_url = ndb.StringProperty()
  followers_url = ndb.StringProperty()

class User(ndb.Model):
  user_id = ndb.StringProperty()
  email = ndb.StringProperty()
  private_email = ndb.BooleanProperty(default=False)
  phone = ndb.IntegerProperty()
  private_phone = ndb.BooleanProperty(default=False)
  description = ndb.TextProperty()
  website = ndb.StringProperty()
  image = ndb.StringProperty()
  tokens = ndb.StructuredProperty(Token, repeated=True)
  net_list = ndb.StructuredProperty(SocialUser, repeated=True)
  group_list = ndb.StructuredProperty(Group, repeated=True)
  rates = ndb.StructuredProperty(UserRating, repeated=True)
  components = ndb.StructuredProperty(UserComponent, repeated=True)

class GitHubAPIKey(ndb.Model):
  token = ndb.StringProperty()

#####################################################################################
# Definicion de metodos para insertar, obtener o actualizar datos de la base de datos
#####################################################################################

def getToken(id_rs, social_net):  # FUNCIONA
  ans = None
  token = Token.query(Token.identifier == id_rs).filter(Token.social_name == social_net).get()
  user = User.query(User.tokens == token).get()
  if not user == None:
    ans = {"token": decodeAES(token.token),
          "user_id": user.user_id}
  return ans

def getUser(user_id): #FUNCIONA
  user = User.query(User.user_id == user_id).get()
  user_info = None
  if not user == None:
    rates = user.rates; nets = user.net_list
    rates_list = []; net_names = []
    for rate in rates:
      comp = rate.component_id
      value = rate.rating_value
      tup = (comp, value)
      rates_list.append(tup)
    for net in nets:
      net_names.append(net.social_name)
    user_info = {"user_id": user.user_id,
                "description": user.description,
                "image": user.image,
                "website": user.website,
                "private_email": user.private_email,
                "private_phone": user.private_phone,
                "email": user.email,
                "phone": user.phone,
                "nets": net_names,
                "components": rates_list}
  return user_info

def getUserId(entity_key):
  user = entity_key.get()
  user_id = None
  if not user == None:
    user_id = user.user_id
  return user_id

@ndb.transactional(xg=True)
def insertUser(rs, ide, access_token, data=None): #FUNCIONA
  user = User()
  # Encodes access token tha will be stored in the database
  access_token = encodeAES(access_token)
  
  token = Token(identifier=ide, token=access_token, social_name=rs)
  token.put()
  user.tokens.append(token)
  if not data == None:
    if data.has_key("user_id"):
      user.user_id = data["user_id"]
    if data.has_key("email"):
      user.email = data["email"]
    if data.has_key("private_email"):
      user.private_email = data["private_email"]
    if data.has_key("phone"):
      user.phone = datos["phone"]
    if data.has_key("private_phone"):
      user.private_phone = data["private_phone"]
    if data.has_key("description"):
      user.description = data["description"]
    if data.has_key("image"):
      user.image = data["image"]
    if data.has_key("website"):
      user.website = data["website"]

  user_key = user.put()

  return user_key


def updateUser(entity_key, data): #FUNCIONA
  user = entity_key.get()
  if data.has_key("email"):
    user.email = data["email"]
  if data.has_key("private_email"):
    user.private_email = data["private_email"]
  if data.has_key("phone"):
    user.phone = data["phone"]
  if data.has_key("private_phone"):
    user.private_phone = data["private_phone"]
  if data.has_key("description"):
    user.description = data["description"]
  if data.has_key("image"):
    user.image = data["image"]
  if data.has_key("website"):
    user.image = data["website"]
  if data.has_key("componente"):
    comp_name = data["component"]
    # We add the component to the component_list of the user
    component = UserComponent(component_id=comp_name, x=0, y=0, height=0, width=0, listening=None)
    user.components.append(component)
    # We add a Rating entity that represents the component rating
    if data.has_key("rate"):
      rate = data["rate"]
    else:
      rate = 0  
    rating = UserRating(component_id=comp_name, rating_value=rate)
    user.rates.append(rating)
  # Updates the data
  user.put()

def insertToken(entity_key, social_name, access_token, user_id): #FUNCIONA
  user = entity_key.get()
  # Encodes access token tha will be stored in the database
  access_token = encodeAES(access_token)
  # We create a Token Entity in the datastore
  tok_aux = Token(identifier=user_id, token=access_token, social_name=social_name)
  tok_aux.put()
  # We add the Token Entity to the user credentials list
  user.tokens.append(tok_aux)
  user.put()

def insertGroup(entity_key, name, data=None): #FUNCIONA
  user = entity_key.get()
  group = Group(group_name=name)
  users = ""
  
  if not data == None:
    if data.has_key("description"): group.description = data["description"]
    if data.has_key("usuarios"):
      for user in datos["usuarios"]:
        users = users + user + ", "

  group.user_list = users
  user.group_list.append(group)
  user.put()

def addUserToGroup(entity_key, group_name, username): #FUNCIONA
  user = entity_key.get()
  groups = user.group_list

  for group in groups:
    if group.group_name == group_name:
      group.user_list += username

def addDescriptionToGroup(entity_key, group_name, description): #FUNCIONA
  user = entity_key.get()
  groups = user.group_list

  for group in groups:
    if group.group_name == group_name:
      group.description = description

  user.put()

def searchGroups(entity_key): #FUNCIONA
  user = entity_key.get()
  ans = {}
  counter = 1
  if user.group_list:
    for group in user.group_list:
      ans[counter] = group.group_name
      counter += 1

  return json.dumps(ans)

def insertNetwork(entity_key, name, data=None): # FUNCIONA
  user = entity_key.get()
  user_social = SocialUser(social_name=name)
  if not datos == None:
    if data.has_key("following"):
      user_social.following = data["following"]
    if data.has_key("followers"):
      user_social.followers = data["followers"]
    if data.has_key("followers_url"):
      user_social.followers_url = data["followers_url"]
    if data.has_key("following_url"):
      user_social.following_url = data["url_sig"]

  user.net_list.append(user_social)
  user.put()
    

def searchNetwork(entity_key): # FUNCIONA
  user = entity_key.get()
  ans = {}
  counter = 1
  if user.net_list:
    for net in user.net_list:
      ans[counter] = net.social_name
      counter += 1

  return json.dumps(ans)

def insertComponent(name, url="", description="", rs="", input_t="", output=""):
  component = Component.query(Component.component_id == name).get()
  res = False
  if component == None:
    component = Component(component_id=name, url=url, input_type=input_t, output_type=output, rs=rs, description=description)
    res = True
  else:
    if not url == "":
      component.url = url
    if not description == "":
      component.description = description
    if not rs == "":
      component.rs = rs
    if not input_t == "":
      component.input_type = input_t
    if not output == "":
      component.output_type = output
  component.put()

  return res

def insertUserComponent(entity_key, name, x=0, y=0, height="", width="", listening=""): # FUNCIONA
  user = entity_key.get()
  component = UserComponent(name=name, x=x, y=y, height=height, width=width, listening=listening)
  user.components.append(component)

  user.put()

def modifyComponent(entity_key, name, data): #FUNCIONA
  user = entity_key.get()
  comps = user.components
  for comp in comps:
    if comp.name == name:
      if data.has_key("x"):
        comp.x = data["x"]
      if data.has_key("y"):
        comp.y = data["y"]
      if data.has_key("height"):
        comp.height = data["height"]
      if data.has_key("width"):
        comp.width = data["width"]
      if data.has_key("listening"):
        comp.listening += data["listening"]
      
  user.put()

def addListening(entity_key, name, events):
  user = entity_key.get()
  comps = user.components
  for comp in comps:
    if comp.component_id == name:
      for event in events:
        comp.listening += event + ""

  user.put()
  

def getComponent(entity_key, name, all_info=False): # FUNCIONA
  comp = Component.query(Component.component_id == name).get()
  if comp == None:
    ans = None
  else:
    rate = UserRating.query(UserRating.component_id == name).get()
    user = entity_key.get()
    user_comp = [cte for cte in user.components if cte.component_id == name]
    general_comp = {"component_id": name}
    general_comp["url"] = comp.url
    general_comp["social_network"] = comp.rs
    general_comp["description"] = comp.description
    if not rate == None: 
      general_comp["rate"] = rate.rating_value
    else:
      general_comp["rate"] = 0
    if all_info and not len(user_comp) == 0:
      general_comp["input_type"] = comp.input_type
      general_comp["output_type"] = comp.output_type
      general_comp["x"] = user_comp.x
      general_comp["y"] = user_comp.y
      general_comp["height"] = user_comp.height
      general_comp["width"] = user_comp.width
      general_comp["listening"] = user_comp.listening
    ans = json.dumps(general_comp)
  return ans


def getComponents(entity_key=None, rs="", all_info=False, filter_by_user=False):
  ans = []
  general_comp = {}
  if filter_by_user:
    # user id specified
    if rs == "":
      # without social network
      if all_info:
        # complete information
        user = entity_key.get()
        # Info for the components used by the specified user
        user_comps = user.components
        for comp in user_comps:
          info_comp = Component.query(Component.component_id == comp.component_id).get()
          rate = UserRating.query(UserRating.component_id == comp.component_id).get()
          general_comp["component_id"] = comp.component_id
          general_comp["url"] = info_comp.url
          general_comp["social_network"] = info_comp.rs
          general_comp["description"] = info_comp.description
          general_comp["x"] = comp.x
          general_comp["y"] = comp.y
          general_comp["input_type"] = info_comp.input_type
          general_comp["output_type"] = info_comp.output_type
          general_comp["listening"] = comp.listening
          general_comp["height"] = comp.height
          general_comp["width"] = comp.width
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          # ans = general_comp
          ans.append(json.dumps(general_comp))

      else:
        user = entity_key.get()
        user_comps = user.components
        # Now we get the general info about the components used by the user
        for comp in user_comps:
          info_comp = Component.query(Component.component_id == comp.component_id).get()
          rate = UserRating.query(UserRating.component_id == comp.component_id).get()
          general_comp["component_id"] = info_comp.component_id
          general_comp["url"] = info_comp.url
          general_comp["social_network"] = info_comp.rs
          general_comp["description"] = info_comp.description
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))

    else:
      if all_info:
        user = entity_key.get()
        user_comps = user.components
        for comp in user_comps:
          info_comp = Component.query(Component.component_id == comp.component_id).filter(Component.rs == rs).get()
          rate = UserRating.query(UserRating.component_id == comp.component_id).get()
          general_comp["component_id"] = comp.component_id
          general_comp["url"] = info_comp.url
          general_comp["social_network"] = info_comp.rs
          general_comp["description"] = info_comp.description
          general_comp["x"] = comp.x
          general_comp["y"] = comp.y
          general_comp["input_type"] = info_comp.input_type
          general_comp["output_type"] = info_comp.output_type
          general_comp["listening"] = comp.listening
          general_comp["height"] = comp.height
          general_comp["width"] = comp.width
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))
      else:
        user = entity_key.get()
        user_comps = user.components
        # Now we get the general info about the components used by the user
        for comp in user_comps:
          info_comp = Component.query(Component.component_id == comp.component_id).filter(Component.rs == rs).get()
          rate = UserRating.query(UserRating.component_id == comp.component_id).get()
          general_comp["component_id"] = info_comp.component_id
          general_comp["url"] = info_comp.url
          general_comp["social_network"] = info_comp.rs
          general_comp["description"] = info_comp.description
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))
  else:
    # Not user id. In this case, the info returned will be always reduced
    if not all_info:
      if rs == "":
        components = Component.query().fetch(20)
        for component in components:
          rate = UserRating.query(UserRating.component_id == component.component_id).get()
          general_comp["component_id"] = component.component_id
          general_comp["url"] = component.url
          general_comp["social_network"] = component.rs
          general_comp["description"] = component.description
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))
      else:
        components = Component.query(Component.rs == rs).fetch(20)
        for comp in components:
          rate = UserRating.query(UserRating.component_id == comp.component_id).get()
          general_comp["component_id"] = comp.component_id
          general_comp["url"] = comp.url
          general_comp["social_network"] = comp.rs
          general_comp["description"] = comp.description
          if not rate == None: 
            general_comp["rate"] = rate.rating_value
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))

  return ans

def searchToken(user_id, rs): #FUNCIONA
  tokens = Token.query()
  token = tokens.filter(Token.identifier==user_id).filter(Token.social_name==rs).get() 
  if token:
    return decodeAES(token.token)
  else:
    return None

def modifyToken(user_id, new_token, rs): #FUNCIONA
  # Encodes access token tha will be stored in the database
  new_token = encodeAES(new_token)
  
  tok = Token.query(Token.identifier == user_id).filter(Token.social_name == rs).get()
  # Updates the token
  tok.token = new_token
  tok.put()
  # Updates the token in the user credential list
  token_aux = Token(identifier=user_id, social_name=rs)
  user = User.query(User.tokens==token_aux).get()
  tokens = user.tokens
  for token in tokens:
    if token.identifier==user_id and token.social_name==rs:
      token.token = new_token

  user.put()
  return user.key

def newUserBeta(email, name, surname): #FUNCIONA
  beta_user = UserBeta(email=email, name=name, surname=surname)
  beta_user.put()

def getEmails(): #FUNCIONA
  beta_users = BetaUser.query().fetch(100)
  email_list = []
  for user in beta_users:
    email_list.append(user.email)

  return email_list


def subscribedUser(email):
  emails = getEmails()
  if email in emails:
    return True
  else:
    return False


def addRate(entity_key, component_id, value):
  user = entity_key.get()
  rate = UserRating(component_id=component_id, rating_value=value)
  status = False
  for comp_rate in user.rates:
    if comp_rate.component_id == component_id:
      comp_rate.rating_value = value
      user.put()
      status = True
  return status

def deleteUser(entity_key):
  user = entity_key.get()
  token_list = user.tokens
  # We delete the user tokens
  for token in token_list:
    deleteCredentials(entity_key, token.social_name, token.identifier)
  # We delete the user
  entity_key.delete()

def deleteComponent(component_name):
  status = False
  component = Component.query(Component.component_id==component_name).get()
  if not component == None:
    status = True

    # We delete the component entity from the datastore
    component.key.delete()

    # Now, it's necessary to delete this component from all the users
    comp = UserComponent(component_id=component_name)
    users = User.query(User.components==comp).fetch(100)
    for user in users:
      user.components.remove(comp)
      user.put()

  return status

def deleteCredentials(entity_key, rs, id_rs):
  status = False
  tok = Token.query(Token.identifier == id_rs).filter(Token.social_name == rs).get()
  if not tok == None:
    user = entity_key.get()
    # We delete the token if it is not the only token stored for the user and
    # does not belong to a social network to perform login in our system
    if not rs in ['google', 'facebook', 'twitter'] and not len(user.tokens) == 1:
      token_aux = tok.token
      del_token = Token(identifier = id_rs, token = token_aux, social_name = rs) 
      tok.key.delete()
      # Deletes the token from the user
      if not user == None:
        user.tokens.remove(del_token)
        user.put()
        status = True
  return status

def getUsers():
  users = User.query().fetch(100)
  users_list = []
  for user in users:
    groups = user.group_list; networks = user.net_list
    group_names = []; net_names = []
    [group_names.append(group.group_name) for group in groups]
    [net_names.append(net.social_name) for net in networks]
    usuario = {"user_id": user.user_id,
              "email": user.email,
              "phone": user.phone,
              "description": user.description,
              "groups": group_names,
              "networks": net_names}
    user_info = json.dumps(usuario)
    users_list.append(user_info)
  return users_list

def searchUserById(user_id):
  user = User.query(id_usuario=user_id).get()
  if user:
    return True
  else:
    return False

def getGitHubAPIKey():
  githubKey = GitHubAPIKey.query().get()
  return githubKey.token


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
