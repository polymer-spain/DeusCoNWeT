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
import yaml
import random

# Definimos la lista de redes sociales con las que trabajamos
social_list = [
    'twitter',
    'facebook',
    'stackoverflow',
    'instagram',
    'linkedin',
    'googleplus',
    'github',
    ]


# We read the relevant fields in the config.yaml file (config params for PicBit Backend)
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# If the param is set wrong, we configure component versioning as static
component_versioning = cfg["component_versioning"] if cfg["component_versioning"] in ["static", "dynamic"] else "static"

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
  input_type = ndb.StringProperty(repeated=True)
  output_type = ndb.StringProperty(repeated=True)
  rs = ndb.StringProperty()
  description = ndb.StringProperty()
  # List of versions available for a component
  version_list = ndb.StringProperty(repeated=True)
  # Index to control the version that will be served to the next user that adds it to his dashboard 
  version_index = ndb.IntegerProperty()
  # Determines the times that the general component has been tested
  test_count = ndb.IntegerProperty(default=0)
  # Represents if the component will served in a predetermined way to every new user in the system
  predetermined = ndb.BooleanProperty(default=False)

class UserComponent(ndb.Model):
  component_id = ndb.StringProperty(required=True)
  x = ndb.FloatProperty()
  y = ndb.FloatProperty()
  height = ndb.StringProperty()
  width = ndb.StringProperty()
  listening = ndb.StringProperty()
  # Actual cersion of the component that is being tested
  version = ndb.StringProperty()
  # Represents if the component is placed in the dashboard
  active = ndb.BooleanProperty(default=True)

# Representa que versiones de un componente en particular han sido testeadas por un usuario
class ComponentTested(ndb.Model):
  # User that tested the component
  user_id = ndb.StringProperty(required = True)
  component_id = ndb.StringProperty(required=True)
  # List of versions tested by the user
  versions_tested = ndb.StringProperty(repeated=True)
  # Actual version tested by the user
  actual_version = ndb.StringProperty()

# Entity that represents a version for a given component
# class VersionedComponent(ndb.Model):
#   component_id = ndb.StringProperty(required=True)
#   version = ndb.StringProperty()
#   # Determines the times that the versioned component has been tested
#   test_count = ndb.IntegerProperty(default=0)
#   version_rating = ndb.FloatProperty(default=0) 

class UserRating(ndb.Model):
  component_id = ndb.StringProperty()
  version = ndb.StringProperty() # Version of the component rated
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
  # following = ndb.IntegerProperty()
  # followers = ndb.IntegerProperty()
  # following_url = ndb.StringProperty()
  # followers_url = ndb.StringProperty()

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

# Represents the session value for a given user in the system
class Session(ndb.Model):
  user_key = ndb.KeyProperty()
  hashed_id = ndb.StringProperty()

#####################################################################################
# Definicion de metodos y variables para el cifrado de claves
#####################################################################################

# Tamaño de bloque
BLOCK_SIZE = 32

# caracter para realizar un padding del mensaje a cifrar 
# (para que sea multiplo del tamaño del bloque)
PADDING = '{'
#Funcion de padding del mensaje a cifrar
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

# Funciones de encode y decode utilizando AES, con codec base64
# encodeAES: funcion anonima para cifrar las claves
# Parámetros: c - cipher (objeto AES que contiene la clave de cifrado)
#             s - mensaje a cifrar
encodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

# decodeAES: funcion anonima para cifrar las claves
# Parámetros: c - cipher (objeto AES que contiene la clave de cifrado)
#             e - mensaje a descifrar
decodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

# Funcion para generar el objeto AES necesario para cifrar/descifrar
# Parametros: token_entity_key: (long) clave de la entidad Token a cifrar
def getCipher(token_entity_key):
  # Obtiene la clave, para cifrar/descifrar
  secret = str(token_entity_key).zfill(32)
  # Crea un objeto cipher
  cipher = AES.new(secret)
  return cipher

#####################################################################################
# Definicion de metodos para el control de versionado de componentes
#####################################################################################

# Defines the version of a given component that will be served to a user that adds it
# to his dashboard (transactional operation)
# Params: - general_component: Component Entity that it is desired to be served to the user
# Returns: string that represents the version that will be served to the user
@ndb.transactional()
def setComponentVersion(general_component):
  version = ""
  if component_versioning == "dynamic":
    # We set the version that will be served to the user
    version = general_component.version_list[general_component.version_index]
    # We change the version_index field, that represents the version that will be served to the next user
    general_component.version_index = (general_component.version_index + 1) % len(general_component.version_list)
    # Update the info about the component changed
    general_component.put()

  # If the component versioning is set as static, we always set the stable version for the component
  elif component_versioning == "static":
    version="stable"

  return version

def getComponentEntity(component_id):
  general_component = Component.query(Component.component_id == component_id).get()
  return general_component

