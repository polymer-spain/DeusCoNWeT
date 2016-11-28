#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Copyright 2016 Luis Ruiz Ruiz
    Copyright 2016 Ana Isabel Lopera Martinez
    Copyright 2016 Miguel Ortega Moreno
    Copyright 2016 Sandra Gómez Yagüez

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

import os
import yaml
import logging
import sys
from Crypto.Cipher import AES
import base64
sys.path.insert(0, 'api_handlers/lib')
from mongoengine import * 
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

mongoOptions = os.path.abspath(os.path.join(basepath, "mongo.yaml"))
with open(mongoOptions, "r") as ymlfile:
    mongoCfg = yaml.load(ymlfile)

# If the param is set wrong, we configure component versioning as static
component_versioning = cfg["component_versioning"] if cfg["component_versioning"] in ["static", "dynamic"] else "static"

# Connect to mongo
# ENV_MODE = os.environ.get('ENV_MODE',None)
database = mongoCfg['database']

# if ENV_MODE == 'test':
#     database = mongoCfg['database_test']

logging.info('Connecting to ' + database + ' database')
db = connect(database, host=mongoCfg['host'], port=mongoCfg['port'], password=mongoCfg['pwd'], username=mongoCfg['user'])

#####################################################################################
# Definicion de entidades de la base de datos
#####################################################################################


class ComponentAttributes(Document):
  component_id =StringField(required=True)
  access_token =StringField()
  secret_token =StringField()
  consumer_key =StringField()
  consumer_secret =StringField()
  endpoint =StringField()
  component_base =StringField()
  language =StringField(default=":language")
  count =IntField()
  username =StringField()
  token =StringField()
  mostrar =IntField()
  component_directory =StringField()
  accessToken =StringField()

class BetaUser(Document):
  email = StringField(required=True)
  name = StringField()
  surname = StringField()

class Component(Document):
  component_id = StringField()
  url = StringField()
  input_type = ListField(StringField())
  output_type = ListField(StringField())
  rs = StringField()
  description = StringField()
  # List of versions available for a component
  version_list = ListField(StringField())
  # Index to control the version that will be served to the next user that adds it to his dashboard
  version_index = IntField()
  # Determines the times that the general component has been tested
  test_count = IntField(default=0)
  # Represents if the component will served in a predetermined way to every new user in the system
  predetermined = BooleanField(default=False)
  # Preasigned version to load the component. It needs to be confirmed
  version = StringField()
  attributes = ReferenceField(ComponentAttributes)

class UserComponent(Document):
  component_id = StringField(required=True)
  x = FloatField()
  y = FloatField()
  height = StringField()
  width = StringField()
  listening = StringField()
  # Actual version of the component that is being tested
  version = StringField()
  # Represents if the component is placed in the dashboard
  active = BooleanField(default=True)

# Representa que versiones de un componente en particular han sido testeadas por un usuario
class ComponentTested(Document):
  # User that tested the component
  user_id = StringField(required = True)
  component_id = StringField(required=True)
  # List of versions tested by the user
  versions_tested = ListField(StringField())
  # Actual version tested by the user
  actual_version = StringField()
class UserRating(Document):
  component_id = StringField()
  version = StringField() # Version of the component rated
  rating_value = FloatField()
  # In the future, this field it could be a reference to an entity that would hold the evaluation resuls
  # Optional_evaluation indicates whether a user has completed the optional form or not.
  optional_evaluation = BooleanField(default=False)

class Group(Document):
  group_name = StringField(required=True)
  user_list = StringField()
  description = StringField()

class Token(Document):
  identifier = StringField()
  token = StringField()
  social_name = StringField()

class SocialUser(Document):
  social_name = StringField(required=True)


class User(Document):
  user_id = StringField()
  email = StringField()
  private_email = BooleanField(default=False)
  phone = IntField()
  private_phone = BooleanField(default=False)
  description = StringField()
  website = StringField()
  image = StringField()
  tokens = ListField(ReferenceField(Token))
  net_list = ListField(ReferenceField(SocialUser))
  group_list = ListField(ReferenceField(Group)) 
  rates = ListField(ReferenceField(UserRating))
  components = ListField(ReferenceField(UserComponent))
  # The next info is related to the user profile
  name = StringField()
  surname = StringField()
  age = IntField()
  studies = StringField() # This field is set through the cuestionaire
  tech_exp = StringField() # This field is set through the cuestionaire
  social_nets_use = StringField() # This field is set through the cuestionaire
  gender = StringField() # This field is set through the cuestionaire

class GitHubAPIKey(Document):
  token = StringField()

# Represents the session value for a given user in the system
class Session(Document):
  user_key = StringField() # Era el valor del ID pero no se setear esto a un valor virtual
  hashed_id = StringField()

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
# Params: - general_component: Component Model that it is desired to be served to the user
# Returns: string that represents the version that will be served to the user

