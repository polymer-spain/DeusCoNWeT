#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Copyright 2015 Luis Ruiz Ruiz
  Copyright 2015 Ana Isabel Lopera Martínez
  Copyright 2015 Miguel Ortega Moreno
  Copyright 2015 Juan Francisco Salamanca Carmona

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

import webapp2, json
import ndb_pb
from google.appengine.api import memcache
from api_oauth import SessionHandler
class UserListHandler(SessionHandler):

  """
  Class that defines the user resource
  It acts as the handler of the /usuarios/ resource
  Methods:
  get -- Returns a list of all the users stored in the system
  post -- Adds a new user to the system
  """

  # GET Method

    def get(self):
      users_list = ndb_pb.getUsers()
      if len(users_list) == 0:
        self.response.content_type = 'application/json'
        self.response.write('')
        self.response.set_status(204)
      else:
        self.response.content_type = 'application/json'
        self.response.write(users_list)
        self.response.set_status(200)

class UserHandler(SessionHandler):

  """
  Class that defines the user resource
  It acts as the handler of the /usuarios/{user_id} resource
  Methods:
  get -- Gets the info about a user  
  """
  def get(self, user_id):
    cookie_value = self.request.cookies.get('session')
    if not cookie_value == None:
      # Obtains info related to the user authenticated in the system
      user_key = self.getUserInfo(cookie_value)
      user_info = ndb_pb.getUser(user_key)
      if user_info == None:
        self.response.content_type = 'application/text'
        self.response.write("")
        self.response.set_status(404)
      else:
        user = json.dumps(user_info)
        # Depending on the user making the request, the info returned will be one or another
        if user["id_usuario"] == user_id:
          self.response.content_type = 'application/json'
          self.response.write(user_info)
          self.response.set_status(200)
        else:
          user_dict = {"id_usuario": user["id_usuario"],
                        "descripcion": user["descripcion"],
                        "imagen": user["imagen"],
                        "sitio_web": user["sitio_web"],
                        "redes": user["redes"],
                        "componentes": user["components"]}
          if user["private_email"] == False:
            user_dict["email"] = user["email"]
          if user["private_phone"] == False:
            user_dict["telefono"] = user["telefono"]
          self.response.content_type = 'application/json'
          self.response.write(user_dict)
          self.response.set_status(200)

  def post(self, user_id):
    cookie_value = self.request.cookies.get('session')
    if not cookie_value == None:
      user_key = self.getUserInfo(cookie_value)
      # It is neccesary to get the parameters from the request
      try:
        
      user_info = ndb_pb.actualizaUsuario()

      