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
"""NDB Instances """
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

class Autor(ndb.Model):
  login = ndb.StringProperty()
  user_id = ndb.IntegerProperty()
  html_url = ndb.StringProperty()
  followers = ndb.IntegerProperty()
  following = ndb.IntegerProperty()

class Componente(ndb.Model):
  full_name = ndb.StringProperty() # Format: ":author/:repo"
  repo_id = ndb.IntegerProperty() # Id of the repo in Github
  name_repo = ndb.StringProperty()
  # ComponentID for the repo. It's the id for the repo managed by polymer_bricks
  full_name_id = ndb.StringProperty() # Format: ":author_:repo"
  autor = ndb.StructuredProperty(Autor)
  html_url = ndb.StringProperty()
  description = ndb.StringProperty()
  stars = ndb.IntegerProperty()
  forks = ndb.IntegerProperty()
  languages = ndb.StringProperty(repeated=True)
  #tags = ndb.StructuredProperty(Tag, repeated=True)
  #releases = ndb.StructuredProperty(Release, repeated=True)  
  # Reputation related fields
  reputation = ndb.FloatProperty()
  ratingsCount = ndb.IntegerProperty()
  reputation_sum = ndb.FloatProperty()
  # SHA-256 string that identifies the repo 
  #repo_hash = ndb.StringProperty()
  # Lowercased names in order to obtain a properly ordering in ndb queries
  #name_repo_lower_case = ndb.StringProperty()
  #full_name_repo_lower_case = ndb.StringProperty()

  #Returns the rounded value corresponding to the reputation of the repo
  def roundReputation(self):
    repValue = float(self.reputation)
    roundRep = round(repValue, 2)
    decRep = roundRep - int(roundRep)
    if decRep < 0.26:
      roundRep = roundRep - decRep
    elif decRep >= 0.26 and decRep<= 0.76:
      roundRep = int(roundRep) + 0.5
    else:
      roundRep = float(int(roundRep) + 1)
    return roundRep

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

class UserRating(ndb.Model):
  google_user_id = ndb.StringProperty()
  repo_full_name_id = ndb.StringProperty()
  repo_hash = ndb.StringProperty()
  rating_value = ndb.FloatProperty()


# Entidad Grupo
class Grupo(ndb.Model):
  nombre = ndb.StringProperty()
  lista_Usuarios = ndb.StringProperty(repeated = True)
  descripcion = ndb.StringProperty()

# Entidad usuario
class Usuario(ndb.Model):
  nombre = ndb.StringProperty()
  identificador = ndb.StringProperty()
  email = ndb.StringProperty()
  lista_Redes = ndb.StringProperty(repeated = True)
  lista_Grupos = ndb.StringProperty(repeated = True)

# Entidad RedSocial
class RedSocial(ndb.Model):
  nombre_rs = ndb.StringProperty()
  nombre_usuario = ndb.StringProperty()
  siguiendo = ndb.IntegerProperty()
  seguidores = ndb.IntegerProperty()
  url_tw_sig = ndb.StringProperty()
  url_tw_seg = ndb.StringProperty()
  url_fb_sig = ndb.StringProperty()
  url_fb_seg = ndb.StringProperty()
  # Faltan las uris del resto de apis a consultar

  # #Actualiza el número de seguidores y siguiendo de cada red red social 
  # def actualizaTwitter_sig(self):
  #   # Hay que usar el token de Twitter para acceder a la API 

  # def actualizaTwitter_seg(self):
  #   # Hay que usar el token de Twitter para acceder a la API 

  # def actualizaFacebook_sig(self):
  #   # Hay que usar el token de Facebook para acceder a la API

class Token(ndb.Model):
  nombre_usuario = ndb.StringProperty()
  id_fb = ndb.StringProperty()
  token_fb = ndb.StringProperty()
  id_tw = ndb.StringProperty()
  token_tw = ndb.StringProperty()
  id_sof = ndb.StringProperty()
  token_sof = ndb.StringProperty()
  id_li = ndb.StringProperty()
  token_li = ndb.StringProperty()
  id_ins = ndb.StringProperty()
  token_ins = ndb.StringProperty()
  id_git = ndb.StringProperty()
  token_git = ndb.StringProperty()
  id_google = ndb.StringProperty()
  token_google = ndb.StringProperty()