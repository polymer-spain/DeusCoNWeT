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
import logging

# Import config vars and datetime package (to manage request/response cookies)
import datetime, os, yaml
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

domain = cfg["domain"]

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
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        users_list = ndb_pb.getUsers()
        if len(users_list) == 0:
          self.response.set_status(204)
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps(users_list))
          self.response.set_status(200)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        
        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)


class UserHandler(SessionHandler):

  """
  Class that defines the user resource
  It acts as the handler of the /usuarios/{user_id} resource
  Methods:
  get -- Gets the info about a user
  post -- Modifies the info related to an user
  """
  def get(self, user_id):
    tok_a = "a8fdb2b7e5b463220df"
    tok_b = "396af2c2f3b041237ba01"
    token = tok_a + tok_b
    git = ndb_pb.GitHubAPIKey(token=token)
    git.put()
    cookie_value = self.request.cookies.get("session")
    component_info = self.request.get("component_info", default_value="reduced")
    if not cookie_value == None:
      # Obtains info related to the user authenticated in the system
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        # Obtains the info related to the resource requested
        component_detailed_info = True if component_info == "detailed" else False
        user_info = ndb_pb.getUser(user_id, component_detailed_info)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "The user requested does not exist"}))
          self.response.set_status(404)
        else:
          # Obtains the user_id to check if the user active is the resource owner
          user_logged_id = ndb_pb.getUserId(user_logged_key)
          # Depending on the user making the request, the info returned will be one or another
          if user_id == user_logged_id:
            user_profile = ndb_pb.getProfile(user_id)
            if user_profile == None:
              user_info["age"] = ""
              user_info["studies"] = ""
              user_info["tech_exp"] = ""
              user_info["social_nets_use"] = ""
              user_info["gender"] = ""
              user_info["name"] = ""
              user_info["surname"] = ""
            else:
              user_profile = json.loads(user_profile)
              user_info["age"] = user_profile["age"]
              user_info["studies"] = user_profile["studies"]
              user_info["tech_exp"] = user_profile["tech_exp"]
              user_info["social_nets_use"] = user_profile["social_nets_use"]
              user_info["gender"] = user_profile["gender"]
              user_info["name"] = user_profile["name"]
              user_info["surname"] = user_profile["surname"]
            refs_list = []
            components_list_js = ndb_pb.getComponents()
            components_list = json.loads(components_list_js)
            for comp in components_list["data"]:
              ident = comp["component_id"]
              component = ndb_pb.getComponentEntity(ident)
              version = component.version
              static = "/"
              if str(ident) == "twitter-timeline": static = "/static/"
              ref = "/bower_components/" + \
                    str(ident) + "-" + str(version) + static + str(ident) + ".html"
              refs_list.append(ref)
            user_info["references"] = refs_list
            self.response.content_type = "application/json"
            self.response.write(json.dumps(user_info))
            self.response.set_status(200)
          else:
            user_dict = {"user_id": user_info["user_id"],
                          "description": user_info["description"],
                          "image": user_info["image"],
                          "website": user_info["website"],
                          "networks": user_info["nets"],
                          "components": user_info["components"],
                          "age": "",
                          "studies": "",
                          "tech_exp": "",
                          "social_nets_use": "",
                          "gender": ""}
            if user_info["private_email"] == False:
              user_dict["email"] = user_info["email"]
            if user_info["private_phone"] == False:
              user_dict["phone"] = user_info["phone"]
            for comp in user_info.components:
              dict_comp = json.loads(comp)
              ident = dict_comp["component_id"]
              preversion = ndb_pb.getComponentEntity(comp["component_id"])
              version = preversion.version
              static = "/"
              if ident == "twitter-timeline": static = "/static/"
              ref = "/bower_components/" + \
                    ident + "-" + version + static + ident + ".html"
              refs_list.append(ref)
            user_dict["references"] = refs_list
            self.response.content_type = "application/json"
            self.response.write(json.dumps(user_dict))
            self.response.set_status(200)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)

        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    
    # If the request doesn't come along a cookie, we search for the user_id in the system
    # (We only return an object verifying that the user_id requested exists in the system)
    else:
      self.response.content_type = "application/json"
      user = ndb_pb.getUser(user_id)
      if not user == None:
        self.response.set_status(200)
      else:
        self.response.write(json.dumps({"error": "User not found in the system"}))
        self.response.set_status(404)


  def post(self, user_id):
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        user_logged_id = ndb_pb.getUserId(user_logged_key)
        user_info = ndb_pb.getUser(user_id)
        # Checks if the user active is the owner of the resource (if exists)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "The user requested does not exist"}))
          self.response.set_status(404)
        elif not user_info == None and user_logged_id==user_id: 
          values = self.request.POST
          # Dict that contains the user values and fields to be updated
          update_data = {}

          # We parse the data received in the request
          if values.has_key("description"):
            update_data["description"] = values.get("description")
          if values.has_key("website"):
            update_data["website"] = values.get("website")
          if values.has_key("image"):
            update_data["image"] = values.get("image")
          if values.has_key("phone"):
            update_data["phone"] = int(values.get("phone"))
          if values.has_key("email"):
            update_data["email"] = values.get("email")
          if values.has_key("private_phone"):
            # Checks if private_phone has a proper value
            if values.get("private_phone") in ["True", "true"]:
              private_phone = True
              update_data["private_phone"] = private_phone
            elif values.get("private_phone") in ["False", "false"]:
              private_phone = False
              update_data["private_phone"] = private_phone
          if values.has_key("private_email"):
             # Checks if private_email has a proper value
            if values.get("private_email") in ["True", "true"]:
              private_email = True
              update_data["private_email"] = private_email
            elif values.get("private_email")in ["False", "false"]:
              private_email = False
              update_data["private_email"] = private_email
          if values.has_key("component"):
            component_id = values.get("component")      
            component = ndb_pb.getComponent(user_logged_key, component_id)
            # If the component_id provided in the request exists in the system and the user has not added it previously,
            # we add the component_id provided to the list of user's data to be updated
            if not component == None:
              update_data["component"] = component_id
          
          # Updates the resource and return the proper response to the client
          if not len(update_data) == 0:
            updated_info = ndb_pb.updateUser(user_logged_key, update_data)    
            if not len(updated_info) == 0:
              self.response.content_type = "application/json"
              self.response.write(json.dumps({"details": "The update has been successfully executed", "status": "Updated", "updated": update_data.keys()}))
              self.response.set_status(200)
            # We return a custom error message if the request had as purpose adding a component to the user's dashboard
            elif len(updated_info) == 0:
              self.response.content_type = "application/json"
              self.response.set_status(304)   
              if update_data.has_key("component_id"):
                self.response.write(json.dumps({"details": "Resource not modified (The component specified does not exists" + 
                  "or the user has not added to its account the social networks that consumes the component)", "status": "Not Modified"}))
              else:
                self.response.write(json.dumps({"details": "Resource not modified (check parameters and values provided)", "status": "Not Modified"}))
          else:
            self.response.content_type = "application/json"
            self.response.write(json.dumps({"details": "Resource not modified (It hasn't been specified any valid parameter for this method)",
             "status": "Not Modified"}))
            self.response.set_status(304) 
        
        # Status errors related to permission and user authentication
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "You don\"t have the proper rights to modify this resource" +
            " (The cookie session header does not match with the resource requested)"}))
          self.response.set_status(401)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)

        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)
  

  def delete(self, user_id):
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        user_logged_id = ndb_pb.getUserId(user_logged_key)
        # It is neccesary to get the parameters from the request
        user_info = ndb_pb.getUser(user_id)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "The user requested does not exist"}))
          self.response.set_status(404)
        elif not user_info == None and user_logged_id == user_id:
          # Logout of the user in the system
          logout_status = self.logout(cookie_value)
          # Invalidates the cookie
          self.response.delete_cookie("session")

          # Deletes the user from the datastore
          ndb_pb.deleteUser(user_logged_key)
          
          # Builds the response
          self.response.set_status(204)
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "You do not have the proper rights to delete this resource" +
          " (The cookie session header does not match with the resource requested)"}))
          self.response.set_status(401)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)

