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
        self.response.content_type = "application/json"
        self.response.write(json.dupms({"error": "The session cookie header does not belong to an active user in the system"}))
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
    cookie_value = self.request.cookies.get("session")
    if not cookie_value == None:
      # Obtains info related to the user authenticated in the system
      user_logged_key = self.getUserInfo(cookie_value)
      if not user_logged_key == None:
        # Obtains the info related to the resource requested
        user_info = ndb_pb.getUser(user_id)
        if user_info == None:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "The user requested does not exist"}))
          self.response.set_status(404)
        else:
          # Obtains the user_id to check if the user active is the resource owner
          user_logged_id = ndb_pb.getUserId(user_logged_key)
          # Depending on the user making the request, the info returned will be one or another
          if user_id == user_logged_id:
            self.response.content_type = "application/json"
            self.response.write(json.dumps(user_info))
            self.response.set_status(200)
          else:
            user_dict = {"user_id": user_info["user_id"],
                          "description": user_info["description"],
                          "image": user_info["image"],
                          "website": user_info["website"],
                          "nets": user_info["nets"],
                          "components": user_info["components"]}
            if user_info["private_email"] == False:
              user_dict["email"] = user_info["email"]
            if user_info["private_phone"] == False:
              user_dict["phone"] = user_info["phone"]
            self.response.content_type = "application/json"
            self.response.write(json.dumps(user_dict))
            self.response.set_status(200)
      else:
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    
    # If the request doesn't come along a cookie, we search for the user_id in the system
    # (We only return an object verifying that the user_id requested exists in the system)
    else:
      self.response.content_type = "application/json"
      user = ndb_pb.getUser(user_id)
      if not user == None:
        self.response.write(json.dumps({"user_id": user["user_id"]}))
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
          if values.has_key("web_site"):
            update_data["web_site"] = values.get("web_site")
          if values.has_key("image"):
            update_data["image"] = values.get("image")
          if values.has_key("phone"):
            update_data["phone"] = int(values.get("phone"))
          if values.has_key("email"):
            update_data["email"] = values.get("email")
          if values.has_key("private_phone"):
            # Checks if private_phone has a proper value
            if values.get("private_phone") == "True":
              private_phone = True
              update_data["private_phone"] = private_phone
            elif values.get("private_phone") == "False":
              private_phone = False
              update_data["private_phone"] = private_phone
          if values.has_key("private_email"):
             # Checks if private_email has a proper value
            if values.get("private_email") == "True":
              private_email = True
              update_data["private_email"] = private_email
            elif values.get("private_email") == "False":
              private_email = False
              update_data["private_email"] = private_email
          if values.has_key("component"):
            component_id = values.get("component")      
            component = ndb_pb.getComponent(user_info, component_id)
            if not component == None:
              update_data["component"] = component_id
          
          # Updates the resource 
          if not len(update_data) == 0:
            user_info = ndb_pb.updateUser(user_logged_key, update_data)
            self.response.content_type = "application/json"
            self.response.write(json.dumps({"success": "The update has been successfully executed", "status": "Updated", "updated": update_data.keys()}))
            self.response.set_status(200)
          else:
            self.response.content_type = "application/json"
            self.response.write(json.dumps({"success": "Resource not modified (check parameters and values provided)", "status": "Not Modified"}))
            self.response.set_status(200) 
        else:
          self.response.content_type = "application/json"
          self.response.write(json.dumps({"error": "You don\"t have the proper rights to modify this resource" +
            " (The cookie session header does not match with the resource requested)"}))
          self.response.set_status(401)
      else:
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
        self.response.content_type = "application/json"
        self.response.write(json.dumps({"error": "The session cookie header does not belong to an active user in the system"}))
        self.response.set_status(400)
    else:
      self.response.content_type = "application/json"
      self.response.write(json.dumps({"error": "The user is not authenticated"}))
      self.response.set_status(401)