def setComponentVersion(general_component):
  # print "====================================================="
  # print "Entrada en la llamada de setting"
  # print "====================================================="
  version = ""
  if component_versioning == "dynamic":
    # We set the version that will be served to the user
    version = general_component.version_list[general_component.version_index]
    # We change the version_index field, that represents the version that will be served to the next user
    new_version_index = (general_component.version_index + 1) % len(general_component.version_list)
    # Update the info about the component changed
    general_component.update(set__version_index=str(new_version_index))
  # If the component versioning is set as static, we always set the stable version for the component
  elif component_versioning == "static":
    version="stable"

  return version

def getComponentEntity(component_id):
  general_component = Component.objects(component_id=component_id)
  if general_component.count() > 0:
    return general_component[0]
  else:
    return general_component

#########################################################################################
# Definicion de metodos relacionados con operaciones de alto nivel sobre la base de datos
# Operaciones relacionadas con el dashboard de usuario
#########################################################################################

# Adds to the user dashboard those component defined as predetermined in the system
def assignPredeterminedComponentsToUser(entity_key):
  # Obtains the predetermined components of the system and adds it to the User
  # We consider that we will have at most 10 predetermined components in our system
  # print "====================================================="
  # print "Entrada en la primera llamada de la asignacion"
  # print "====================================================="
  predetermined_comps = Component.objects(predetermined=True).limit(10)
  
  for comp in predetermined_comps:
    st = activateComponentToUser(comp.component_id, entity_key)
    
# Set the version for the component in the case it will be added to the user dashboard
# def setPreasignedVersion(component_id):
#  comp = Component.query(Component.component_id == component_id).get()
#  version = setComponentVersion(comp)
#  comp.preasigned_version = version
#  comp.put()
#  return version

# Adds a given component to the user,
# creating or updating the corresponding entities that store properties about this action
def activateComponentToUser(component_id, user): #No entiendo lo que pretende hacer
  general_component = Component.objects(component_id=component_id)[0]
  user_component = None
  status = False
  # We check if the user has added the corresponding social network to his/her profile
  for social_network in user.net_list:
    if general_component.rs == social_network.social_name:
      #We check if the component provided is in the user component list
      # If not, we create a new UserComponent Entity, setting the component version the user will use
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
          user.save()
          status = True
      else:
        # We set the version of the component
        general_component = getComponentEntity(component_id)
        version = general_component.version
        # We create a new UserComponent entity
        user_component = UserComponent(component_id=component_id, x=0, y=0, height="0", width="0", listening=None, version=version).save()
        # We add the component to the component_list of the user
        user.components.append(user_component)
        user.save()

        # We increase the counters that represents the times that a given component has been tested (general and versioned)
        new_version = setComponentVersion(general_component)
        # print "============================================="
        general_component.version = new_version
        general_component.test_count += 1
        general_component.save()
        status = True

      # We store in a ComponentTested entity the new version tested by the user
      user_component_tested = ComponentTested.objects(component_id=component_id, user_id=user.user_id)[0]
      if not user_component_tested == None:
        # We update the field that represents the actual version that is being tested
        user_component_tested.actual_version = version
        # We add the version to the versions tested list, if is not was added previously
        if not version in user_component_tested.versions_tested:
          user_component_tested.versions_tested.append(version)
          user_component_tested.save()
      else:
        # We create a new ComponentTested entity to store the versions of a component tested by the user
        component_tested = ComponentTested(component_id=component_id, user_id=user.user_id, versions_tested=[version], actual_version=version).save()
  return status






# Removes the component from the user's dashboard
# It turns the field active to False, thus the component will not be listed as a
# component included in the user's dashboard
def deactivateUserComponent(document_id, component_id):
  user = User.objects(id=document_id)[0]
  status = False
  # We check if the component provided is in the user component list
  for comp in user.components:
    if comp.component_id == component_id and comp.active:
      # Deactivates the component
      comp.active = False
      user.save()
      status = True

  return status

#####################################################################################
# Definicion de metodos para insertar, obtener o actualizar datos de la base de datos
#####################################################################################

## Metodos asociados a la entidad Token

"""
Get access token of a social network
:param id_rs: user identifier Ex: lrr9204
:param social_net: social network to look for access_token
:return ans: And dictionary: {token:access_token of the social network, user_id: user name in picbit, token_id:Name in the social network}
"""

def getToken(id_rs, social_net):  
  ans = None
  token = Token.objects(identifier=id_rs, social_name=social_net)
  if token.count() > 0:
    token = token[0]
    user = User.objects(tokens=token.id)
    if user.count() > 0:
      user = user[0]
      cipher = getCipher(str(token.id))
      ans = {"token": decodeAES(cipher, token.token),
            "user_id": user.user_id,
            "token_id": token.identifier}
  return ans

def getUserTokens(user_id):
  token_aux = {}
  ans = None
  user = User.objects(user_id=user_id)
  if user.count() > 0:
    user = user[0]
    for token in user.tokens:
      cipher = getCipher(str(token.id)) # coger el id 
      token_aux[token.social_name] = decodeAES(cipher, token.token)
    ans = json.dumps(token_aux)
  return ans