#########################################################################################
# Definicion de metodos relacionados con operaciones de alto nivel sobre la base de datos
# Operaciones relacionadas con el dashboard de usuario
#########################################################################################

# Adds to the user dashboard those component defined as predetermined in the system
def assignPredeterminedComponentsToUser(entity_key):
  # Obtains the predetermined components of the system and adds it to the User
  # We consider that we will have at most 10 predetermined components in our system
  predetermined_comps = Component.query(Component.predetermined == True).fetch(10)
  for comp in predetermined_comps:
    activateComponentToUser(comp.component_id, entity_key)


# Adds a given component to the user,
# creating or updating the corresponding entities that store properties about this action
def activateComponentToUser(component_id, entity_key):
  user = entity_key.get()
  general_component = Component.query(Component.component_id == component_id).get()
  user_component = None
  status = False
  # We check if the user has added the corresponding social network to his/her profile
  for social_network in user.net_list:
    if general_component.rs == social_network.social_name:
      #We check if the component provided is in the user component list
      # If not, we create a new UserComponent Entity, setting the component version that will use the user
      for comp in user.components:
        if comp.component_id == component_id:
          user_component = comp

      if not user_component == None:
        # We set the field to active
        # The user's preferences (heigh, width) does not change
        # We get the version of the component that will be served to the user
        # (the same version than the setted when the user activated the component for the first time)
        version = user_component.version
        if not user_component.active:
          user_component.active = True
          user.put()
          status = True
      else:
        # We set the version of the component
        general_component = getComponentEntity(component_id)
        version = setComponentVersion(general_component)
        # We create a new UserComponent entity
        user_component = UserComponent(component_id=component_id, x=0, y=0, height="0", width="0", listening=None, version=version)
        # We add the component to the component_list of the user
        user.components.append(user_component)
        user.put()

        # We increase the counters that represents the times that a given component has been tested (general and versioned)
        general_component.test_count = general_component.test_count + 1
        general_component.put()
        # versioned_component = VersionedComponent.query(ndb.AND(VersionedComponent.component_id == component_id,
        # versionedComponent.version == version)).get()
        # versioned_component.test_count = versioned_component.test_count + 1
        # versioned_component.put()
        status = True

      # We store in a ComponentTested entity the new version tested by the user
      user_component_tested = ComponentTested.query(ndb.AND(ComponentTested.component_id == component_id, ComponentTested.user_id == user.user_id)).get()
      if not user_component_tested == None:
        # We update the field that represents the actual version that is being tested
        user_component_tested.actual_version = version
        # We add the version to the versions tested list, if is not was added previously
        if not version in user_component_tested.versions_tested:
          user_component_tested.versions_tested.append(version)
          user_component_tested.put()
      else:
        # We create a new ComponentTested entity to store the versions of a component tested by the user
        component_tested = ComponentTested(component_id=component_id, user_id=user.user_id, versions_tested=[version], actual_version=version)
        component_tested.put()
  return status


# Removes the component from the user's dashboard
# It turns the field active to False, thus the component will not be listed as a
# component included in the user's dashboard
def deactivateUserComponent(entity_key, component_id):
  user = entity_key.get()
  status = False
  # We check if the component provided is in the user component list
  for comp in user.components:
    if comp.component_id == component_id and comp.active:
      # Deactivates the component
      comp.active = False
      user.put()
      status = True

  return status


#####################################################################################
# Definicion de metodos para insertar, obtener o actualizar datos de la base de datos
#####################################################################################

## Metodos asociados a la entidad Token
def getToken(id_rs, social_net):  # FUNCIONA
  ans = None
  token = Token.query(Token.identifier == id_rs).filter(Token.social_name == social_net).get()
  user = User.query(User.tokens == token).get()
  if not user == None:
    cipher = getCipher(token.key.id())
    ans = {"token": decodeAES(cipher, token.token),
          "user_id": user.user_id}
  return ans

def searchToken(token_id, rs): #FUNCIONA
  tokens = Token.query()
  token = tokens.filter(Token.identifier==token_id).filter(Token.social_name==rs).get() 
  if token:
    cipher = getCipher(token.key.id())
    return decodeAES(cipher, token.token)
  else:
    return None

def modifyToken(user_id, new_token, rs): #FUNCIONA
  tok = Token.query(Token.identifier == user_id).filter(Token.social_name == rs).get()
  
  # Ciphers the token
  cipher = getCipher(tok.key.id())
  new_token = encodeAES(cipher, new_token)
  
  # Updates the token
  tok.token = new_token
  token_key = tok.put()

  # Updates the token in the user credential list
  token_aux = Token(identifier=user_id, social_name=rs)
  user = User.query(User.tokens==token_aux).get()
  tokens = user.tokens
  for token in tokens:
    if token.identifier==user_id and token.social_name==rs:
      token.token = new_token

  user.put()
  return user.key

