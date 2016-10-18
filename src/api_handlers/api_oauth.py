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
import json
import os
import yaml
import httplib
import hashlib
import urllib
from google.appengine.ext import ndb
from google.appengine.api import memcache
import time
import ndb_pb
from ndb_pb import Token, User
import datetime
import logging

# Imports for TwitterHandler
import oauth
from google.appengine.api import channel

# Import config vars
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

domain = cfg["domain"]

client = None

# Configuration params in order to perform the request to Twitter
consumer_key = "tuprQMrGCdGyz7QDVKdemEWXl"
consumer_secret = \
    "byQEyUYKZm1R7ZatsSWoFLX0lYn8hRONBU4AAyGLFRDWVg7rzm"
request_token_url = \
    "https://api.twitter.com/oauth/request_token"
base_authorization_url = \
    "https://api.twitter.com/oauth/authorize"
callback_uri = "https://" + domain \
    + "/api/oauth/twitter/authorization"
# Request to Twitter the request_token and authorization URL
client = oauth.TwitterClient(consumer_key, consumer_secret,
        callback_uri)

# Generic handlers for the session management, login, logout and actions
# related to user credentials
class SessionHandler(webapp2.RequestHandler):
    """
    Class that handles the session of the application
    Methods:
        login - Generates a valid hash for a given user_key
        getUserInfo - Gets the info related to a logged user_id
        logout - Deletes the session for a given user
    """

    def login(self, user_key):
        message = str(user_key.id()) + str(time.time())
        cypher = hashlib.sha256(message)
        hash_id = cypher.hexdigest()
        # Store in memcache hash-user_id pair
        # memcache.add(hash_id, user_key)
        # Create a new session in the system
        ndb_pb.createSession(user_key, hash_id)
        return hash_id

    def getUserInfo(self, hashed_id):
        # user = memcache.get(hashed_id)
        user_key = ndb_pb.getSessionOwner(hashed_id)
        return user_key

    def logout(self, hashed_id):
        logout_status = False
        # status = memcache.delete(hashed_id)
        status = ndb_pb.deleteSession(hashed_id)
        if status == 2:
            logout_status = True
        return logout_status