def searchToken(token_id, rs):
  token = Token.objects(identifier=token_id, social_name=rs)
  if token.count() > 0:
    token = token[0]
    cipher = getCipher(str(token.id))
    return decodeAES(cipher, token.token)
  else:
    return None

def modifyToken(user_id, new_token, rs):
  tok = Token.objects(identifier=user_id, social_name=rs)
  if tok.count() > 0:
    tok = tok[0]
  # Ciphers the token
  cipher = getCipher(str(tok.id))
  new_token = encodeAES(cipher, new_token)

  # Updates the token
  tok.token = new_token
  token_key = tok.save()

  # Updates the token in the user credential list
  token_aux = Token(identifier=user_id, social_name=rs).save()
  user = User.objects(tokens=token_aux)
  if user.count() > 0:
    tokens = user.tokens
    for token in tokens:
      if token.identifier==user_id and token.social_name==rs:
        token.token = new_token

    user.save()
  return str(user.id)
## Metodos asociados a la entidad Usuario
# Obtiene la lista de credenciales (token_id, red_social) de un usuario en el sistema
def getUserCredentialList(user_id):
  user = User.objects(user_id=user_id)
  if user.count()>0:
    user = user[0]
  credential_list = []
  for token in user.tokens:
    credential = {"token_id": token.identifier,
    "social_network": token.social_name}
    credential_list.append(credential)
  return credential_list


def getUser(user_id, component_detailed_info = False):
  user = User.objects(user_id=user_id)
  user_info = None
  
  if user.count() > 0:
    user = user[0]
    rates = user.rates; nets = user.net_list
    user_component_list = [];  net_names = []
    # Componemos la lista de redes a la que está suscrito un usuario
    for net in nets:
      net_names.append(net.social_name)
    
    # Componemos la lista de componentes de usuario, detallada o reducida
    user_component_list = getUserComponentList(user_id, component_detailed_info)
    # Obtenemos la lista de credenciales de usuario
    credential_list = getUserCredentialList(user_id)
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
                "token_ids": credential_list,
                "components": user_component_list}

  return user_info

def getUserId(user_id):
  user = User.objects(id=user_id)
  user_id = None
  if user.count() > 0:
    user_id = str(user[0].id)
  return user_id
"""
  Insert a user in database
  :param rs: The name of the social network. Ex: twitter
  :param ide: Identifier of the user in a social network. Ex: lrr9204
  :param access_token: Access_token's social nertork
  :param data: Data about the User
  :return key, user: Key is the document ID and User is the document (Document ~= Entity)
"""
def insertUser(rs, ide, access_token, data=None):
  user = User()
  # We add to the user's net list the social network used to sign up to the system
  user_net = SocialUser(social_name=rs).save()
  user.net_list.append(user_net)

  # We store the user info passed in the data argument
  if not data == None:
    if ide:
      user.user_id = ide
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
      user.website = data["website"]

  # Inserts the user entity
  user_key = user.save()

  token = Token(identifier=ide, token="", social_name=rs).save()
  # Ciphers the access token and stores in the datastore
  cipher = getCipher(str(token.id))
  token.token = encodeAES(cipher, access_token)
  token.save()
  user.tokens.append(token)

  # Updates the user entity
  user.save()

  return user_key


# Actualiza la info de usuario proporcionada y retorna una lista de los elementos actualizados
"""
  Update the user information provided

  :param user_id: username's picbit
  :param data: Field will be updated 
  :return updated_data: updated fields
"""
def updateUser(user_id, data):
  user = User.objects(user_id=user_id)
  if user.count()>0:
    user = user[0]
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
    activated = activateComponentToUser(comp_name, user)
    if activated:
      updated_data += ["component"]

  if data.has_key("rate"):
    rate = data["rate"]
    # We add a Rating entity that represents the component rating
    rating = UserRating(component_id=comp_name, rating_value=rate).save()
    user.rates.append(rating)
    updated_data += ["rate"]

  # We update the optional_evaluation field
  if data.has_key("optional_evaluation"):
    user.optional_evaluation = data['optional_evaluation']

  # Updates the user data
  user.save()
  # Returns the list that represents the data that was updated
  return updated_data

"""
Insert a new token in the database
:param user_id: Id of the user in the social network
:param social_name: Name of the social network of the new token
:param access_token: new access_token ValueError
:param user_id: username's Picbit 
"""
def insertToken(document_id, social_name, access_token, user_id):
  # We create a Token Entity in the datastore
  user = User.objects(id=document_id)
  if user.count() > 0:
    user = user[0]
  tok_aux = Token(identifier=user_id, token="", social_name=social_name).save()
  # Ciphers access token that will be stored in the datastore
  cipher = getCipher(str(tok_aux.id))
  access_token = encodeAES(cipher, access_token)
  tok_aux.token = access_token
  tok_aux.save()
  # We add the Token Entity to the user credentials list
  user.tokens.append(tok_aux)
  # We add the social network to the user's nets list
  social_aux = SocialUser(social_name="social_name").save()
  if not social_aux in user.net_list:
    social_network = SocialUser(social_name=social_name).save()
    user.net_list.append(social_network)
  # Updates the user
  user.save()