## Metodos asociados a la entidad Usuario
def getUser(user_id, component_detailed_info = False): #FUNCIONA
  user = User.query(User.user_id == user_id).get()
  user_info = None
  
  if not user == None:
    rates = user.rates; nets = user.net_list
    user_component_list = [];  net_names = []
    # Componemos la lista de redes a la que está suscrito un usuario
    for net in nets:
      net_names.append(net.social_name)
    
    # Componemos la lista de componentes de usuario, detallada o reducida
    user_component_list = getUserComponentList(user_id, component_detailed_info)

    # Componemos el diccionario con la info relativa al usuario
    user_info = {"user_id": user.user_id,
                "description": user.description,
                "image": user.image,
                "website": user.website,
                "private_email": user.private_email,
                "private_phone": user.private_phone,
                "email": user.email,
                "phone": user.phone,
                "nets": net_names,
                "components": user_component_list}

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
  # We add to the user's net list the social network used to sign up to the system
  user_net = SocialUser(social_name=rs)
  user.net_list.append(user_net)

  # We store the user info passed in the data argument
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

  # Inserts the user entity
  user_key = user.put()
  
  token = Token(identifier=ide, token="", social_name=rs)
  token_key = token.put()
  # Ciphers the access token and stores in the datastore
  cipher = getCipher(token_key.id())
  token.token = encodeAES(cipher, access_token)
  token.put()
  user.tokens.append(token)

  # Updates the user entity
  user.put()

  return user_key


# Actualiza la info de usuario proporcionada y retorna una lista de los elementos actualizados
def updateUser(entity_key, data): #FUNCIONA
  user = entity_key.get()
  updated_data = []
  if data.has_key("email"):
    user.email = data["email"]
    updated_data += ["email"]

  if data.has_key("private_email"):
    user.private_email = data["private_email"]
    updated_data += ["private_email"]

  if data.has_key("phone"):
    user.phone = data["phone"]
    updated_data += ["phone"]

  if data.has_key("private_phone"):
    user.private_phone = data["private_phone"]
    updated_data += ["private_phone"]

  if data.has_key("description"):
    user.description = data["description"]
    updated_data += ["description"]
  
  if data.has_key("image"):
    user.image = data["image"]
    updated_data += ["image"]

  if data.has_key("website"):
    user.image = data["website"]
    updated_data += ["website"]

  if data.has_key("component"):
    comp_name = data["component"]
    # Adds the component to the user
    activated = activateComponentToUser(comp_name, entity_key)
    if activated:
      updated_data += ["component"]

  if data.has_key("rate"):
    rate = data["rate"]
    # We add a Rating entity that represents the component rating
    rating = UserRating(component_id=comp_name, rating_value=rate)
    user.rates.append(rating)
    updated_data += ["rate"]    

  # Updates the user data
  user.put()
  # Returns the list that represents the data that was updated
  return updated_data


def insertToken(entity_key, social_name, access_token, user_id): #FUNCIONA
  user = entity_key.get()  
  # We create a Token Entity in the datastore
  tok_aux = Token(identifier=user_id, token="", social_name=social_name)
  token_key = tok_aux.put()
  # Ciphers access token that will be stored in the datastore
  cipher = getCipher(token_key.id())
  access_token = encodeAES(cipher, access_token)
  tok_aux.token = access_token
  tok_aux.put()
  # We add the Token Entity to the user credentials list
  user.tokens.append(tok_aux)
  # We add the social network to the user's nets list
  if not social_name in user.net_list:
    social_network = SocialUser(social_name=social_name)
    user.net_list.append(social_network)
  # Updates the user
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

# Creates a component (Component Entity)
def insertComponent(name, url="", description="", rs="", input_t=None, output=None, version_list=None, predetermined=False):
  # Generates a random initial value that represents the version of the component that will be 
  # served to the next user who adds it to his dashboard
  initial_index = random.randint(0, len(version_list)-1)
  component = Component(component_id=name, url=url, input_type=input_t, output_type=output,
   rs=rs, description=description, version_list=version_list, version_index=initial_index, predetermined=predetermined)
  # We create a new VersionedComponent Entity for each version_added to the version_list
  # for version in version_list:
  #   versionedComponent = VersionedComponent(version=version, component_id=component.component_id)
  #   versionedComponent.put()
  created = True
  # Saves the changes to the entity
  component.put()


