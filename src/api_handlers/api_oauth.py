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

# Imports for TwitterHandler
import oauth
from google.appengine.api import channel

# Import config vars
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)

domain = cfg["domain"]


# Generic handlers for the session management, login, logout and actions 
# related to user credentials 
class SessionHandler(webapp2.RequestHandler):
    """
    Class that handles the session of the application
    Methods:
        login - Generates a valid hash for a given user_id
        getUserInfo - Gets the info related to a logged user_id
        logout - Deletes the session for a given user
    """

    def login(self, user_id):
        message = str(user_id.id()) + str(time.time())
        cypher = hashlib.sha256(message)
        hash_id = cypher.hexdigest()

        # Store in memcache hash-user_id pair
        memcache.add(hash_id, user_id)
        return hash_id

    def getUserInfo(self, hashed_id):
        user = memcache.get(hashed_id)
        return user

    def logout(self, hashed_id):
        logout_status = False
        status = memcache.delete(hashed_id)
        if status == 2:
            logout_status = True
        return logout_status

class OauthLoginHandler(SessionHandler):
    """ Defines the logic for the login action, in those social networks that
        act as authentication services in PicBit, and have 
        a client authorization flow (for example, GooglePlus or Facebook)
        Methods:
            post_login - Implements the login action. Stores the pair of 
            token_in and access_token in the system, and generates the
            cookie for the session.
    """
    def post_login(self, social_network):
        try:
            access_token = self.request.POST["access_token"]
            token_id = self.request.POST["token_id"]
            user_identifier = self.request.POST["user_identifier"]

            # Checks if the username was stored previously
            stored_credentials = ndb_pb.searchToken(token_id,
                    social_network)
            if stored_credentials == None:
                data = {}
                data["user_id"] = user_identifier
                # Generate a valid username for a new user
                user_key = ndb_pb.insertUser(social_network,
                        token_id, access_token, data)
                session_id = self.login(user_key)

                # Returns the session cookie
                self.response.set_cookie("session", session_id,
                        path="/", domain=domain, secure=True)

                self.response.set_status(201)
            else:
                # We store the new set of credentials
                user_key = ndb_pb.modifyToken(token_id,
                        access_token, social_network)
                session_id = self.login(user_key)

                # Returns the session cookie
                self.response.set_cookie("session", session_id,
                        path="/", domain=domain, secure=True)
                self.response.set_status(200)
        except KeyError:
            response = \
                {"error": "You must provide a valid pair of access_token and token_id in the request," +
                " along with the user_identifier owner of the credentials"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(400)

class OauthLogoutHandler(SessionHandler):
    """ Defines the logic for the logout action, in those social networks that
        act as authentication services in PicBit, and have 
        a client authorization flow (for example, GooglePlus or Facebook)
        Methods:
            post_logout - Implements the logout action. Destroys the
            cookie for the session.
    """
    def post_logout(self, social_network):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            # Logout
            logout_status = self.logout(cookie_value)
            # TODO: Invalidate the cookie!
            self.response.delete_cookie("session")
            self.response.set_status(200)
        else:
            response = \
                {"error": "This request requires a secure_cookie with the session identifier"}
            self.response.content_type = "application/json"
            self.response.write(json.dumps(response))
            self.response.set_status(401)


class OauthCredentialsHandler(SessionHandler):
    def get_credentials(self, social_network, token_id):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            # Obtains info related to the user authenticated in the system
            logged_user = self.getUserInfo(cookie_value)
            # Searchs for user"s credentials
            if not logged_user == None:
                # Obtains user info
                logged_user_info = json.loads(ndb_pb.getUser(logged_user))
                logged_user_id = logged_user_info["user_id"]
                # Obtains user credentials
                user_credentials = ndb_pb.getToken(token_id, social_network)
                if not user_credentials == None:
                    if user_credentials["user_id"] == logged_user_id:
                        response = \
                            {"user_id": user_credentials["user_id"],
                            "access_token": user_credentials["token"]}
                        self.response.content_type = "application/json"
                        self.response.write(json.dumps(response))
                        self.response.set_status(200)
                    else:
                        response = \
                            {"user_id": user_credentials["user_id"]}
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
                response = \
                    {"error": "The cookie session provided does not belongs to any active user"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        
        # If we don't provide a cookie in the request, we search for the token in the system
        # and return a 200 o 404 status. It is a request included in the login flow of the system
        else:
            user_credentials = ndb_pb.getToken(token_id, social_network)
            if not user_credentials == None:
                response = \
                    {"response": "The token requested correspond to an active user in the system"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                response = \
                    {"error": "The token requested was not found in the system"}
                self.response.content_type = "application/json"
                self.response.write(json.dumps(response))
                self.response.set_status(404)

    
    def delete_credentials(self, social_network, token_id):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            # Searchs for user"s credentials
            user = self.getUserInfo(cookie_value)
            if not user == None:
                deleteStatus = ndb_pb.deleteCredentials(user, social_network, token_id)
                if deleteStatus:
                    response = \
                        {"status": "Credentials deleted successfully"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(204)
                else:
                    response = \
                        {"status": "Token not found in the system"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(404)
            else:
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


class OAuthCredentialsContainerHandler(SessionHandler):
    def post_credentials(self, social_network):
        cookie_value = self.request.cookies.get("session")
        if not cookie_value == None:
            user = self.getUserInfo(cookie_value)
            if not user == None:
                try:
                    # Gets the data from the request form
                    access_token = self.request.POST["access_token"]
                    token_id = self.request.POST["token_id"]

                    # Checks if the username was stored previously
                    stored_credentials = ndb_pb.searchToken(token_id,
                            social_network)
                    print "Stored credentials ", stored_credentials
                    if stored_credentials == None:

                      # Stores the credentials in a Token Entity
                        ndb_pb.insertUser(social_network, token_id,
                                access_token)
                        self.response.set_status(201)
                    else:

                        # We store the new set of credentials
                        user_id = ndb_pb.modifyToken(token_id, access_token,
                                social_network)
                        self.response.set_status(200)
                except KeyError:
                    response = \
                        {"error": "You must provide a valid pair of access_token and token_id in the request"}
                    self.response.content_type = "application/json"
                    self.response.write(json.dumps(response))
                    self.response.set_status(400)
            else:
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

class FacebookLogoutHandler(OauthLogoutHandler):
    """ This class is a resource that represents the logout 
    action using the Facebook credentials to autenticate in PicBit 
    """
    def post(self):
        self.post_logout("facebook")

# HANDLERS FOR RESOURCES RELATED TO GITHUB
class GitHubHandler(OauthCredentialsHandler):
    """
    Class that represents the GitHub token resource. 
    Methods:
        get -- Returns the GitHub access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in GitHub for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("github", token_id)

    def delete(self, token_id):
        self.delete_credentials("github", token_id)


class GitHubContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Github credentials resource. 
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in GitHub)
    """
    def post(self):
        url = "github.com"
        # authorize_url = \
        # "http://test-backend.example-project-13.appspot.com/api/oauth/github?action=request_token"
        access_token_url = "/login/oauth/access_token"
        client_id = "1f21e4d820abd2cb5a7a"
        client_secret = "b24d6b5f298e85514bebc70abcbf100a8ef8a5f4"
        access_token = ""
        connection = httplib.HTTPSConnection(url)

        # Cogemos el codigo de la peticion
        code = self.request.get("code")

        # Indicamos los parametros de la peticion a github
        params_token = urllib.urlencode({"client_id": client_id,
                "client_secret": client_secret, "code": code})

        # Realizamos la peticion en la conexion
        connection.request("POST", access_token_url, params_token)

        # Cogemos la respuesta de la peticion y realizamos un split
        # para coger el valor del token
        response_token = connection.getresponse()
        data_token = response_token.read()
        access_token = data_token.split("&")
        access_token = access_token[0].split("=")[1]

        # Gestion de la respuesta de webapp
        self.response.content_type = "application/json"
        response = {"token": "" + access_token + ""}
        self.response.write(json.dumps(response))
        connection.close()
        self.response.set_status(200)

        # Obtenemos los detalles del usuario autenticado
        connectionAPI = httplib.HTTPSConnection("api.github.com")
        headers = {"Accept": "application/vnd.github.v3+json",
                   "User-Agent": "PicBit-App",
                   "Authorization": "token GITHUB_TOKEN"}
        connectionAPI.request("GET", "/user", params_token, headers)
        response = connectionAPI.getresponse()
        aux = response.read()
        user_details = json.loads(aux)
        print aux

        # Buscamos el par id usuario/token autenticado en la base
        stored_credentials = ndb_pb.searchToken(str(user_details["id"
                ]), "github")
        if stored_credentials == None:

            # Almacena las credenciales en una entidad Token
            user_credentials = ndb_pb.insertUser("github",
                    str(user_details["id"]), access_token)
            self.response.set_status(201)
        else:

            # Almacenamos el access token recibido
            user_id = ndb_pb.modifyToken(str(user_details["id"]),
                    access_token, "github")
            self.response.set_status(200)


# HANDLERS FOR RESOURCES RELATED TO GOOGLEPLUS
class GooglePlusHandler(OauthCredentialsHandler):
    """
    Class that represents the Instagram token resource. 
    Methods:
        get -- Returns the Instagram access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Instagram for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("google", token_id)

    def delete(self, token_id):
        self.delete_credentials("google", token_id)

class GooglePlusLoginHandler(OauthLoginHandler):
    """ This class is a resource that represents the login 
    action using the GooglePlus credentials to autenticate in PicBit 
    """
    def post(self):
        self.post_login("google")


class GooglePlusLogoutHandler(OauthLogoutHandler):
    """ This class is a resource that represents the logout
    action using the GooglePlus credentials to autenticate in PicBit 
    """
    def post(self):
        self.post_logout("google")


# HANDLERS FOR RESOURCES RELATED TO INSTAGRAM
class InstagramHandler(OauthCredentialsHandler):
    """
    Class that represents the Instagram token resource. 
    Methods:
        get -- Returns the Instagram access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Instagram for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("instagram", token_id)

    def delete(self, token_id):
        self.delete_credentials("instagram", token_id)

class InstagramContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Instagram credentials resource. 
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in GitHub)
    """
    def post(self):
        self.post_credentials("instagram")


# HANDLERS FOR RESOURCES RELATED TO LINKEDIN
class LinkedinHandler(OauthCredentialsHandler):
    """
    Class that represents the Linkedin token resource. 
    Methods:
        get -- Returns the Linkedin access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in Linkedin for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("linkedin", token_id)

    def delete(self, token_id):
        self.delete_credentials("linkedin", token_id)

class LinkedinContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Linkedin credentials resource. 
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in GitHub)
    """
    def post(self):
        self.post_credentials("linkedin")


# HANDLERS FOR RESOURCES RELATED TO STACKOVERFLOW
class StackOverflowHandler(OauthCredentialsHandler):
    """
    Class that represents the StackOverflow token resource. 
    Methods:
        get -- Returns the StackOverflow access_token and token_id
               for a user authenticated
        delete -- Deletes the pair of token_id and access_token
                  in StackOverflow for the user authenticated
    """
    def get(self, token_id):
        self.get_credentials("stackoverflow", token_id)

    def delete(self, token_id):
        self.delete_credentials("stackoverflow", token_id)

class StackOverflowContainerHandler(OAuthCredentialsContainerHandler):
    """
    Class that represents the List of Stackoverflow credentials resource. 
    Methods:
        post -- Adds a new set of credentials (token_id and access_token in GitHub)
    """
    def post(self):
        self.post_credentials("stackoverflow")

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
        """ Handles the first step in the Twitter login flow
        Keyword arguments: 
        self -- info about the request build by webapp2
        """
        # Configuration params in order to perform the request to Twitter
        consumer_key = "tuprQMrGCdGyz7QDVKdemEWXl"
        consumer_secret = \
            "byQEyUYKZm1R7ZatsSWoFLX0lYn8hRONBU4AAyGLFRDWVg7rzm"
        request_token_url = \
            "https://api.twitter.com/oauth/request_token"
        base_authorization_url = \
            "https://api.twitter.com/oauth/authorize"
        callback_uri = "https://" + domain \
            + "/api/oauth/twitter?action=authorization"
        # Request to Twitter the request_token and authorization URL
        client = oauth.TwitterClient(consumer_key, consumer_secret,
                callback_uri)
        # Return the authorization URL
        self.response.content_type = "application/json"
        response = {"oauth_url": client.get_authorization_url()}
        self.response.write(json.dumps(response))


# Handler that manages the callback from Twitter as a final step of the oauth flow
class TwitterAuthorizationHandler(webapp2.RequestHandler):
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

        # Query for the stored user
        stored_user = ndb_pb.searchToken(user_info["username"],
                "twitter")
        if stored_user == None:

            # We store the user id and token into a Token Entity
            user_id = ndb_pb.insertUser("twitter",
                    user_info["username"], user_info["token"])
            response_status = 201
            self.response.set_status(response_status)
        else:

            # We store the new user"s access_token
            user_id = ndb_pb.modifyToken(user_info["username"],
                    user_info["token"], "twitter")
            response_status = 200
            self.response.set_status(response_status)

        # Create Session
        session_id = self.login(user_id)

        # Stores in memcache the session id associated with the oauth_verifierj
        key_verifier = "oauth_verifier_" + oauth_verifier
        data = {"session_id": session_id,
                "response_status": response_status
                }
        memcache.add(key_verifier, data)


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


class TwitterLoginHandler(SessionHandler):
    """ This class is a resource that represents the login 
    action using the Twitter credentials to autenticate in PicBit 
    """
    def post(self):
        oauth_verifier = self.request.get("oauth_verifier",
                default_value="None")
        if not oauth_verifier == "":
            key_verifier = "oauth_verifier_" + oauth_verifier
            data = memcache.get(key_verifier)
            print type(data)
            if not data == None:
                session_id = data["session_id"]
                response_status = data["response_status"]
                # Set the cookie session with the session id stored in the system
                self.response.set_cookie("session",
                        value=session_id, path="/", domain=domain,
                        secure=True)

                # Delete the key-value for the pair oauth_verifier-session_id stored in memcache
                memcache.delete(key_verifier)
                self.response.set_status(response_status)
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

class TwitterLogoutHandler(SessionHandler):
    """ This class is a resource that represents the logout 
    action using the Twitter credentials to autenticate in PicBit 
    """
    def post(self):
        self.post_logout("twitter")