def insertGroup(document_id, name, data=None):
  user = User.objects(id=document_id)
  if user.count() > 0:
      user = user[0]
  group = Group(group_name=name).save()
  users = ""

  if not data == None:
    if data.has_key("description"): group.description = data["description"]
    if data.has_key("usuarios"):
      for user in data["usuarios"]:
        users = users + user + ", "

  group.user_list = users
  user.group_list.append(group)
  user.save()


def addUserToGroup(document_id, group_name, username):
  user = User.objects(id=document_id)
  if user.count() > 0:
      user = user[0]
  groups = user.group_list

  for group in groups:
    if group.group_name == group_name:
      group.user_list += username
      group.save()

def addDescriptionToGroup(document_id, group_name, description):
  user = User.objects(id=document_id)
  if user.count() > 0:
        user = user[0]
  groups = user.group_list

  for group in groups:
    if group.group_name == group_name:
      group.description = description

  user.save()

def searchGroups(document_id):
  user = User.objects(id=document_id)[0]
  if user.count() > 0:
        user = user[0]
  ans = {}
  counter = 1
  if user.group_list:
    for group in user.group_list:
      ans[counter] = group.group_name
      counter += 1

  return json.dumps(ans)

def searchNetwork(user):
  ans = {}
  counter = 1
  if user.net_list:
    for net in user.net_list:
      ans[counter] = net.social_name
      counter += 1

  return json.dumps(ans)

# Creates a component (Component Entity)
"""
  Insert a component in the database
  :param name: Identifier of the component
  :param url: ??
  :param description: Description of the components
  :param rs: Social network needed
  :param input_t: Input attributes
  :param output_t: Output attributes
  :param version_list: List of versions
  :param predeterminated: ??
  :param endpoint: ???
  :param component_directory: Base directory of the component
"""
def insertComponent(name, url="", description="", rs="", input_t=None, output_t=None, version_list=None, predetermined=False, endpoint="", component_directory=""):
  # Generates a random initial value that represents the version of the component that will be
  # served to the next user who adds it to his dashboard
  # Depending on the social network, different attributes are needed
  attributes = None
  if rs == "twitter":
    attributes = ComponentAttributes(component_id=name, access_token="", secret_token="OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock", consumer_key="J4bjMZmJ6hh7r0wlG9H90cgEe",
                  consumer_secret="8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf", 
                  component_base="bower_components/twitter-timeline/static/", count=200, endpoint=endpoint).save()
  elif rs == "github":
    attributes = ComponentAttributes(component_id=name, component_directory=component_directory, username=":user", 
                  token="", mostrar=10).save()
  elif rs == "instagram":
    attributes = ComponentAttributes(component_id=name, endpoint=endpoint, accessToken=" ").save()
  elif rs == "googleplus":
    attributes = ComponentAttributes(component_id=name, token="").save()
  elif rs == "facebook":
    attributes = ComponentAttributes(component_id=name, access_token="", component_directory=component_directory).save()
  initial_index = random.randint(0, len(version_list)-1)
  component = Component(component_id=name, url=url, input_type=input_t, output_type=output_t,
   rs=rs, description=description, version_list=version_list, version_index=initial_index, predetermined=predetermined,
   attributes=attributes)
  # We create a new VersionedComponent Entity for each version_added to the version_list
  # for version in version_list:
  #   versionedComponent = VersionedComponent(version=version, component_id=component.component_id)
  #   versionedComponent.save()
  created = True
  # Saves the changes to the entity

  component.version = setComponentVersion(component)
  component.test_count += 1
  component.save()


# Modifies the related info about a General component in the system (ComponentEntity)
def updateComponent(component_id, url="", description="", rs="", input_t=None, output_t=None, version_list=None):
  component = Component.objects(component_id=component_id)
  if component.count() > 0:
    component = component[0]
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
        versionedComponent = VersionedComponent(version=version, component_id=component.component_id).save()
    # Saves the changes to the entity
    component.save()


def insertUserComponent(document_id, name, x=0, y=0, height="", width="", listening=""):
  user = User.objects(id=document_id)
  if user.count() > 0:
        user = user[0]
  component = UserComponent(name=name, x=x, y=y, height=height, width=width, listening=listening).save()
  user.components.append(component)
  user.save()


# Modifies the user's preferences stored related to a component
def modifyUserComponent(document_id, name, data):
  user = User.objects(id=document_id)[0]
  if user.count() > 0:
        user = user[0]
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
  user.save()

def addListening(document_id, name, events):
  user = User.objects(id=document_id)
  if user.count() > 0:
        user = user[0]
  comps = user.components
  for comp in comps:
    if comp.component_id == name:
      for event in events:
        comp.listening += event + ""

  user.save()

"""
Search a compoent by component_id
:param component_id: identifier of a component
:return document: the document found of a component
"""
def searchComponent(component_id):
  return Component.objects(component_id=component_id)[0]
