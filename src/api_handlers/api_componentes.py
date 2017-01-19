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
import string
import json

import ndb_pb
from api_oauth import SessionHandler

# import cliente_gitHub

# Import config vars and datetime package (to manage request/response cookies)
import datetime, os, yaml, json
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

domain = cfg["domain"]


social_list = ["twitter", "facebook", "stackoverflow", "instagram", "linkedin", "googleplus", "github", "pinterest", ""]

class ComponentRatingHandler(SessionHandler):
    """
    Class that defines the method related to user rating about a certain component
    in the system (componentes/:idComponente/componenteValorado)
    Methods:
        post -
    """
    # POST Method
    def post(self, component_id):
        """ - Modifies the info about a component
        Keyword arguments:
        self -- info about the request build by webapp2
        component_id -- path url directory corresponding to the component id
        """
        # Get the cookie in the request
        cookie_value = self.request.cookies.get("session")
        # Param Methods
        version = self.request.get("version", default_value="none")
        rate = self.request.get("rate", default_value="none")
        optional_form_completed = self.request.get("optional_form_completed", default_value="false")
        if not cookie_value == None:
            # Checks whether the cookie belongs to an active user and the request has provided at least one param
            user_id = self.getUserInfo(cookie_value)
            if not user_id == None:
                # TODO: Data params validation
                # We compose the data to be updated
                data = []
                data["comp_name"] = component_id
                data["rate"] = rate
                data["optional_evaluation"] = True if optional_form_completed == "true" else False
                # We update the user info
                updated_data = ndb_pb.updateUser(user_id, data)
                if not updated_data == None:
                    self.response.set_status(200)
                else:
                    self.response.set_status(304)
            else:
                # We invalidate the session cookie received
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

                # We write in the response details about the error
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)