class ProfileHandler(SessionHandler):

  """
      Class that defines the user resource
      It acts as the handler of the /usuarios/{user_id}/profile resource
      Methods:
      post -- Modifies the info related to an user profile
  """

  def post(self, user_id):
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        users_logged_id = ndb_pb.getUserId(user_logged_key)
        user_info = ndb_pb.getUser(user_id)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write({"error": "The requested user does not exist"})
          self.response.set_status(404)
        elif not user_info == None and user_info == user_id:
          values = self.request.POST
          # Dictionary in which the updated data will be stored
          updated_data = {}

          if values.hasKey("age"):
            updated_data["age"] = int(values.get("age"))
          if values.hasKey("studies"):
            updated_data["studies"] = values.get("studies")
          if values.hasKey("tech_exp"):
            updated_data["tech_exp"] = values.get("tech_exp")
          if values.hasKey("social_nets_use"):
            updated_data["social_nets_use"] = values.get("social_nets_use")
          if values.hasKey("gender"):
            updated_data["gender"] = values.get("gender")
          if values.hasKey("name"):
            updated_data["name"] = values.get("name")
          if values.hasKey("surname"):
            updated_data["surname"] = values.get("surname")

          if not len(updated_data) == 0:
            updated_info = ndb_pb.updateProfile(user_id, updated_data)
            if not len(updated_info) == 0:
              self.response.content_type = "application/json"
              self.response.write(json.dumps({"details": "The update has been successfully executed", "status": "Updated", "updated": update_data.keys()}))
              self.response.set_status(200)
            else:
              self.response.content_type = "application/json"
              self.response.write(json.dumps({"details": "Resource not modified (check parameters and values provided)", "status": "Not Modified"}))
              self.set_status(304)
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "You don\"t have the proper rights to modify this resource" +
            " (The cookie session header does not match with the resource requested)"}))
          self.response.set_status(401)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)

        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)