"""
  Get a component from user
:param document_id: Document id of the user 
:param name: name of the component 
:param all_info:
"""
def getComponent(document_id, name, all_info=False):
  user = User.objects(id=document_id)
  if user.count() > 0:
        user = user[0]
  comp = Component.objects(component_id=name)[0]
  if comp == None:
    ans = None
  else:
    rate = UserRating.objects(component_id=name)[0]
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
def getUserComponent(document_id, component_id):
  user = User.objects(id=document_id)
  if user.count() > 0:
        user = user[0]
  result = None
  user_comps = user.components
  for comp in user_comps:
    if comp.component_id == component_id:
      result = comp
  return result

# Retorna una lista de Componentes pertenecientes al dashboard de usuario, incluyendo la valoración del usuario
def getUserComponentList(user_id, component_detailed_info=False):
  # Obtenemos la valoración del componente en particular
  component_list = []
  user = User.objects(user_id=user_id)
  if user.count() > 0:
        user = user[0]
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

"""
  Get list of components
  :param document_id: Document identifier
  :param rs: Name of the social network
  :param all_info: Get all the information of the User
  :param filter_by_user: ???
  :return json: Component information in JSON format
"""
def getComponents(document_id=None, rs="", all_info=False, filter_by_user=False):
  ans = []
  general_comp = {}
  if filter_by_user:
    # user id specified
    if rs == "":
      # without social network
      if all_info:
        # complete information
        # Info for the components used by the specified user
        user = User.objects(id=document_id)
        if user.count() > 0:
          user = user[0]
        user_comps = user.components
        for comp in user_comps:
          # Returns the info about the active components in the user dashboard
          if comp.active:
            info_comp = Component.objects(component_id=comp.component_id)[0]
            rate = UserRating.objects(component_id=comp.component_id)[0]
            attributes = ComponentAttributes.objects(component_id=comp.component_id)[0]
            general_comp["component_id"] = str(comp.component_id)
            general_comp["url"] = str(info_comp.url)
            general_comp["social_network"] = str(info_comp.rs)
            general_comp["description"] = str(info_comp.description)
            general_comp["x"] = str(comp.x)
            general_comp["y"] = str(comp.y)
            general_comp["input_type"] = str(info_comp.input_type)
            general_comp["output_type"] = str(info_comp.output_type)
            general_comp["listening"] = str(comp.listening)
            general_comp["height"] = str(comp.height)
            general_comp["width"] = str(comp.width)
            general_comp["version"] = str(comp.version)
            general_comp["attributes"] = {}
            if general_comp["social_network"] == "twitter":
              general_comp["attributes"]["access_token"] = str(attributes.access_token)
              general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
              general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
              general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
              general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
              general_comp["attributes"]["component_base"] = str(attributes.component_base)
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["count"] = str(attributes.count)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/twitter-logo.png')
              general_comp["tokenAttr"] = str('access_token')
            elif general_comp["social_network"] == "github":
              general_comp["attributes"]["username"] = str(attributes.username)
              general_comp["attributes"]["token"] = str(attributes.token)
              general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/github-icon.png')
              general_comp["tokenAttr"] = str('token')
            elif general_comp["social_network"] == "instagram":
              general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
              general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
              general_comp["attributes"]["language"] = str(attributes.language)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/instagram-icon.png')
              general_comp["tokenAttr"] = str('accessToken')
            elif general_comp["social_network"] == "googleplus":
              general_comp["attributes"]["token"] = str(attributes.token)
              general_comp["attributes"]["language"] = str(attributes.language)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/google-icon.svg')
              general_comp["tokenAttr"] = str('token')
            elif general_comp["social_network"] == "facebook":
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
              general_comp["attributes"]["access_token"] = str(attributes.access_token)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/facebook-icon.png')
              general_comp["tokenAttr"] = str('access_token')
            if not rate == None:
              general_comp["rate"] = str(rate.rating_value)
            else:
              general_comp["rate"] = str(0)
            # ans = general_comp
            ans.append(general_comp)


      else:
        user_comps = user.components
        # Now we get the general info about the components used by the user
        for comp in user_comps:
          if comp.active:
            info_comp = Component.objects(component_id=comp.component_id)[0]
            rate = UserRating.objects(component_id=comp.component_id)[0]
            general_comp["component_id"] = str(info_comp.component_id)
            general_comp["url"] = str(info_comp.url)
            general_comp["social_network"] = str(info_comp.rs)
            general_comp["description"] = str(info_comp.description)
            general_comp["version"] = str(comp.version)
            general_comp["attributes"] = {}
            if general_comp["social_network"] == "twitter":
              general_comp["attributes"]["access_token"] = str(attributes.access_token)
              general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
              general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
              general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
              general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
              general_comp["attributes"]["component_base"] = str(attributes.component_base)
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["count"] = str(attributes.count)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/twitter-logo.png')
              general_comp["tokenAttr"] = str('access_token')
            elif general_comp["social_network"] == "github":
              general_comp["attributes"]["username"] = str(attributes.username)
              general_comp["attributes"]["token"] = str(attributes.token)
              general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/github-icon.png')
              general_comp["tokenAttr"] = str('token')
            elif general_comp["social_network"] == "instagram":
              general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
              general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
              general_comp["attributes"]["language"] = str(attributes.language)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/instagram-icon.png')
              general_comp["tokenAttr"] = str('accessToken')
            elif general_comp["social_network"] == "googleplus":
              general_comp["attributes"]["token"] = str(attributes.token)
              general_comp["attributes"]["language"] = str(attributes.language)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/google-icon.svg')
              general_comp["tokenAttr"] = str('token')
            elif general_comp["social_network"] == "facebook":
              general_comp["attributes"]["language"] = str(attributes.language)
              general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
              general_comp["attributes"]["access_token"] = str(attributes.access_token)
              json.dumps(general_comp["attributes"])
              general_comp["img"] = str('images/components/facebook-icon.png')
              general_comp["tokenAttr"] = str('access_token')
            if not rate == None:
              general_comp["rate"] = str(rate.rating_value)
            else:
              general_comp["rate"] = str(0)
            ans.append(json.dumps(general_comp))

    else:
      if all_info:
        user_comps = user.components
        for comp in user_comps:
          if comp.active:
            info_comp = Component.objects(component_id=comp.component_id, rs=rs)[0]
            rate = UserRating.objects(component_id=comp.component_id)[0]
            if not info_comp == None:
              general_comp["component_id"] = str(comp.component_id)
              general_comp["url"] = str(info_comp.url)
              general_comp["social_network"] = str(info_comp.rs)
              general_comp["description"] = str(info_comp.description)
              general_comp["x"] = str(comp.x)
              general_comp["y"] = str(comp.y)
              general_comp["input_type"] = str(info_comp.input_type)
              general_comp["output_type"] = str(info_comp.output_type)
              general_comp["listening"] = str(comp.listening)
              general_comp["height"] = str(comp.height)
              general_comp["width"] = str(comp.width)
              general_comp["version"] = str(comp.version)
              general_comp["attributes"] = {}
              if general_comp["social_network"] == "twitter":
                general_comp["attributes"]["access_token"] = str(attributes.access_token)
                general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
                general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
                general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
                general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
                general_comp["attributes"]["component_base"] = str(attributes.component_base)
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["count"] = str(attributes.count)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/twitter-logo.png')
                general_comp["tokenAttr"] = str('access_token')
              elif general_comp["social_network"] == "github":
                general_comp["attributes"]["username"] = str(attributes.username)
                general_comp["attributes"]["token"] = str(attributes.token)
                general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/github-icon.png')
                general_comp["tokenAttr"] = str('token')
              elif general_comp["social_network"] == "instagram":
                general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
                general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
                general_comp["attributes"]["language"] = str(attributes.language)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/instagram-icon.png')
                general_comp["tokenAttr"] = str('accessToken')
              elif general_comp["social_network"] == "googleplus":
                general_comp["attributes"]["token"] = str(attributes.token)
                general_comp["attributes"]["language"] = str(attributes.language)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/google-icon.svg')
                general_comp["tokenAttr"] = str('token')
              elif general_comp["social_network"] == "facebook":
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
                general_comp["attributes"]["access_token"] = str(attributes.access_token)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/facebook-icon.png')
                general_comp["tokenAttr"] = str('access_token')
              if not rate == None:
                general_comp["rate"] = rate.rating_value
              else:
                general_comp["rate"] = 0
              ans.append(json.dumps(general_comp))
      else:
        user_comps = user.components
        # Now we get the general info about the components used by the user
        for comp in user_comps:
          if comp.active:
            info_comp = Component.objects(component_id=comp.component_id, rs=rs)[0]
            rate = UserRating.objects(component_id=comp.component_id)[0]
            if not info_comp == None:
              general_comp["component_id"] = str(info_comp.component_id)
              general_comp["url"] = str(info_comp.url)
              general_comp["social_network"] = str(info_comp.rs)
              general_comp["description"] = str(info_comp.description)
              general_comp["version"] = str(comp.version)
              general_comp["attributes"] = {}
              if general_comp["social_network"] == "twitter":
                general_comp["attributes"]["access_token"] = str(attributes.access_token)
                general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
                general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
                general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
                general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
                general_comp["attributes"]["component_base"] = str(attributes.component_base)
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["count"] = str(attributes.count)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/twitter-logo.png')
                general_comp["tokenAttr"] = str('access_token')
              elif general_comp["social_network"] == "github":
                general_comp["attributes"]["username"] = str(attributes.username)
                general_comp["attributes"]["token"] = str(attributes.token)
                general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/github-icon.png')
                general_comp["tokenAttr"] = str('token')
              elif general_comp["social_network"] == "instagram":
                general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
                general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
                general_comp["attributes"]["language"] = str(attributes.language)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/instagram-icon.png')
                general_comp["tokenAttr"] = str('accessToken')
              elif general_comp["social_network"] == "googleplus":
                general_comp["attributes"]["token"] = str(attributes.token)
                general_comp["attributes"]["language"] = str(attributes.language)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = str('images/components/google-icon.svg')
                general_comp["tokenAttr"] = str('token')
              elif general_comp["social_network"] == "facebook":
                general_comp["attributes"]["language"] = str(attributes.language)
                general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
                general_comp["attributes"]["access_token"] = str(attributes.access_token)
                json.dumps(general_comp["attributes"])
                general_comp["img"] = 'images/components/facebook-icon.png'
                general_comp["tokenAttr"] = 'access_token'
              if not rate == None:
                general_comp["rate"] = rate.rating_value
              else:
                general_comp["rate"] = 0
              ans.append(json.dumps(general_comp))
  else:
    # Not user id. In this case, the info returned will be always reduced
    if not all_info:
      if rs == "":
        components = Component.objects().limit(20)
        for component in components:
          rate = UserRating.objects(component_id=component.component_id)[0]
          attributes = ComponentAttributes.objects(component_id=component.component_id)[0]
          general_comp["component_id"] = str(component.component_id)
          general_comp["url"] = str(component.url)
          general_comp["social_network"] = str(component.rs)
          general_comp["description"] = str(component.description)
          general_comp["version"] = str(component.version)
          general_comp["attributes"] = {}
          if general_comp["social_network"] == "twitter":
            general_comp["attributes"]["access_token"] = str(attributes.access_token)
            general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
            general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
            general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
            general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
            general_comp["attributes"]["component_base"] = str(attributes.component_base)
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["count"] = str(attributes.count)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/twitter-logo.png')
            general_comp["tokenAttr"] = str('access_token')
          elif general_comp["social_network"] == "github":
            general_comp["attributes"]["username"] = str(attributes.username)
            general_comp["attributes"]["token"] = str(attributes.token)
            general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/github-icon.png')
            general_comp["tokenAttr"] = str('token')
          elif general_comp["social_network"] == "instagram":
            general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
            general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
            general_comp["attributes"]["language"] = str(attributes.language)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/instagram-icon.png')
            general_comp["tokenAttr"] = str('accessToken')
          elif general_comp["social_network"] == "googleplus":
            general_comp["attributes"]["token"] = str(attributes.token)
            general_comp["attributes"]["language"] = str(attributes.language)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/google-icon.svg')
            general_comp["tokenAttr"] = str('token')
          elif general_comp["social_network"] == "facebook":
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
            general_comp["attributes"]["access_token"] = str(attributes.access_token)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/facebook-icon.png')
            general_comp["tokenAttr"] = str('access_token')
          if not rate == None:
            general_comp["rate"] = str(rate.rating_value)
          else:
            general_comp["rate"] = str(0)
          ans.append(json.dumps(general_comp))
      else:
        components = Component.objects(rs=rs).limit(20)
        for comp in components:
          rate = UserRating.objects(component_id=comp.component_id)[0]
          general_comp["component_id"] = str(comp.component_id)
          general_comp["url"] = str(comp.url)
          general_comp["social_network"] = str(comp.rs)
          general_comp["description"] = str(comp.description)
          eneral_comp["version"] = str(component.version)
          general_comp["attributes"] = {}
          if general_comp["social_network"] == "twitter":
            general_comp["attributes"]["access_token"] = str(attributes.access_token)
            general_comp["attributes"]["secret_token"] = str(attributes.secret_token)
            general_comp["attributes"]["consumer_key"] = str(attributes.consumer_key)
            general_comp["attributes"]["consumer_secret"] = str(attributes.consumer_secret)
            general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
            general_comp["attributes"]["component_base"] = str(attributes.component_base)
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["count"] = str(attributes.count)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/twitter-logo.png')
            general_comp["tokenAttr"] = str('access_token')
          elif general_comp["social_network"] == "github":
            general_comp["attributes"]["username"] = str(attributes.username)
            general_comp["attributes"]["token"] = str(attributes.token)
            general_comp["attributes"]["mostrar"] = str(attributes.mostrar)
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/github-icon.png')
            general_comp["tokenAttr"] = str('token')
          elif general_comp["social_network"] == "instagram":
            general_comp["attributes"]["accessToken"] = str(attributes.accessToken)
            general_comp["attributes"]["endpoint"] = str(attributes.endpoint)
            general_comp["attributes"]["language"] = str(attributes.language)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/instagram-icon.png')
            general_comp["tokenAttr"] = str('accessToken')
          elif general_comp["social_network"] == "googleplus":
            general_comp["attributes"]["token"] = str(attributes.token)
            general_comp["attributes"]["language"] = str(attributes.language)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/google-icon.svg')
            general_comp["tokenAttr"] = str('token')
          elif general_comp["social_network"] == "facebook":
            general_comp["attributes"]["language"] = str(attributes.language)
            general_comp["attributes"]["component_directory"] = str(attributes.component_directory)
            general_comp["attributes"]["access_token"] = str(attributes.access_token)
            json.dumps(general_comp["attributes"])
            general_comp["img"] = str('images/components/facebook-icon.png')
            general_comp["tokenAttr"] = str('access_token')
          if not rate == None:
            general_comp["rate"] = str(rate.rating_value)
          else:
            general_comp["rate"] = 0
          ans.append(json.dumps(general_comp))
  return json.dumps({'data':[json.loads(el) for el in ans]})