class ComponentListHandler(SessionHandler):

    """
    Class that defines the component list resource.
    It acts as the handler of the /components resource

    Methods:
    get -- Gets a filtered list of the components stored in the system
    put -- Uploads a component
    """

    # GET Method
    def get(self):
        """ Gets a filtered list of the components stored in the system
        Keyword arguments:
        self -- info about the request build by webapp2
        """
        # Get the cookies in the request
        cookie_value = self.request.cookies.get("session")

        # Social_network,filter_param and list_format are optional params
        social_network = self.request.get("social_network", default_value="")
        filter_param = self.request.get("filter",default_value="general")
        list_format = self.request.get("list_format", default_value="reduced")

        # Lists of posible values for each param
        filter_list = ["general","user"]
        format_list = ["complete","reduced"]
        if not cookie_value == None:
            user_id = self.getUserInfo(cookie_value)
            if not user_id == None:
                if social_network in social_list  or social_network == "" and filter_param in filter_list and list_format in format_list:
                    format_flag = True if list_format == "complete" and filter_param == "user" else False
                    user_filter = True if filter_param == "user" else False
                    # Get the component list, according to the filters given
                    component_list = ndb_pb.getComponents(user_id, social_network, format_flag, user_filter)
                    component_list_aux = json.loads(component_list)
                    if not len(component_list_aux["data"]) == 0:
                        self.response.content_type = "application/json"
                        self.response.write(component_list)
                        self.response.set_status(200)
                    else:
                        self.response.set_status(204)
                else:
                    response = \
                    {"error": "Invalid value for param social_network, filter o list_format"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                # We invalidate the session cookie received
                expire_date = datetime.datetime(1970,1,1,0,0,0)
                self.response.set_cookie("session", "",
                    path="/", domain=domain, secure=True, expires=expire_date)
                # We delete and invalidate other cookies received, like the user logged nickname
                # and social network in which performed the login
                if not self.request.cookies.get("social_network") == None:
                    self.response.set_cookie("social_network", "",
                        path="/", domain=domain, secure=True, expires=expire_date)
                if not self.request.cookies.get("user") == None:
                    self.response.set_cookie("user", "",
                        path="/", domain=domain, secure=True, expires=expire_date)

                # Response to the client
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


    # PUT Method
    def put(self):
        """ Uploads a component. The component is stored in the Datastore of the application
        This request does not need to be made along with a cookie identifying the session
        Keyword arguments:
        self -- info about the request build by webapp2
        """
        try:
            # Get the request POST params
            url = self.request.POST["url"] # Url to the component stable repo
            component_id = self.request.POST["component_id"]
            description = self.request.POST["description"]
            social_network = self.request.POST["social_network"]
            input_type = self.request.POST.getall("input_type")
            output_type = self.request.POST.getall("output_type")
            version_list = self.request.POST.getall("versions")
            attributes = self.request.POST["attributes"]
            # endpoint = ""
            # component_directory = ""
            # api_key = ""
            # if self.request.POST.has_key("endpoint"):
            #     endpoint = self.request.POST["endpoint"]
            # if self.request.POST.has_key("component_directory"):
            #     component_directory = self.request.POST["component_directory"]
            # if self.request.POST.has_key("api_key"):
            #     api_key = self.request.POST["api_key"]

            # Predetermined is an optional param (default_value=False)
            predetermined = None
            if self.request.POST.has_key("predetermined"):
                if self.request.POST["predetermined"] in ["True","true"]:
                    predetermined = True
                elif self.request.POST["predetermined"] in ["False","false"]:
                    predetermined = False
            else:
                predetermined = False
            # We check if the social network param has a proper value
            if social_network in social_list:
                # We check if the request has provided at least the version "stable" for the version_list param
                if "stable" in version_list:
                    # We check if "predetermined" has a boolean value
                    if not predetermined == None: #isinstance(predetermined,bool):
                        # We check if the component exists in our system
                        component_stored = ndb_pb.searchComponent(component_id)
                        if component_stored == None:
                            # print "=========================="
                            # print "Voy a insertar el componente de " + social_network
                            # print "=========================="
                            # Adds the component to datastore
                            ndb_pb.insertComponent(component_id, url=url, description=description, rs=social_network, input_t=input_type, output_t=output_type, 
                                                    version_list=version_list, predetermined=predetermined, attributes=attributes)
                            response = {"status": "Component uploaded succesfully"}
                            self.response.write(json.dumps(response))
                            self.response.set_status(201)
                        else:
                            self.response.set_status(403)
                    else:
                        response = {"error": "Bad value for 'predetermined' param (it must be 'True' or 'False')"}
                        self.response.write(json.dumps(response))
                        self.response.set_status(400)
                else:
                    response = {"error": "The versions param must contains stable as one of its values"}
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                response = {"error": "Bad value for the social_network param"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)

        except KeyError:
            response = {"error": "Missing params in the request body"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)

class ComponentHandler(SessionHandler):
    """
    Class that defines the component resource
    It acts as the handler of the /components/{component_id} resource
    Methods:
    get -- Gets the info about a component
    post -- Modifies the info about a component
    delete -- Deletes a component in the system
    """

    # GET Method
    def get(self, component_id):
        """ Gets the info about a component or
        gets a filtered list of the components stored in the system
        Keyword arguments:
        self -- info about the request build by webapp2
        component_id -- path url directory corresponding to the component id
        """
        # Get the cookie in the request
        cookie_value = self.request.cookies.get("session")
        # Format is an optional param
        format = self.request.get("format", default_value="reduced")
        if not cookie_value == None:
            user_id = self.getUserInfo(cookie_value)
            if not user_id == None:
                if format == "reduced" or format == "complete":
                    format_flag = True if format == "complete" else False
                    component = ndb_pb.getComponent(user_id, component_id, format_flag)
                    if not component == None:
                        comp_aux = json.load(component)
                        comp_aux["ref"] = "centauro.ls.fi.upm.es/bower_components/" + comp_aux["component_id"] + "-" + comp_aux["version"]
                        component = json.dumps(comp_aux)
                        self.response.content_type = "application/json"
                        self.response.write(component)
                        self.response.set_status(200)
                    else:
                        response = \
                        {"error": "Component not found in the system"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(404)
                else:
                    response = \
                    {"error": "The format param provided is incorrect"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                # We invalidate the session cookie received
                expire_date = datetime.datetime(1970,1,1,0,0,0)
                self.response.set_cookie("session", "",
                    path="/", domain=domain, secure=True, expires=expire_date)
                # We delete and invalidate other cookies received, like the user logged nickname
                # and social network in which performed the login
                if not self.request.cookies.get("social_network") == None:
                    self.response.set_cookie("social_network", "",
                        path="/", domain=domain, secure=True, expires=expire_date)
                if not self.request.cookies.get("user") == None:
                    self.response.set_cookie("user", "",
                        path="/", domain=domain, secure=True, expires=expire_date)

                # We write the response providing details about the error
                response = \
                    {"error": "The session cookie provided is incorrect"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


    # POST Method
    def post(self, component_id):
        """ - Modifies the info about a component
        Keyword arguments:
        self -- info about the request build by webapp2
        component_id -- path url directory corresponding to the component id
        """
        # Get the cookie in the request
        cookie_value = self.request.cookies.get("session")
        # Rating, x_axis, y_axis are optional params
        rating = self.request.get("rating", default_value="none")
        x_axis = self.request.get("x_axis", default_value="none")
        y_axis = self.request.get("y_axis", default_value="none")
        listening = self.request.get("listening", default_value="none")
        if not cookie_value == None:
            # Checks whether the cookie belongs to an active user and the request has provided at least one param
            user_id = self.getUserInfo(cookie_value)
            if not user_id == None:
                data = {}
                component_modified_success = False
                rating_error = False
                # We get the data from the request
                try:
                    if not rating == "none":
                        rating_value = float(rating)
                    if not x_axis == "none":
                        data["x"] = float(x_axis)
                    if not y_axis == "none":
                        data["y"] = float(y_axis)
                    if not listening == "none":
                        data["listening"] = listening

                except ValueError:
                    response = \
                    {"error": "x_axis, y_axis and rating must have a numeric value"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)

                # Updates the component rating
                if not rating == "none":
                    if rating_value > 0 and rating_value < 5:
                        rating_updated = ndb_pb.addRate(user_id, component_id, rating_value)
                        if not rating_updated:
                            rating_error = True
                            response = {"error": "The component_id specified does not belong to the user dashboard"}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(400)
                        else:
                            component_modified_success = True
                    else:
                        rating_error = True
                        response = \
                        {"error": "Rating must be a numeric value between 0.0 and 5.0"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(400)

                # Updates the info about the component
                if not len(data) == 0 and not rating_error:
                    ndb_pb.modifyUserComponent(user_id, component_id, data)
                    component_modified_success = True

                # Compounds the success response if the component has ben updated successfully
                if component_modified_success:
                    response = {"status": "Component updated succesfully"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(200)
            else:
                # We invalidate the session cookie received
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

                # We write in the response details about the error
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


    # DELETE Method
    def delete(self, component_id):
        """ - Deletes a component in the system
        Keyword arguments:
        self -- info about the request build by webapp2
        component_id -- path url directory corresponding to the component id
        """
        scope = self.request.get("scope", default_value="user")
        cookie_value = self.request.cookies.get("session")

        if scope=="user":
            if not cookie_value == None:
                user_logged_key = self.getUserInfo(cookie_value)
                if not user_logged_key == None:
                    deactivated = ndb_pb.deactivateUserComponent(user_logged_key, component_id)
                    if deactivated:
                        response = {"status": "Component deleted succesfully"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(200)
                    else:
                        response = {"error": "The component does not correspond to the user's dashboard"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(404)
                else:
                    # We invalidate the session cookie received
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

                    self.response.content_type = "application/json"
                    response = {"error": "The session cookie header does not belong to an active user in the system"}
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                self.response.content_type = "application/json"
                self.response.write(json.dumps({"error": "To perform this action, you must be authenticated"}))
                self.response.set_status(401)
        elif scope=="global":
            # Deletes the component in the datastore
            deleted = ndb_pb.deleteComponent(component_id)
            if deleted:
                response = {"status": "Component deleted succesfully"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(204)
            else:
                response = {"error": "Component not found in the system"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(404)
        else:
            response = {"error": "Bad value for the scope params"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)
