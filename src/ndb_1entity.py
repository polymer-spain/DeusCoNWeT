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
"""NDB Instances """

class Entidad(ndb.Model):
  # "Componente"
  # nombre_componente = ndb.StringProperty()
  # x_componente = ndb.FloatProperty()
  # y_componente = ndb.FloatProperty()
  # url_componente = ndb.StringProperty()
  # height_componente = ndb.StringProperty()
  # width_componente = ndb.StringProperty()

  # #"User Rating"
  # full_name_id_rating = ndb.StringProperty() # ¡¡PREGUNTAR!!
  # rating_value = ndb.FloatProperty()

  # # "Grupo"
  # nombre_grupo = ndb.StringProperty()
  # lista_Usuarios_grupo = ndb.StringProperty(repeated=True)
  # descripcion_grupo = ndb.StringProperty()

  # # "Token"
  # id_fb = ndb.StringProperty()
  # token_fb = ndb.StringProperty()
  # id_tw = ndb.StringProperty()
  # token_tw = ndb.StringProperty()
  # id_sof = ndb.StringProperty()
  # token_sof = ndb.StringProperty()
  # id_li = ndb.StringProperty()
  # token_li = ndb.StringProperty()
  # id_ins = ndb.StringProperty()
  # token_ins = ndb.StringProperty()
  # id_git = ndb.StringProperty()
  # token_git = ndb.StringProperty()
  # id_google = ndb.StringProperty()
  # token_google = ndb.StringProperty()

  # # "Usuario social"
  # nombre_rs_pertenece = ndb.StringProperty(repeated=True)
  # siguiendo_rs_pertenece = ndb.IntegerProperty(repeated=True)
  # seguidores_rs_pertenece = ndb.IntegerProperty(repeated=True)
  # url_sig_rs_pertenece = ndb.StringProperty(repeated=True)
  # url_seg_rs_pertenece = ndb.StringProperty(repeated=True)

  # "Usuario"

  id_unico = ndb.IntegerProperty()

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

def getToken(self, nombre_usuario, rs):
  user = Entidad.query(Entidad.id_unico == nombre_usuario).get()
  res = ''
  if rs == "facebook":
    res = user.token_fb
  elif rs == "twitter":
    res = user.token_tw
  elif rs == "stack-overflow":
    res = user.token_sof
  elif rs == "linkedin":
    res = user.token_li
  elif rs == "instagram":
    res = user.token_ins
  elif rs == "github":
    res = user.token_git
  elif rs == "google":
    res = user.token_google
  else:
    print "La red social solicitada no esta contemplada"
  return res