def newUserBeta(email, name, surname):
  beta_user = UserBeta(email=email, name=name, surname=surname).save()

def getEmails():
  beta_users = BetaUser.objects().limit(100)
  email_list = []
  for user in beta_users:
    email_list.append(user.email)

  return email_list

def updateProfile(user_id, data):
  user = User.objects(user_id=user_id)
  if user.count() > 0:
    user = user[0]
  updated_data = []
  if data.hasKey("age"):
    user["age"] = data.age
    updated_data.append("age")
  if data.hasKey("studies"):
    user["studies"] = data.studies
    updated_data.append("studies")
  if data.hasKey("tech_exp"):
    user["tech_exp"] = data.tech.exp
    updated_data.append("tech_exp")
  if data.hasKey("social_nets_use"):
    user["social_nets_use"] = data.social_nets_use
    updated_data.append("social_nets_use")
  if data.hasKey("gender"):
    user["gender"] = data.gender
    updated_data.append("gender")
  user.save()
  return updated_data

def getProfile(user_id):
  ans = None
  user = User.objects(user_id=user_id)
  if user.count() > 0:
    user = user[0]
    user_info = {"age": user.age,
                  "studies": user.studies,
                  "tech_exp": user.tech_exp,
                  "social_nets_use": user.social_nets_use,
                  "gender": user.gender,
                  "name": user.name,
                  "surname": user.surname}
    ans = json.dumps(user_info)
  return ans
