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

import webapp2
from google.appengine.ext import ndb
from google.appengine.api import memcache

class UserListHandler(webapp2.RequestHandler):

    """
  Class that defines the user resource
  It acts as the handler of the /usuarios/{user_id} resource
  Methods:
  get -- Returns a list of all the users stored in the system
  post -- Adds a new user to the system
  """

  # GET Method

    def get(self):
        """ Returns a list of all the users stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """

        results = Usuario.query().fetch()

        self.response.content_type = 'application/json'
        self.response.write(json.dumps(results))

  # POST Method

    def post(self):
        """ Adds a new user to the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """

        name = self.request.get('name', default_value='None')
        email = self.request.get('email', default_value='None')
        if not name == 'None' and not email == 'None':

      # Checks if the user was previously stored

            user = Usuario.query(Usuario.email == email).get()
            if user == None:

        # Creates the new user

                newUser = Usuario(nombre=name, identificador=name,
                                  email=email, lista_Redes=[],
                                  lista_Grupos=[])
                newUser.put()
                self.response.set_status(200)
            else:

        # Returns a Not Modified status

                self.response.set_status(304)
        else:

      # Returns a Bad Request status

            self.response.set_status(400)


class UserHandler(webapp2.RequestHandler):

    """
  Class that defines the user resource
  It acts as the handler of the /usuarios/{user_id} resource
  Methods:
  get -- Gets the info about a user  
  """

  # GET Method

    def get(self, user_id):
        """ Gets the info about an user
    Keyword arguments: 
      self -- info about the request build by webapp2
      user_id -- id of the user 
    """

    # Returns the component queried

        user = Usuario.query(Usuario.identificador == user_id).get()
        if user == None:
            self.response.set_status(404)
        else:

      # Builds the response

            response = {
                'name': user.nombre,
                'user_id': user.identificador,
                'email': user.email,
                'network_list': user.lista_Redes,
                'group_list': user.lista_Grupos,
                }
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
