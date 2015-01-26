""" Copyright 2015 Luis Ruiz Ruiz
	Copyright 2015 Ana Isabel Lopera Martínez
	Copyright 2015 Miguel Ortega Moreno

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
# -*- coding: utf8 -*-
import webapp2
import ndb
import re

class ComponentListHandler(webapp2.RequestHandler):
  """
  Class that defines the component list resource

  Methods:
  get -- Gets a filtered list of the components stored in the system  
  post -- Uploads a component
  """

  # GET Method
  def get(self):
    """ Gets a filtered list of the components stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    # Get the params in the request
    user = self.request.get("user", default_value = "null")
    sortBy = self.request.get("sortBy", default_value = "stars")
    query = self.request.get("query", default_value = "null")
    orderBy = self.request.get("orderBy", default_value = "desc")
    

  #POST Method
  #Uploads a component
  def post(self):
    pass


class ComponentHandler(webapp2.RequestHandler):
  """
  Class that defines the component resource

  Methods:
  get -- Gets the info about a component 
  put -- Adds a rating about a component  
  """

  # GET Method
  def get(self):
    """ Gets the info about a component or
    gets a filtered list of the components stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    # Get the params in the request
    componentId = self.request.get("componentId", default_value = "null")
    user = self.request.get("user", default_value = "null")
    if  not componentId == "null":
      # Returns the component queried
      component = ndb.Repo.query(Repo.full_name_id == idComponent).get()
      # TODO: Renders the page



  # POST Method
  def post(self):
    """ - Add a rating about a component
    Keyword arguments: 
      self -- info about the request build by webapp2
    """
    componentId = self.request.get("componentId", default_value = "null")
    user = self.request.get("user", default_value = "null")
    rate = self.request.get("rate", default_value = 0)




app = webapp2.WSGIApplication([
    ('/components', ComponentListHandler),
    ('/components/(/S)', ComponentHandler)
], debug=True)