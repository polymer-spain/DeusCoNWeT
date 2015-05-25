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
import datetime
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


class OAuthLoginHandler(SessionHandler):

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
                         + ' and access_token in ' + social_network \
                         + ' stored in the system'}
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

    def post_credentials(self, social_network):

        # Gets the data from the request form

        action = self.request.get('action')
        if action == 'login':
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
        elif action == 'logout':
            cookie_value = self.request.cookies.get('session')
            if not cookie_value == None:

                # Logout

                logout_status = self.logout(cookie_value)

                # Invalidate cookie

                self.response.set_cookie(
                    'session',
                    cookie_value,
                    path='/',
                    expires=datetime.datetime.now(),
                    domain=domain,
                    secure=True,
                    )

                self.response.set_status(200)
            else:
                response = \
                    {'error': 'This request requires a secure_cookie with the session identifier'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {'error': 'Invalid value for the action param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OAuthHandler(SessionHandler):

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


class OAuthTwitterHandler(SessionHandler):

    """
    Class that handles the Oauth Twitter Flow from the server and represent the Twitter
    token resource.
    Methods:
        get -- Handles the calls related to Twitter Tokens.
        post -- 
    """

    # GET Method

    def get(self):
        """ Handles the calls related to Twitter Tokens. 
        Depending on the 'action' param, performs different actions:
            - 'action': login. Initiates the three-step oauth flow in Twitter. 
            - 'action': credentials. Returns the Twitter token_id and access_token for a user authenticated.
            - 'action': authorization. Manages the callback from Twitter in the Twitter oauth flow.
        Keyword arguments: 
        self -- info about the request build by webapp2
        """

        # self.response.headers['Access-Control-Allow-Origin'] = 'http://example-project-13.appspot.com'

        action = self.request.get('action', default_value='None')
        username = self.request.get('username', default_value='None')

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
                'https://'+domain+'/api/oauth/twitter?action=authorization'
                )
        if action == 'request_token':
            self.response.content_type = 'application/json'
            response = {'oauth_url': client.get_authorization_url()}

            self.response.write(json.dumps(response))
        elif action == 'authorization':

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
        elif action == 'login':

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
        elif action == 'credentials' and not username == None:

            cookie_value = self.request.cookies.get('session')
            if not cookie_value == None:

                # Obtains info related to the user authenticated in the system

                user = self.getUserInfo(cookie_value)

                # Searchs for user's credentials

                if not user == None:
                    user_credentials = ndb_pb.getToken(user, 'twitter')
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
                             + 'and access_token in googleplus stored in the system'}
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
                response = \
                    {'error': 'You must provide a session cookie'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {'error': 'Invalid value for the action param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)

    # POST Method

    def post(self):
        """ Destroys the session previously initialized in the system
            Keyword arguments: 
            self -- info about the request built by webapp2
        """

        action = self.request.get('action', default_value='')
        if action == 'logout':
            cookie_value = self.request.cookies.get('session')
            if not cookie_value == None:

                # Logout

                logout_status = self.logout(cookie_value)

                # Invalidate the cookie

                self.response.set_cookie(
                    'session',
                    cookie_value,
                    path='/',
                    expires=datetime.datetime.now(),
                    domain=domain,
                    secure=True,
                    )


                self.response.set_status(200)
            else:
                response = \
                    {'error': 'This request requires a secure_cookie with the session identifier'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        else:
            response = {'error': 'Invalid value for the action param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OAuthGithubHandler(SessionHandler):

    """
        Class that will act as the handler to ask for the access_token to the GitHub API
        Method:
        get -- Returns the Github access_token for a user authenticated
        post -- Defines the flow of the process to get an access_token to use the Github API 
    """

    # GET Method

    def get(self):
        """ - Returns the Github access_token for a user authenticated
        Keyword arguments: 
        self -- info about the request build by webapp2
        """

        cookie_value = self.request.cookies.get('session')
        action = self.request.get('action', default_value='')
        if action == 'credentials':
            if not cookie_value == None:

                # Obtains info related to the user authenticated in the system

                user = self.getUserInfo(cookie_value)

                # Searchs for user's credentials

                if not user == None:

                    # userKey = ndb.Key(ndb_pb.Usuario,str(user))

                    user_credentials = ndb_pb.getToken(user, 'github')
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
                             + 'and access_token in github stored in the system'}
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
                response = \
                    {'error': 'You must provide a session cookie'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        elif action == 'request_token':
            url = 'github.com'

            # authorize_url = \
            # 'http://test-backend.example-project-13.appspot.com/api/oauth/github?action=request_token'

            access_token_url = '/login/oauth/access_token'
            client_id = '1f21e4d820abd2cb5a7a'
            client_secret = 'b24d6b5f298e85514bebc70abcbf100a8ef8a5f4'
            access_token = ''
            connection = httplib.HTTPSConnection(url)

            # Cogemos el codigo de la peticion

            code = self.request.get('code')
            print code

            # Indicamos los parametros de la peticion a github

            params_token = urllib.urlencode({'client_id': client_id,
                    'client_secret': client_secret, 'code': code})

            # Realizamos la peticion en la conexion

            connection.request('POST', access_token_url, params_token)

            # Cogemos la respuesta de la peticion y realizamos un split
            # para coger el valor del token

            response_token = connection.getresponse()
            data_token = response_token.read()
            access_token = data_token.split('&')
            access_token = access_token[0].split('=')[1]

            # Gestion de la respuesta de webapp

            self.response.content_type = 'application/json'
            response = '{"token": "' + access_token + '"}'
            self.response.write(response)
            connection.close()
            self.response.set_status(200)

            # Obtenemos los detalles del usuario autenticado

            connectionAPI = httplib.HTTPSConnection('api.github.com')
            headers = {'Accept': 'application/vnd.github.v3+json',
                       'User-Agent': 'PicBit-App',
                       'Authorization': 'token GITHUB_TOKEN'}
            connectionAPI.request('GET', '/user', params_token, headers)
            response = connectionAPI.getresponse()
            aux = response.read()
            user_details = json.loads(aux)
            print aux

            # Buscamos el par id usuario/token autenticado en la base

            stored_credentials = ndb_pb.buscaToken(str(user_details['id'
                    ]), 'github')
            if stored_credentials == None:

                # Almacena las credenciales en una entidad Token

                user_credentials = ndb_pb.insertaUsuario('github',
                        str(user_details['id']), access_token)
                self.response.set_status(201)
            else:

                # Almacenamos el access token recibido

                user_id = ndb_pb.modificaToken(str(user_details['id']),
                        access_token, 'github')
                self.response.set_status(200)
        else:
            self.response.set_status(400)


class OauthLinkedinHandler(OAuthHandler):

    """
    Class that represents the Linkedin token resource. 
    Methods:
        get -- Returns the Linkedin access_token and token_id for a user authenticated
        post -- Creates or updates the pair of token_id and access_token for an user.
    """

    # GET Methodo

    def get(self):
        self.get_credentials('linkedin')

    # POST Method

    def post(self):
        self.post_credentials('linkedin')


class OAuthInstagramHandler(OAuthHandler):

    """
    Class that represents the Instagram token resource. 
    Methods:
        get -- Returns the Instagram access_token and token_id for a user authenticated
        post -- Creates or updates the pair of token_id and access_token for an user.
    """

    # GET Method

    def get(self):
        """ - Returns the Instagram access_token for a user authenticated
        Keyword arguments: 
        self -- info about the request build by webapp2
        """

        self.get_credentials('instagram')

    # POST Method

    def post(self):
        """ - Creates or updates the pair of token_id and access_token for an user.
            Keyword arguments: 
            self -- info about the request build by webapp2
        """

        self.post_credentials('instagram')


class OauthFacebookHandler(OAuthLoginHandler):

    """
    Class that represents the FaceBook token resource. 
    Methods:
        get -- Returns the Facebook access_token and token_id for a user authenticated
        post -- Creates or updates the pair of token_id and access_token for an user and
            initiates a new session or destroy a session previously initialized.
    """

    # GET Method

    def get(self):
        """ - Returns the Facebook access_token for a user authenticated
        Keyword arguments: 
        self -- info about the request built by webapp2
        """

        self.get_credentials('facebook')

    # POST Method

    def post(self):
        self.post_credentials('facebook')


class OauthStackOverflowHandler(OAuthHandler):

    """
        Class that represents the StackOverflow token resource. 
        Methods:
            get -- Returns the StackOverflow access_token and token_id
                     for a user authenticated.
            post -- Creates or updates the pair of token_id and access_token
                     for an user authenticated.
    """

    # GET Method

    def get(self):
        """ - Returns the StackOverflow access_token for a user authenticated
            Keyword arguments: 
            self -- info about the request build by webapp2
        """

        self.get_credentials('stackoverflow')

    # POST Method

    def post(self):
        """ Creates or updates the pair of token_id and access_token for an user.        
        Keyword arguments: 
            self -- info about the request built by webapp2
        """

        self.post_credentials('stackoverflow')


class OauthGooglePlusHandler(OAuthLoginHandler):

    """
    Class that represents the GooglePlus token resource. 
    Methods:
        get -- Returns the GooglePlus access_token and token_id for a user authenticated
        post -- Creates or updates the pair of token_id and access_token for an user and
        initiates a new session or destroy a session previously initialized.
    """

    # GET Method

    def get(self):
        """ - Returns the GooglePlus access_token and token_id for a user authenticated
        Keyword arguments: 
        self -- info about the request built by webapp2
        """

        self.get_credentials('google')

    # POST Method

    def post(self):
        """ - It performs two possible actions:
            Login: Creates or updates the pair of token_id and access_token for an user.
                   Also, it initiates a session in the system. 
            Logout: Destroys the session previously initialized in the system
        Keyword arguments: 
        self -- info about the request built by webapp2
        """

        self.post_credentials('google')


class OAuthTwitterTimelineHandler(webapp2.RequestHandler):

    def get(self):
        consumer_key = self.request.get('consumer_key', default_value=''
                )
        consumer_secret = self.request.get('consumer_secret',
                default_value='')
        access_token = self.request.get('access_token', default_value=''
                )
        secret_token = self.request.get('secret_token', default_value=''
                )
        count = self.request.get('count', default_value='20')

        client = oauth.TwitterClient(consumer_key, consumer_secret,
                'oob')

        respuesta = \
            client.make_request('https://api.twitter.com/1.1/statuses/home_timeline.json'
                                , token=access_token,
                                secret=secret_token,
                                additional_params={'count': count},
                                protected=True)
        self.response.write(respuesta.content)