# Modifies the related info about a General component in the system (ComponentEntity)
def updateComponent(component_id, url="", description="", rs="", input_t=None, output_t=None, version_list=None):
  component = Component.query(Component.component_id == component_id).get()
  if not component == None:
    if not url == "":
      component.url = url
    if not description == "":
      component.description = description
    if not rs == "":
      component.rs = rs
    if not input_t == None:
      component.input_type = component.input_type + input_t
    if not output_t == None:
      component.output_type = component.output_type + output_t
    if not version_list == None:
      component.version_list = component.version_list + version_list
      # We create a new VersionedComponent Entity for each version_added to the version_list
      for version in version_list:
        versionedComponent = VersionedComponent(version=version, component_id=component.component_id)
        versionedComponent.put()

    # Saves the changes to the entity
    component.put()


def insertUserComponent(entity_key, name, x=0, y=0, height="", width="", listening=""): # FUNCIONA
  user = entity_key.get()
  component = UserComponent(name=name, x=x, y=y, height=height, width=width, listening=listening)
  user.components.append(component)

  user.put()


# Modifies the user's preferences stored related to a component
def modifyUserComponent(entity_key, name, data): #FUNCIONA
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
  

def searchComponent(component_id):
  return Component.query(Component.component_id == component_id).get()
  
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
      general_comp["version"] = user_comp.version
    ans = json.dumps(general_comp)
  return ans

# Retorna los detalles sobre un componente del usuario en particular
def getUserComponent(entity_key, component_id):
  result = None
  user = entity_key.get()
  user_comps = user.components
  for comp in user_comps:
    if comp.component_id == component_id:
      result = comp
  return result

# Retorna una lista de Componentes pertenecientes al dashboard de usuario, incluyendo la valoración del usuario
def getUserComponentList(user_id, component_detailed_info=False):
  # Obtenemos la valoración del componente en particular
  component_list = []
  user = User.query(User.user_id == user_id).get()
  user_comps = user.components
  for comp in user_comps:
    # Returns only the components active in the user's dashboard
    if comp.active:
      # Obtains the user's rating relative to the component
      rating = UserRating.query(UserRating.component_id == comp.component_id).get()
      component_rate = rating if not rating == None else 0.0
      if component_detailed_info:
        component_info = {"component_id": comp.component_id, 
                        "x": comp.x,
                        "y": comp.y,
                        "height": comp.height,
                        "width": comp.width,
                        "listening": comp.listening,
                        "user_rate": component_rate,
                        "version": comp.version}
      else:
          component_info = {"component_id": comp.component_id, 
                        "user_rate": component_rate}
      # Adds the component to the component list
      component_list.append(component_info)
  return component_list

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
          # Returns the info about the active components in the user dashboard
          if comp.active:
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
            general_comp["version"] = comp.version
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
          if comp.active:
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
          if comp.active:
            info_comp = Component.query(Component.component_id == comp.component_id).filter(Component.rs == rs).get()
            rate = UserRating.query(UserRating.component_id == comp.component_id).get()
            if not info_comp == None:
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
              general_comp["version"] = comp.version
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
          if comp.active:
            info_comp = Component.query(Component.component_id == comp.component_id).filter(Component.rs == rs).get()
            rate = UserRating.query(UserRating.component_id == comp.component_id).get()
            if not info_comp == None:
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
    users = User.query(User.components.component_id==component_name).fetch(100)
    for user in users:
      for comp in user.components:
        # We delete the component from the user's component list
        if comp.component_id == component_name:
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
    if not rs in ['googleplus', 'facebook', 'twitter'] and not len(user.tokens) == 1:
      token_aux = tok.token
      del_token = Token(identifier = id_rs, token = token_aux, social_name = rs) 
      tok.key.delete()
      if not user == None:
        # Deletes the token from the user
        user.tokens.remove(del_token)
        # Deletes the social network from the user's net_list
        social_user = SocialUser(social_name=rs)
        user.net_list.remove(social_user)
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
              "description": user.description,
              "groups": group_names,
              "networks": net_names}
    # Returns the user's phone an email if they haven't a private scope 
    if not user.private_phone:
      usuario["phone"] = user.phone
    if not user.private_email:
      usuario["email"] = user.email
    # user_info = json.dumps(usuario)
    users_list.append(usuario)
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

# METHODS FOR SESSION SUPPORT
# Creates a sesion for the given user in the system
# If the user has an active session in the system, we delete the previous session
# and we create a new one (we only support single login per user)
def createSession(user_key, hashed_id):
  stored_session = Session.query(Session.user_key == user_key).get()
  if not stored_session == None:
    stored_session.key.delete()
  # We create a new session assigned to the user
  session = Session(user_key=user_key, hashed_id=hashed_id)
  session.put()

def getSessionOwner(hashed_id):
  user_key = None
  session = Session.query(Session.hashed_id == hashed_id).get()
  if not session == None:
    user_key = session.user_key
  return user_key

def deleteSession(hashed_id):
  deleted = False
  session = Session.query(Session.hashed_id == hashed_id).get()
  if not session == None:
    session.key.delete()
    deleted = True
  return deleted

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