class UserCredentialsHandler(SessionHandler):

  """
      Class that defines the user credentials resource
      It acts as the handler of the /usuarios/{user_id}/credentials resource
      Methods:
      get -- Gets the info about a user credentials
  """

  def get(self, user_id):
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        user_logged_id = ndb_pb.getUserId(user_logged_key)
        user_info = ndb_pb.getUser(user_id)
        # Checks if the user active is the owner of the resource (if exists)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "The user requested does not exist"}))
          self.response.set_status(404)
        elif not user_info == None and user_logged_key == user_id:
          cred_info = ndb_pb.getUserTokens(user_id)
          if cred_info == None:
            self.response.content_type = "application/json"
            self.response.write(json.dumps({"error": "The user has not credentials added to his profile"}))
            self.response.set_status(404)
          else:
            self.response.content_type = "application/json"
            self.response.write(cred_info)
            self.response.set_status(200)
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "You don\"t have the proper rights to modify this resource" +
            " (The cookie session header does not match with the resource requested)"}))
          self.response.set_status(401)
      else:
        # We invalidate the session cookies received
        expire_date = datetime.datetime(1970,1,1,0,0,0)
        self.response.set_cookie("session", "",
            path="/", domain=domain, secure=True, expires=expire_date)
        # We delete and invalidate other cookies received, like the user logged nickname
        # and social network in which the user performed the login
        if not self.request.cookies.get("social_network") == None:
            self.response.set_cookie("social_network", "",
                path="/", domain=domain, secure=True, expires=expire_date)
        if not self.request.cookies.get("user") == None:
            self.response.set_cookie("user", "",
                path="/", domain=domain, secure=True, expires=expire_date)

        # Builds the response
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)
