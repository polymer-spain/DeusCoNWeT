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
from ndb_pb import Token, Usuario

# Imports for TwitterHandler

import oauth
from google.appengine.api import channel

# Import config vars
# import ConfigParser
# configParser = ConfigParser.RawConfigParser()
# configFilePath = r'config.cfg'
# configParser.read(configFilePath)
# domain = configParser.get('app_data', 'domain')

# Import config vars

basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, 'config.yaml'))
with open(configFile, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

domain = cfg['domain']


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
    def post_login(self, social_network):
        try:
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

            # Checks if the username was stored previously

            stored_credentials = ndb_pb.buscaToken(token_id,
                    social_network)
            if stored_credentials == None:

                # Generate a valid username for a new user

                user_id = ndb_pb.insertaUsuario(social_network,
                        token_id, access_token)
                session_id = self.login(user_id)

                # Returns the session cookie

                self.response.set_cookie('session', session_id,
                        path='/', domain=domain, secure=True)

                # self.response.headers.add_header('Set-Cookie', 'session=%s' % session_id)

                self.response.set_status(201)
            else:

                # We store the new set of credentials

                user_id = ndb_pb.modificaToken(token_id,
                        access_token, social_network)
                session_id = self.login(user_id)

                # Returns the session cookie
                # self.response.set_cookie('session',value=session_id, secure=False)
                # self.response.headers.add_header('Set-Cookie', 'session=%s' % session_id)

                self.response.set_cookie('session', session_id,
                        path='/', domain=domain, secure=True)
                self.response.set_status(200)
        except KeyError:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)

class OauthLogoutHandler(SessionHandler):
    def post_logout(self, social_network):
        cookie_value = self.request.cookies.get('session')
            if not cookie_value == None:
                # Logout
                logout_status = self.logout(cookie_value)
                # TODO: Invalidate the cookie!
                self.response.delete_cookie('session')
                self.response.set_status(200)
            else:
                response = \
                    {'error': 'This request requires a secure_cookie with the session identifier'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)


class OauthCredentialsHandler(SessionHandler):
    def get_credentials(self, social_network):
    cookie_value = self.request.cookies.get('session')
    if not cookie_value == None:

        # Obtains info related to the user authenticated in the system
        user = self.getUserInfo(cookie_value)

        # Searchs for user's credentials
        if not user == None:
            # userKey = ndb.Key(ndb_pb.Usuario,str(user))
            user_credentials = ndb_pb.getToken(user, social_network)
            if not user_credentials == None:
                response = \
                    {'token_id': user_credentials.identificador,
                     'access_token': user_credentials.token}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                response = \
                    {'error': 'The active user does not have a pair of token_id' \
                     + 'and access_token in linkedin stored in the system'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(404)
        else:
            response = \
                {'error': 'The cookie session provided does not belongs to any active user'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)
    else:
        response = {'error': 'You must provide a session cookie'}
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(response))
        self.response.set_status(400)

    # TODO!
    def delete_credentials(self, social_network):
        pass


class OAuthCredentialsContainerHandler(SessionHandler):
    def post_credentials(self, social_network):
        # Gets the data from the request form
        try:
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

            # Checks if the username was stored previously
            stored_credentials = ndb_pb.buscaToken(token_id,
                    social_network)
            if stored_credentials == None:

              # Stores the credentials in a Token Entity
                ndb_pb.insertaUsuario(social_network, token_id,
                        access_token)
                self.response.set_status(201)
            else:

                # We store the new set of credentials
                user_id = ndb_pb.modificaToken(token_id, access_token,
                        social_network)
                self.response.set_status(200)
        except KeyError:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