def subscribedUser(email):
  emails = getEmails()
  if email in emails:
    return True
  else:
    return False

"""
  Add the user rate of a component_versioning
  :param document_id: Document ID of the user
  :param component_id: Id of the component was rated
  :param value: Rate value
  :return satatus: True if the component was rated
"""
def addRate(document_id, component_id, value):
  user = User.objects(id=document_id)
  if user.count() > 0:
    user = user[0]
  rate = UserRating(component_id=component_id, rating_value=value).save()
  status = False
  for comp_rate in user.rates:
    if comp_rate.component_id == component_id:
      comp_rate.rating_value = value
      user.save()
      status = True
  return status

def deleteUser(document_id):
  user = User.objects(id=document_id)
  if user.count() > 0:
    user = user[0]
  token_list = user.tokens
  # We delete the user tokens
  for token in token_list:
    deleteCredentials(document_id, token.social_name, token.identifier)
  # We delete the user
  user.delete()

def deleteComponent(component_name):
  status = False
  component = Component.objects(component_id=component_name)
  if component.count() > 0:
    component = component[0]
    status = True

    # We delete the component entity from the datastore
    component.delete()

    # Now, it's necessary to delete this component from all the users
    comp = UserComponent(component_id=component_name).save()
    users = User.objects(components__component_id=component_name).litmit(100)
    for user in users:
      for comp in user.components:
        # We delete the component from the user's component list
        if comp.component_id == component_name:
          user.components.remove(comp)
          user.save()

  return status