class OauthSignUpHandler(SessionHandler):
    """ Defines the logic for the signup action, in those social networks that
        act as authentication services in PicBit, and have
        a client authorization flow (for example, GooglePlus or Facebook)
        Methods:
            post_signup - Implements the signup action. Stores the pair of
            token_in and access_token in the system, and generates the
            cookie for the session.
    """
    def post_signup(self, social_network):
        try:
            # We get the params from the POST data
            access_token = self.request.POST["access_token"]
            token_id = self.request.POST["token_id"]
            user_identifier = self.request.POST["user_identifier"]
            # Checks if the username was stored previously
            logging.info('access_token: ' +access_token)
            logging.info('token_id: ' +token_id)
            logging.info('user_identifier: ' +user_identifier)
            stored_credentials = ndb_pb.searchToken(token_id, social_network)
            if stored_credentials == None: # Not found
                user_data = {}
                user_id_repeated = True if not ndb_pb.getUser(user_identifier) == None else False
                if not user_id_repeated:
                    user_data["user_id"] = user_identifier
                    # Generate a valid username for a new user
                    user_key = ndb_pb.insertUser(social_network,
                            token_id, access_token, user_data)
                    # Creates the session
                    session_id = self.login(user_key)

                    # Returns the session, user_id and social_network cookie
                    self.response.set_cookie("session", session_id,
                            path="/", domain=domain, secure=True)
                    self.response.set_cookie("social_network", social_network,
                            path="/", domain=domain, secure=True)
                    self.response.set_cookie("user", user_identifier,
                            path="/", domain=domain, secure=True)

                    # Builds the response
                    response = {"status": "User logged successfully", "user_id": user_identifier}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(201)
                else:
                    response = {"error": "The user_identifier provided for the sign up has been already taken"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                response = \
                {"error": "The token_id provided belong to a registered user in the system. Consider perform a login request instead"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        except KeyError:
            response = \
                {"error": "You must provide access_token, token_id and user_identifier params in the request"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OauthLoginHandler(SessionHandler):
    """ Defines the logic for the login action, in those social networks that
        act as authentication services in PicBit, and have
        a client authorization flow (for example, GooglePlus or Facebook)
        Methods:
            post_login - Implements the login action. Updates the
            access_token for a given user in the system, and generates the
            cookie for the session.
    """
    def post_login(self, social_network):
        try:
            # We get the params from the POST data
            access_token = self.request.POST["access_token"]
            token_id = self.request.POST["token_id"]

            # Checks if the username was stored previously
            stored_credentials = ndb_pb.searchToken(token_id,
                    social_network)
            if not stored_credentials == None:
                # We store the new set of credentials
                user_key = ndb_pb.modifyToken(token_id,
                        access_token, social_network)
                user_id = ndb_pb.getUserId(user_key)
                session_id = self.login(user_key)

                # Gets the user_id to generate the user cookie
                user_id = ndb_pb.getUserId(user_key)
                # Returns the session cookie
                self.response.set_cookie("session", session_id, path="/", domain=domain, secure=True)
                self.response.set_cookie("social_network", social_network, path="/", domain=domain, secure=True)
                self.response.set_cookie("user", user_id, path="/", domain=domain, secure=True)

                # Builds the response
                response = {"status": "User logged successfully", "user_id": user_id}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                response = \
                {"error": "The token_id provided does not belong to any user in the system. Consider perform a signup request instead"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        except KeyError:
            response = \
                {"error": "You must provide a valid pair of access_token and token_id in the request"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OauthLogoutHandler(SessionHandler):
    """ Defines the logic for the logout action, in those social networks that
        act as authentication services in PicBit, and have
        a client authorization flow (for example, GooglePlus or Facebook)
        Methods:
            post_logout - Implements the logout action. Invalidates the
            cookie for the session.
    """
    def post_logout(self, social_network):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            # We get the user_id to check if the user is logged in the system
            user_id = self.getUserInfo(cookie_value)
            if not user_id == None:
                # Logout
                logout_status = self.logout(cookie_value)
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
                response = \
                {"error": "The cookie session provided does not belongs to any active user. The logout action was not performed"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)

        else:
            response = \
                {"error": "This request requires a secure_cookie with the session identifier"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


class OauthCredentialsHandler(SessionHandler):
    def get_credentials(self, social_network, token_id):
        cookie_value = self.request.cookies.get("session")
        # Obtains info related to the user authenticated in the system
        if not cookie_value == None:
            logged_user = self.getUserInfo(cookie_value)
            # Searchs for user"s credentials
            if not logged_user == None:
                # Obtains user info
                logged_user_id = ndb_pb.getUserId(logged_user)

                # Obtains user credentials
                user_credentials = ndb_pb.getToken(token_id, social_network)
                if not user_credentials == None:
                    if user_credentials["user_id"] == logged_user_id:
                        response = \
                            {"user_id": user_credentials["user_id"],
                            "access_token": user_credentials["token"],
                            "token_id": user_credentials["token_id"]}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(200)
                    else:
                        response = {"user_id": user_credentials["user_id"]}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(200)
                else:
                    response = \
                        {"error": "The active user does not have a pair of token_id" \
                         + " and access_token in " + social_network + " stored in the system"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(404)
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
                response = \
                {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)

        # If we don't provide a cookie in the request, we search for the token in the system
        # and return a 200 o 404 status. It is a request included in the login flow of the system
        else:
            user_credentials = ndb_pb.getToken(token_id,social_network)
            if not user_credentials == None:
                response = {"user_id": user_credentials["user_id"]}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                response =  {"error": "Token not found in the system"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(404)


    def delete_credentials(self, social_network, token_id):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            # Searchs for user"s credentials
            logged_user_key = self.getUserInfo(cookie_value)
            if not logged_user_key == None:
                logged_user_id = ndb_pb.getUserId(logged_user_key)
                token = ndb_pb.getToken(token_id, social_network)
                if not token == None:
                    token_owner_id = token['user_id']
                    if logged_user_id == token_owner_id:
                        # Deletes the token from the user
                        token_deleted = ndb_pb.deleteCredentials(logged_user_key, social_network, token_id)
                        if token_deleted:
                            response = \
                                {"status": "Credentials deleted successfully"}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(204)
                        else:
                            response = \
                                {"error": "This token cannot be deleted, because it is being used as the only token " + \
                                 "to perform the login action in the system"}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(403)
                    else:
                        response = \
                            {"error": "You do not have permissions to perform this request"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(401)
                else:
                    response = \
                            {"error": "Token not found in the system"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(404)
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

class OAuthCredentialProviderHandler(OauthCredentialsHandler):

    def update_credentials(self, social_network, token_id):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            user = self.getUserInfo(cookie_value)
            if not user == None:
                logged_user_id = ndb_pb.getUserId(user)
                try:
                    # Gets the data from the request form
                    access_token = self.request.POST["access_token"]

                    # Checks if the username was stored previously
                    stored_credentials = ndb_pb.getToken(token_id,
                            social_network)
                    if not stored_credentials == None:
                        token_owner_id = stored_credentials['user_id']
                        if token_owner_id == logged_user_id:
                            # We update the user credentials
                            user_id = ndb_pb.modifyToken(token_id, access_token,
                                    social_network)
                            # Builds the response
                            response = {"user_id": stored_credentials["user_id"]}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(200)
                        else:
                            response = \
                            {"error": "You don't have the proper rights to perform this action"}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(403)
                    else:
                        response = \
                        {"error": "Credentials not found in the system"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(404)
                except KeyError:
                    response = \
                        {"error": "You must provide a valid pair of access_token and token_id in the request"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
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
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = \
                {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


class OAuthCredentialsContainerHandler(SessionHandler):
    def put_credentials(self, social_network):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            user = self.getUserInfo(cookie_value)
            if not user == None:
                try:
                    # Gets the data from the request form
                    access_token = self.request.POST["access_token"]
                    token_id = self.request.POST["token_id"]

                    # Checks if the username was stored previously
                    stored_credentials = ndb_pb.getToken(token_id,
                            social_network)
                    if stored_credentials == None:
                        # Adds the token to the user credentials list
                        ndb_pb.insertToken(user, social_network, access_token, token_id)
                        #Builds the response
                        user_id = ndb_pb.getUserId(user)
                        response = {"user_id": user_id}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(201)
                    else:
                        response = \
                        {"error": "This set of credentials already exists in the system"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(400)
                except KeyError:
                    response = \
                        {"error": "You must provide a valid pair of access_token and token_id in the request"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
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
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = \
                {"error": "You must provide a session cookie"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


##################################################################################
# HANDLERS MAPPERS / IMPLEMENTATIONS FOR EACH SOCIAL NETWORK SUPPORTED IN PICBIT
##################################################################################

# HANDLERS FOR RESOURCES RELATED TO FACEBOOK
class FacebookHandler(OauthCredentialsHandler):
    """
    Class that represents the Facebook token resource.
    Methods:
        get -- Returns the Facebook access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Facebook for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("facebook", token_id)

    def delete(self, token_id):
        self.delete_credentials("facebook", token_id)

class FacebookLoginHandler(OauthLoginHandler):
    """ This class is a resource that represents the login
    action using the Facebook credentials to autenticate in PicBit
    """
    def post(self):
        self.post_login("facebook")

class FacebookSignUpHandler(OauthSignUpHandler):
    """ This class is a resource that represents the sign-up
    action using the Facebook credentials to autenticate in PicBit
    """
    def post(self):
        self.post_signup("facebook")

class FacebookLogoutHandler(OauthLogoutHandler):
    """ This class is a resource that represents the logout
    action using the Facebook credentials to autenticate in PicBit
    """
    def post(self):
        self.post_logout("facebook")

class FacebookCredentialsHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Facebook credentials resource.
    Methods:
        put -- Adds a new set of credentials (token_id and access_token in Facebook)
    """
    def put(self):
        self.put_credentials("facebook")

# HANDLERS FOR RESOURCES RELATED TO GITHUB
class GitHubCredentialHandler(OAuthCredentialProviderHandler):
    """
    Class that represents the GitHub token resource.
    Methods:
        get -- Returns the GitHub access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in GitHub for the user authenticated
        post -- Updates the pair of token_id and access_token in
                GitHub for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("github", token_id)

    def delete(self, token_id):
        self.delete_credentials("github", token_id)

    def post(self,token_id):
        self.update_credentials("github", token_id)

class GitHubContainerHandler(webapp2.RequestHandler):
    """
    Class that represents the List of Github credentials resource.
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in GitHub)
    """
    def post(self):
        # tok1 = "80dbc6c5b"
        # tok2 = "35c8ee515"
        # tok3 = "b8d18cc8a"
        # tok4 = "489646d3c"
        # tok5 = "8457"
        # git_tok = ndb_pb.GitHubAPIKey(token=tok1 + tok2 + tok3 + tok4 + tok5)
        # git_tok.put()
        url = "github.com"
        # authorize_url = \
        # "http://test-backend.example-project-13.appspot.com/api/oauth/github?action=request_token"
        access_token_url = "/login/oauth/access_token"
        client_id = "ae271d42c068cae023b9"
        client_secret = "7834524345411e5b112c9715949ba33861db61a4"
        access_token = ""
        print "=================================="
        print "Body de la peticion a Github"
        print self.request.body
        print "=================================="
        connection = httplib.HTTPSConnection(url)
        # Cogemos el codigo de la peticion
        try:
            body = json.loads(self.request.body)
            code = self.request.get('code')
            params_token = urllib.urlencode({"client_id": client_id,
                    "client_secret": client_secret, "code": code})
            # Realizamos la peticion en la conexion
            connection.request("POST", access_token_url, params_token)
            # Cogemos la respuesta de la peticion y realizamos un split
            # para coger el valor del token
            response_token = connection.getresponse()
            data_token = response_token.read()
            print "===========================================================" + data_token
            access_token = data_token.split("&")
            access_token = access_token[0].split("=")[1]
            logging.info('Ya tiene codigo: ' + access_token)
            # Gestion de la respuesta de webapp
            # self.response.content_type = "application/json"
            # response = {"token": "" + access_token + ""}
            # self.response.write(json.dumps(response))
            # connection.close()
            # self.response.set_status(200)

            # Obtenemos la informacion del usuario registrado para 
            # almacenar correctamente la informacion
           
            cookie_value = self.request.cookies.get("session")
            if not cookie_value == None:
                user = self.getUserInfo(cookie_value)
                if not user == None:
                    # Obtenemos los detalles del usuario autenticado
                    connectionAPI = httplib.HTTPSConnection("api.github.com")
                    headers = {"Accept": "application/vnd.github.v3+json",
                                "User-Agent": "PicBit-App",
                                "Authorization": "token " + ndb_pb.getGitHubAPIKey()}
                    connectionAPI.request("GET", "/user", urllib.urlencode({}), headers)
                    response = connectionAPI.getresponse()
                    aux = response.read()
                    user_details = json.loads(aux)
                    # Buscamos el par id usuario/token autenticado en la base
                    stored_credentials = ndb_pb.searchToken(str(user_details["login"
                            ]), "github")
                    response = {"token": access_token}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    if stored_credentials == None:
                        # Almacena las credenciales en una entidad Token
                        user_credentials = ndb_pb.insertToken(user, "github", access_token,
                                            user_details["login"])
                        self.response.set_status(201)
                    else:
                        # Almacenamos el access token recibido
                        user_id = ndb_pb.modifyToken(str(user_details["login"]),
                                access_token, "github")
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
                    response = \
                        {"error": "The cookie session provided does not belongs to any active user"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                response = \
                    {"error": "You must provide a session cookie"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(401)
        except KeyError:
            response = \
                {"error": "You must provide a valid code value in the request"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)

# HANDLERS FOR RESOURCES RELATED TO GOOGLEPLUS
class GooglePlusHandler(OauthCredentialsHandler):
    """
    Class that represents the GooglePlus token resource.
    Methods:
        get -- Returns the GooglePlus access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in GooglePlus for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("googleplus", token_id)

    def delete(self, token_id):
        self.delete_credentials("googleplus", token_id)

class GooglePlusLoginHandler(OauthLoginHandler):
    """ This class is a resource that represents the login
    action using the GooglePlus credentials to autenticate in PicBit
    """
    def post(self):
        self.post_login("googleplus")

class GooglePlusSignUpHandler(OauthSignUpHandler):
    """ This class is a resource that represents the sign-up
    action using the GooglePlus credentials to autenticate in PicBit
    """
    def post(self):
        self.post_signup("googleplus")

class GooglePlusLogoutHandler(OauthLogoutHandler):
    """ This class is a resource that represents the logout
    action using the GooglePlus credentials to autenticate in PicBit
    """
    def post(self):
        self.post_logout("googleplus")

class GooglePlusCredentialsHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Googleplus credentials resource.
    Methods:
        put -- Adds a new set of credentials (token_id and access_token in Googleplus)
    """
    def put(self):
        self.put_credentials("googleplus")

# HANDLERS FOR RESOURCES RELATED TO INSTAGRAM
class InstagramCredentialHandler(OAuthCredentialProviderHandler):
    """
    Class that represents the Instagram token resource.
    Methods:
        get -- Returns the Instagram access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Instagram for the user authenticated
        post -- Updates the pair of token_id and access_token in
                Instagram for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("instagram", token_id)

    def delete(self, token_id):
        self.delete_credentials("instagram", token_id)

    def post(self, token_id):
        self.update_credentials("instagram", token_id)

class InstagramContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Instagram credentials resource.
    Methods:
        put -- Adds a new set of credentials (token_id and access_token in Instagram)
    """
    def put(self):
        self.put_credentials("instagram")


# HANDLERS FOR RESOURCES RELATED TO LINKEDIN
class LinkedinCredentialHandler(OAuthCredentialProviderHandler):
    """
    Class that represents the Linkedin token resource.
    Methods:
        get -- Returns the Linkedin access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Linkedin for the user authenticated
        post -- Updates the pair of token_id and access_token in
                Linkedin for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("linkedin", token_id)

    def delete(self, token_id):
        self.delete_credentials("linkedin", token_id)

    def post(self, token_id):
        self.update_credentials("linkedin", token_id)

class LinkedinContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Linkedin credentials resource.
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in Linkedin)
    """
    def put(self):
        self.put_credentials("linkedin")


# HANDLERS FOR RESOURCES RELATED TO STACKOVERFLOW
class StackOverflowCredentialHandler(OAuthCredentialProviderHandler):
    """
    Class that represents the StackOverflow token resource.
    Methods:
        get -- Returns the StackOverflow access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in StackOverflow for the user authenticated
        post -- Updates the pair of token_id and access_token in
                StackOverflow for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("stackoverflow", token_id)

    def delete(self, token_id):
        self.delete_credentials("stackoverflow", token_id)

    def post(self,token_id):
        self.update_credentials("stackoverflow", token_id)

class StackOverflowContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Stackoverflow credentials resource.
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in Stackoverflow)
    """
    def put(self):
        self.put_credentials("stackoverflow")

# HANDLERS FOR RESOURCES RELATED TO TWITTER
# Handler that manages the first step in the Twitter login flow
# (obtain the request token and request url to initiate the login in client)
class TwitterRequestLoginHandler(webapp2.RequestHandler):
    """ This resource represents the first step in the Twitter
        login flow, in which the server must request to Twitter a
        request_token that identifies the login flow in a temporal way
        and provides the url in which the user must access and authorize
        the access of his/her credentials.
        It is the first step in a login flow of three steps.
        The second step is performed in frontend and the third step is a
        callback received from Twitter endpoint.
    """
    def get(self):
        global client
        """ Handles the first step in the Twitter login flow
        Keyword arguments:
        self -- info about the request build by webapp2
        """
        # Return the authorization URL
        self.response.content_type = "application/json"
        response = {"oauth_url": client.get_authorization_url()}
        self.response.write(json.dumps(response))


# Handler that manages the callback from Twitter as a final step of the oauth flow
class TwitterAuthorizationHandler(SessionHandler):
    """ This class is a resource that represents the authorization
        step in the Twitter Login flow, in which the Twitter Endpoint returns
        asyncronously the credentials for the user authenticated in the flow.
        It is the third step in a login flow of three steps.
    """

    def get(self):
        """ Manages the callback from Twitter in the Twitter oauth flow.
        Keyword arguments:
        self -- info about the request built by webapp2
        """
        # Gets the params in the request
        auth_token = self.request.get("oauth_token")
        oauth_verifier = self.request.get("oauth_verifier")
        # Retrieves user info
        user_info = client.get_user_info(auth_token,
                auth_verifier=oauth_verifier)
        # Stores in memcache the session id associated with the oauth_verifier
        #and data associated to the logged user
        key_verifier = "oauth_verifier_" + oauth_verifier
        data = {"token_id": user_info["username"],
                "access_token": user_info["token"]
                }
        memcache.add(key_verifier, data)

        # Set the status for the response
        self.response.set_status(200)

class TwitterAuthorizationDetailsHandler(webapp2.RequestHandler):
    def get(self, authorization_id):
        """Manages the info returned by the callback from Twitter
        Keyword arguments:
        self -- info about the request built by webapp2
        authorization_id -- oauth_verifier that defines the authorization flow
        """
        key_verifier = "oauth_verifier_" + authorization_id
        twitter_user_data = memcache.get(key_verifier)
        # Return the user's token id that authorized the application
        if not twitter_user_data == None:
            response = {"token_id": twitter_user_data["token_id"]}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(200)
        else:
            response = {"error": "The oauth_verifier provided does not correspond to an active authorization flow"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(404)

class TwitterHandler(OauthCredentialsHandler):
    """
    Class that represents the Twitter token resource.
    Methods:
        get -- Returns the Twitter access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Twitter for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("twitter", token_id)

    def delete(self, token_id):
        self.delete_credentials("twitter", token_id)

class TwitterCredentialsHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Twitter credentials resource.
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in Twitter)
    """
    def post(self):
        self.put_credentials("twitter")

class TwitterSignUpHandler(SessionHandler):
    """ This class is a resource that represents the sign-up
    action using the Twitter credentials to autenticate and
    create a new user into PicBit
    Methods:
        post -- Signs ups a user in the system
    """
    def post(self):
        oauth_verifier = self.request.get("oauth_verifier", default_value="None")
        user_identifier = self.request.get("user_identifier", default_value="")

        if not oauth_verifier == "":
            key_verifier = "oauth_verifier_" + oauth_verifier
            twitter_user_data = memcache.get(key_verifier)
            if not twitter_user_data == None:
                # Checks if the username was stored previously
                stored_credentials = ndb_pb.searchToken(twitter_user_data["token_id"], "twitter")
                if stored_credentials == None:
                    user_info = {}
                    if not user_identifier == "":
                        # Checks if the user_id taken exists in the system
                        user_id_repeated = True if not ndb_pb.getUser(user_identifier) == None else False
                        if not user_id_repeated:
                            user_info["user_id"] = user_identifier
                            user_key = ndb_pb.insertUser("twitter",
                            twitter_user_data["token_id"], twitter_user_data["access_token"], user_info)

                            # Deletes the key-value for the pair oauth_verifier-session_id stored in memcache
                            memcache.delete(key_verifier)

                            # Returns the session, user_id and social_network cookie
                            session_id = self.login(user_key)
                            self.response.set_cookie("session",
                                    value=session_id, path="/", domain=domain,
                                    secure=True)
                            self.response.set_cookie("social_network",
                                    value="twitter", path="/", domain=domain,
                                    secure=True)
                            self.response.set_cookie("user",
                                    value=user_identifier, path="/", domain=domain,
                                    secure=True)

                            # Builds the response
                            response = {"status": "User logged successfully", "user_id": user_identifier}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(201)
                        else:
                            response = {"error": "The user_identifier provided for the sign up has been already taken"}
                            self.response.content_type = "application/json"
                            self.response.write(json.dumps(response))
                            self.response.set_status(400)
                    else:
                        response = {"error": "You must provide a valid user_identifier in the request"}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(400)
                else:
                    response = \
                    {"error": "The token_id provided belong to a registered user in the system. Consider perform a login request instead"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                response = \
                    {"error": "There isn\"t any Twitter OAuth flow initiated in the system for the oauth_verifier value specified"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(404)
        else:
            response = \
                {"error": "You must specify a value for the oauth_verifier param in the request"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class TwitterLoginHandler(SessionHandler):
    """ This class is a resource that represents the login
    action using the Twitter credentials to autenticate in PicBit
    """
    def post(self):
        oauth_verifier = self.request.get("oauth_verifier",
                default_value="None")
        user_identifier = self.request.get("user_identifier", default_value="")

        if not oauth_verifier == "":
            key_verifier = "oauth_verifier_" + oauth_verifier
            twitter_user_data = memcache.get(key_verifier)
            if not twitter_user_data == None:
                # Checks if the username was stored previously
                stored_credentials = ndb_pb.searchToken(twitter_user_data["token_id"], "twitter")
                if not stored_credentials == None:
                    # We store the new set of credentials
                    user_key = ndb_pb.modifyToken(twitter_user_data["token_id"],
                            twitter_user_data["access_token"], "twitter")
                    user_id = ndb_pb.getUserId(user_key)
                    session_id = self.login(user_key)

                    # Gets the user_id to generate the user cookie
                    user_id = ndb_pb.getUserId(user_key)

                    # Returns the session, social_network and user cookie
                    self.response.set_cookie("session", session_id,
                            path="/", domain=domain, secure=True)
                    self.response.set_cookie("social_network",
                            value="twitter", path="/", domain=domain,
                            secure=True)
                    self.response.set_cookie("user",
                            value=user_id, path="/", domain=domain,
                            secure=True)

                    # Builds the response
                    response = {"status": "User logged successfully", "user_id": user_id}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(200)
                else:
                    response = \
                    {"error": "The token_id provided does not belong to a registered user in the system. Consider perform a signup request instead"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
                response = \
                    {"error": "There isn\"t any session in the system for the oauth_verifier value specified"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(404)
        else:
            response = \
                {"error": "You must specify a value for the oauth_verifier param in the request"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)

class TwitterLogoutHandler(OauthLogoutHandler):
    """ This class is a resource that represents the logout
    action using the Twitter credentials to autenticate in PicBit
    """
    def post(self):
        self.post_logout("twitter")