# Handler that manages the callback from Twitter as a final step of the oauth flow
class TwitterAuthorizationHandler(webapp2.RequestHandler):
    def get(self):
        # Gets the params in the request
        auth_token = self.request.get('oauth_token')
        oauth_verifier = self.request.get('oauth_verifier')

        # Retrieves user info
        user_info = client.get_user_info(auth_token,
                auth_verifier=oauth_verifier)

        # Query for the stored user
        stored_user = ndb_pb.buscaToken(user_info['username'],
                'twitter')
        if stored_user == None:

            # We store the user id and token into a Token Entity
            user_id = ndb_pb.insertaUsuario('twitter',
                    user_info['username'], user_info['token'])
            response_status = 201
            self.response.set_status(response_status)
        else:

            # We store the new user's access_token
            user_id = ndb_pb.modificaToken(user_info['username'],
                    user_info['token'], 'twitter')
            response_status = 200
            self.response.set_status(response_status)

        # Create Session
        session_id = self.login(user_id)

        # Stores in memcache the session id associated with the oauth_verifierj
        key_verifier = 'oauth_verifier_' + oauth_verifier
        data = {'session_id': session_id,
                'response_status': response_status}
        memcache.add(key_verifier, data)

# Handler that manages the first step in the Twitter login flow 
# (obtain the request token and request url to initiate the login in client)
class TwitterRequestLoginHandler(webapp2.RequestHandler):
    def get(self):
        consumer_key = 'tuprQMrGCdGyz7QDVKdemEWXl'
        consumer_secret = \
            'byQEyUYKZm1R7ZatsSWoFLX0lYn8hRONBU4AAyGLFRDWVg7rzm'
        request_token_url = \
            'https://api.twitter.com/oauth/request_token'
        base_authorization_url = \
            'https://api.twitter.com/oauth/authorize'
        callback_uri = 'https://' + domain \
            + '/api/oauth/twitter?action=authorization'
        client = oauth.TwitterClient(consumer_key, consumer_secret,
                callback_uri)
        self.response.content_type = 'application/json'
        response = {'oauth_url': client.get_authorization_url()}
        self.response.write(json.dumps(response))

# Handlers that identifies resource containers for a social network 

class FacebookContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('facebook')

class GitHubContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('github')

class GoogleplusContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('google')

class InstagramContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('instagram')

class LinkedinContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('linkedin')

class StackOverflowContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('stackoverflow')

class TwitterContainerHandler(OAuthCredentialsContainerHandler):
    def post(self):
        self.post_credentials('twitter')


# Handlers that represents the credentials for a given social network
class FacebookHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("facebook")

    def delete(self):
        self.delete_credentials("facebook")

class GitHubHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("github")

    def delete(self):
        self.delete_credentials("github")

class GoogleplusHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("google")

    def delete(self):
        self.delete_credentials("google")

class InstagramHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("instagram")

    def delete(self):
        self.delete_credentials("instagram")

class LinkedinHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("linkedin")

    def delete(self):
        self.delete_credentials("linkedin")

class StackOverflowHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("stackoverflow")

    def delete(self):
        self.delete_credentials("stackoverflow")

class TwitterHandler(OauthCredentialsHandler):
    def get(self):
        self.get_credentials("twitter")

    def delete(self):
        self.delete_credentials("twitter")


# Handlers for the login flow in a given network

class FacebookLoginHandler(OauthLoginHandler):
    def post(self):
        self.post_login('facebook')

class GoogleplusLoginHandler(OauthLoginHandler):
    def post(self):
        self.post_login('google')

class TwitterLoginHandler(SessionHandler):
    def post(self):
        # TODO: data!!
        oauth_verifier = self.request.get('oauth_verifier',
                default_value='None')
        if not oauth_verifier == '':
            key_verifier = 'oauth_verifier_' + oauth_verifier
            data = memcache.get(key_verifier)
            print type(data)
            if not data == None:
                session_id = data['session_id']
                response_status = data['response_status']

                # Set the cookie session with the session id stored in the system

                self.response.set_cookie('session',
                        value=session_id, path='/', domain=domain,
                        secure=True)

                # Delete the key-value for the pair oauth_verifier-session_id stored in memcache

                memcache.delete(key_verifier)
                self.response.set_status(response_status)
            else:
                response = \
                    {'error': 'There isn\'t any session in the system for the oauth_verifier value specified'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(404)
        else:
            response = \
                {'error': 'You must specify a value for the oauth_verifier param in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


# Handlers for the logout flow in a given network
class FacebookLogoutHandler(OauthLogoutHandler):
    def post(self):
        self.post_logout('facebook')

class GoogleplusLogoutHandler(OauthLogoutHandler):
    def post(self):
        self.post_logout('google')

class TwitterLogoutHandler(SessionHandler):
    def post(self):
        self.post_logout('google')