def deleteCredentials(document_id, rs, id_rs):
  status = False
  user = User.objects(id=document_id)[0]
  if user.count() > 0:
    user = user[0]
  tok = Token.objects(identifier=id_rs, social_name=rs)
  if tok.count() > 0:
    tok = tok[0]
    # We delete the token if it is not the only token stored for the user and
    # does not belong to a social network to perform login in our system
    if not rs in ['googleplus', 'facebook', 'twitter'] and not len(user.tokens) == 1:
      token_aux = tok.token
      del_token = Token(identifier = id_rs, token = token_aux, social_name = rs).save()
      tok.delete()
      if not user == None:
        # Deletes the token from the user
        user.tokens.remove(del_token)
        # Deletes the social network from the user's net_list
        social_user = SocialUser(social_name=rs).save()
        user.net_list.remove(social_user)
        user.save()
        status = True
  return status

def getUsers():
  users = User.objects().limit(100)
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
  user = User.objects(id_usuario=user_id)
  if user.count() > 0:
    return True
  else:
    return False

def getGitHubAPIKey():
  githubKey = GitHubAPIKey.objects()[0]
  return githubKey.token

# METHODS FOR SESSION SUPPORT
# Creates a sesion for the given user in the system
# If the user has an active session in the system, we delete the previous session
# and we create a new one (we only support single login per user)
def createSession(user_key, hashed_id):
  stored_session = Session.objects(user_key=user_key)
  if stored_session.count() > 0:
    stored_session = stored_session[0]
    stored_session.key.delete()
  # We create a new session assigned to the user
  session = Session(user_key=user_key, hashed_id=hashed_id).save()

def getSessionOwner(hashed_id):
  user_key = None
  session = Session.objects(hashed_id=hashed_id)
  if session.count() > 0:
    session = session[0]
    user_key = session.user_key
  return user_key

def deleteSession(hashed_id):
  deleted = False
  session = Session.objects(hashed_id=hashed_id)
  if session.count() > 0:
    session = session[0]
    session.key.delete()
    deleted = True
  return deleted

def dropDB():
  User.objects().delete()
  Token.objects().delete()
  SocialUser.objects().delete()
