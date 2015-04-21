#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
import re
import string
import json
import httplib
import hashlib
import urllib
from google.appengine.ext import ndb
from google.appengine.api import memcache

# Inserts to the path the 'lib' directory

import sys
sys.path.insert(1, 'lib/')

# Local imports
# Eliminados Tag y Release y Repo

import ndb_pb
from ndb_pb import UserRating, Usuario, Grupo, Token, Componente
import cliente_gitHub

# Import for twitter

import oauth

# Imports for ContactHandler

from google.appengine.api import mail

import cliente_gitHub

# Global vars

domain = 'http://example-project-13.appspot.com'


class ComponentListHandler(webapp2.RequestHandler):

    """
  Class that defines the component list resource.
  It acts as the handler of the /components resource

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

        user = self.request.get('user', default_value='none')
        sortBy = self.request.get('sortBy', default_value='stars')
        query = self.request.get('query', default_value='none')
        orderBy = self.request.get('orderBy', default_value='desc')

    # Get all the components stored in the Datastore

        results = Repo.query().fetch()

    # Build the response

        componentList = []
        for item in results:
            rating = 0
            if not user == 'none':
                componentRating = \
                    UserRating.query(ndb.AND(UserRating.google_user_id
                        == user, UserRating.repo_full_name_id
                        == item.full_name_id)).get()
                if not componentRating == None:
                    rating = componentRating.rating_value
            component = {
                'componentId': item.full_name_id,
                'name': item.name_repo,
                'author': item.owner.login,
                'description': item.description,
                'nStars': item.stars,
                'starRate': item.reputation,
                'nForks': item.forks,
                'userRating': rating,
                }
            componentList.append(component)
        self.response.content_type = 'application/json'
        self.response.write(json.dumps(componentList))

  # POST Method

    def post(self):
        """ Uploads a component. The component is stored in the Datastore of the application
    Keyword arguments: 
      self -- info about the request build by webapp2
    """

        url = self.request.get('url', default_value='none')
        user = self.request.get('user', default_value='none')

        component = True
        path = url.split('/')
        basePath = '/repos/' + path[len(path) - 2] + '/' \
            + path[len(path) - 1]
        repoId = ''
        repo_owner = ''

    # Open connection to the API endpoint

        cliente_gitHub.openConnection(basePath)

    # Set available request, in order to get statistics about the request consumed in the upload operation

        availableRequest = cliente_gitHub.getRateLimitRemaining('core')

    # Get repo info

        repoDetails = cliente_gitHub.getRepoInfo()

    # Check if the call to GitHub returned the details about the repo required
    # (if not, the url doesn't correspond to a repo, or the cliente_gitHub encountered
    # an error while doing the call to the GitHub API)

        if repoDetails == None:
            component = False
        else:

      # Set the repoId and repo_owner

            repoId = repoDetails['id']
            repo_owner = repoDetails['owner']['login']

      # Get the languages of the repo

            languages = cliente_gitHub.getRepoLanguages()
            languagesList = []
            for (key, value) in languages.iteritems():
                languagesList.append(key)

    # If the url given corresponds to a web component,
    # the metadata about it is stored and it is sent the number of
    # stars of the repo to Google Analytics

        if component:

      # Also check if the component was uploaded previously

            if not Repo.query(Repo.full_name == repoDetails['full_name'
                              ]).count() == 0:

        # Returns Not Modified Status

                self.response.set_status(304)
            else:

        # Get the Repo tags

                tagsList = cliente_gitHub.getTags(True)

        # Gets the commit details asociated to every tag
        # CommitList contains the commits related to all tags in tagsList

                commitList = cliente_gitHub.getCommitsTags(tagsList)

        # Adds the releases to the repo

                releases = cliente_gitHub.getReleases()

        # Gets the user details

                userDetails = cliente_gitHub.getUserDetails(repo_owner)

        # Stores the info about the repo in the datastore

                repo_full_name = repoDetails['full_name'].replace('/',
                        '_')
                lowerCaseFullName = string.lower(repo_full_name)

        # TODO: See if we have to set full_name_hash:
        #      full_name_hash = generateRepoHash(repo_full_name)

                name_lower_case = string.lower(repoDetails['name'])
                repo = Repo(
                    full_name=repoDetails['full_name'],
                    repo_id=repoId,
                    name_repo=repoDetails['name'],
                    owner=Autor(login=userDetails['login'],
                                user_id=userDetails['id'],
                                html_url=userDetails['html_url'],
                                followers=userDetails['followers']),
                    html_url=repoDetails['html_url'],
                    description=repoDetails['description'],
                    stars=repoDetails['stargazers_count'],
                    forks=repoDetails['forks_count'],
                    reputation=0.0,
                    languages=languagesList,
                    full_name_id=repo_full_name,
                    repo_hash='',
                    reputation_sum=0,
                    ratingsCount=0,
                    name_repo_lower_case=lowerCaseFullName,
                    )
                repo_key = repo.put()

        # The repo is yet stored. Now, it is necessary to update it with the remaining information

                list_tag = []
                list_release = []
                for (tag, commit) in zip(tagsList, commitList):
                    aux_tag = Tag(name_tag=tag['name'],
                                  date_tag=commit['date'],
                                  author=commit['author'],
                                  zipball_url=tag['zipball_url'],
                                  tarball_url=tag['tarball_url'])
                    list_tag.append(aux_tag)

                repo = repo_key.get()
                for release in releases:
                    aux_release = Release(
                        tag_name=release['tag_name'],
                        html_url=release['html_url'],
                        name_release=release['name'],
                        description=release['body'],
                        publish_date=release['published_at'],
                        zipball_url=release['zipball_url'],
                        tarball_url=release['tarball_url'],
                        )
                    list_release.append(aux_release)

        # Now, we store them in the Datastore

                repo = repo_key.get()
                repo.tags = list_tag
                repo.releases = list_release
                repo.put()

        # The component has been uploaded succesfully

                print 'LOG_INFO: Component uploaded succesfully'

        # TODO Build the response

                self.response.set_status(200)
        else:

    # If the uri doesn't correspond to a component, return an error status
      # TODO Build the response

            self.response.set_status(404)

    # Gets statistics about the request to gihtub consumed in the upload operation

        remainingRequests = cliente_gitHub.getRateLimitRemaining('core')
        requestConsumed = availableRequest - remainingRequests
        print 'LOG_INFO: Requests to Github endpoint remaining: ' \
            + str(remainingRequests)
        print 'LOG_INFO: Requests to Github endpoint consumed: ' \
            + str(requestConsumed) + '\n'

    # Close the connection with github endpoint

        cliente_gitHub.closeConnection()


class ComponentHandler(webapp2.RequestHandler):

    """
  Class that defines the component resource
  It acts as the handler of the /components/{component_id} resource
  Methods:
  get -- Gets the info about a component 
  put -- Adds a rating about a component  
  """

  # GET Method

    def get(self, component_id):
        """ Gets the info about a component or
    gets a filtered list of the components stored in the system
    Keyword arguments: 
      self -- info about the request build by webapp2
      component_id -- path url directory corresponding to the component id
    """

    # Get the request params
    # componentId = self.request.get("componentId", default_value = "null")

        user = self.request.get('user', default_value='null')
        componentId = self.request.path

    # Returns the component queried

        component = Repo.query(Repo.full_name_id == component_id).get()
        if component == None:
            self.response.set_status(404)
        else:

      # Get the user rating (userRating field in the response)

            rating = 0
            if not user == 'none':
                componentRating = \
                    UserRating.query(ndb.AND(UserRating.google_user_id
                        == user, UserRating.repo_full_name_id
                        == component.full_name_id)).get()
                if not componentRating == None:
                    rating = componentRating.rating_value

      # Builds the response

            response = {
                'componentId': component.full_name_id,
                'name': component.name_repo,
                'author': component.owner.login,
                'description': component.description,
                'nStars': component.stars,
                'starRate': component.reputation,
                'nForks': component.forks,
                'userRating': rating,
                }
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))

  # POST Method

    def post(self, component_id):
        """ - Add a rating about a component
    Keyword arguments: 
      self -- info about the request build by webapp2
      component_id -- path url directory corresponding to the component id
    """

    # Get the request params

        user = self.request.get('user', default_value='null')
        rate = float(self.request.get('rate', default_value=0.0))

    # Check if the components exists. If not, return

        repo = Repo.query(Repo.full_name_id == component_id).get()
        if not repo == None:
            storedRating = \
                UserRating.query(ndb.AND(UserRating.google_user_id
                                 == user, UserRating.repo_full_name_id
                                 == component_id)).get()
            if storedRating == None:

        # Create the new rating

                newRating = UserRating(google_user_id=user,
                        repo_full_name_id=repo.full_name_id,
                        repo_hash=repo.repo_hash, rating_value=rate)
                newRating.put()

        # Recalculate the reputation of the repo

                repo.reputation_sum = repo.reputation_sum + rate
                repo.ratingsCount = repo.ratingsCount + 1
                repo.reputation = float(repo.reputation_sum
                        / repo.ratingsCount)
                repo.put()
                print 'DEBUG: Creada tupla de valoracion de usuario. Almacenada reputacion'
            else:

        # The User had rated the component previously

                self.response.set_status(304)
        else:

        # raise NotFoundException("Component not found in Datastore")

            self.response.set_status(404)


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


class SessionHandler(webapp2.RequestHandler):

    """
  Class that handles the session of the application
  Methods:
    login - Generates a valid hash for a given user_id
    getUserInfo - Gets the info related to a logged user_id
    logout - Deletes the session for a given user
  """

    def login(self, user_id):
        cypher = hashlib.sha256(str(user_id))
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


class OAuthTwitterHandler(SessionHandler):

    """
  Class that handles the Oauth Twitter Flow
  Methods:
    get -- Handles the calls related to Twitter Tokens.
  """

  # GET Method

    def get(self):
        """ Handles the calls related to Twitter Tokens. 
    Depending on the 'action' param, performs different actions:
    - 'action':request_token. Gets the Twitter access_token for a user authenticated via web and
       stores it in the database. 
    - 'action':access_token. Returns the Twitter access_token for a user authenticated.
    - 'action':authorization. Manages the callback from Twitter in the Twitter oauth flow.
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

        client = oauth.TwitterClient(consumer_key, consumer_secret,
                'http://example-project-13.appspot.com/api/oauth/twitter?action=authorization'
                )

        if action == 'request_token':
            self.response.content_type = 'application/json'
            response = {'oauth_url': client.get_authorization_url()}
            self.response.write(json.dumps(response))
        elif action == 'authorization':

            auth_token = self.request.get('oauth_token')
            auth_verifier = self.request.get('oauth_verifier')
            user_info = client.get_user_info(auth_token,
                    auth_verifier=auth_verifier)

            # We store the user id and token into a Token Entity

            stored_user = Token.query(Token.token == user_info['token'
                    ]).get()

            # TODO: query for the stored user (modificaToken)

            if stored_user == None:
                user_id = ndb_pb.insertaUsuario('Twitter',
                        user_info['username'], user_info['token'])

                # Create Session

                session_id = self.login(str(user_id.id()))
                self.response.set_cookie('session', value=session_id,
                        path='/', domain=domain, secure=True)
                self.response.set_status(201)

            # Create Session

            session_id = self.login(stored_user)
            self.response.set_cookie('session', value=session_id,
                    path='/', domain=domain, secure=True)
            self.response.set_status(200)
        elif action == 'access_token' and not username == None:

            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'username': user_details.nombre_usuario,
                            'id_twitter': user_details.id_tw,
                            'token_twitter': user_details.token_tw}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:

            self.response.set_status(400)


class OAuthGithubHandler(webapp2.RequestHandler):

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

        username = self.request.get('username', default_value='None')
        if not username == None:
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'username': user_details.nombre_usuario,
                            'id_github': user_details.id_git,
                            'token_github': user_details.token_git}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)

  # POST Method

    def post(self):
        """ Defines the flow of the process to get an access_token to use the Github API
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        action = self.request.get('action', default_value='request_code'
                                  )
        url = 'github.com'
        authorize_url = \
            'http://github-login-lab.appspot.com/oauth/github?action=request_token'
        access_token_url = '/login/oauth/access_token'
        client_id = '1f21e4d820abd2cb5a7a'
        client_secret = 'b24d6b5f298e85514bebc70abcbf100a8ef8a5f4'
        access_token = ''

        connection = httplib.HTTPSConnection(url)
        if action == 'request_token':

      # Cogemos el codigo de la peticion

            code = self.request.get('code')

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
                       'User-Agent': 'PolymerBricks-App',
                       'Authorization': 'token TOKEN_GITHUB'}
            connectionAPI.request('GET', '/user', params_token, headers)
            response = connectionAPI.getresponse()
            user_details = json.loads(response.read())

      # Almacenamos el par id usuario/token autenticado

            stored_credentials = Token.query(Token.id_git
                    == str(user_details['id'])).get()
            if stored_credentials == None:

        # Almacena las credenciales en una entidad Token
        # TODO: Generar un id de usuario valido

                user_credentials = Token(id_git=str(user_details['id'
                        ]), token_git=access_token)
                user_credentials.put()
                response = {'username': user_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(201)
            else:

        # Almacenamos el access token recibido

                stored_credentials.id_git = str(user_details['id'])
                stored_credentials.token_git = access_token
                stored_credentials.put()

        # TODO: devolver el propietario de las claves

                response = \
                    {'username': stored_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)


class OauthLinkedinHandler(webapp2.RequestHandler):

  # GET Method

    def get(self):
        """ - Returns the Linkedin access_token for a user authenticated
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        username = self.request.get('username', default_value='None')
        if not username == 'None':
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'token_id': user_details.id_li,
                            'access_token': user_details.token_li}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

  # POST Method

    def post(self):

    # Gets the data from the request form

        try:
            print self.request
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

      # Checks if the username was stored previously

            stored_credentials = Token.query(Token.id_li
                    == token_id).get()
            if stored_credentials == None:

        # Stores the credentials in a Token Entity
        # TODO: Generate a valid username for a new user in the user_credentials

                user_credentials = Token(id_li=token_id,
                        token_li=access_token)
                user_credentials.put()

        # TODO: Return the username owner of the keys

                response = {'username': user_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(201)
            else:

        # We store the new set of credentials

                stored_credentials.id_li = token_id
                stored_credentials.token_li = access_token
                stored_credentials.put()

        # TODO: Return the username owner of the keys

                response = \
                    {'username': stored_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
        except:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OAuthInstagramHandler(webapp2.RequestHandler):

  # GET Method

    def get(self):
        """ - Returns the Instagram access_token for a user authenticated
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        username = self.request.get('username', default_value='None')
        if not username == 'None':
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'token_id': user_details.id_ins,
                            'access_token': user_details.token_ins}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

  # POST Method

    def post(self):

    # self.response.headers['Access-Control-Allow-Origin'] = 'http://example-project-13.appspot.com'

    # Gets the data from the request form

        try:
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

      # Checks if the username was stored previously

            stored_credentials = Token.query(Token.id_ins
                    == token_id).get()
            if stored_credentials == None:

        # Stores the credentials in a Token Entity
        # TODO: Generate a valid username for a new user in the user_credentials

                user_credentials = Token(id_ins=token_id,
                        token_ins=access_token)
                user_credentials.put()

        # TODO: Return the username owner of the keys

                response = {'username': user_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(201)
            else:

        # We store the new set of credentials

                stored_credentials.id_ins = token_id
                stored_credentials.token_ins = access_token
                stored_credentials.put()

        # TODO: Return the username owner of the keys

                response = \
                    {'username': stored_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
        except:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OauthFacebookHandler(webapp2.RequestHandler):

  # GET Method

    def get(self):
        """ - Returns the Facebook access_token for a user authenticated
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        username = self.request.get('username', default_value='None')
        if not username == 'None':
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'token_id': user_details.id_fb,
                            'access_token': user_details.token_fb}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

  # POST Method

    def post(self):

    # Gets the data from the request form

        try:
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

      # Checks if the username was stored previously

            stored_credentials = Token.query(Token.id_fb
                    == token_id).get()
            if stored_credentials == None:

        # Stores the credentials in a Token Entity
        # TODO: Generate a valid username for a new user in the user_credentials

                user_credentials = Token(id_fb=token_id,
                        token_fb=access_token)
                user_credentials.put()

        # TODO: Return the username owner of the keys

                response = {'username': user_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(201)
            else:

        # We store the new set of credentials

                stored_credentials.id_fb = token_id
                stored_credentials.token_fb = access_token
                stored_credentials.put()

        # TODO: Return the username owner of the keys

                response = \
                    {'username': stored_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
        except KeyError:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OauthStackOverflowHandler(webapp2.RequestHandler):

  # GET Method

    def get(self):
        """ - Returns the StackOverflow access_token for a user authenticated
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        username = self.request.get('username', default_value='None')
        if not username == 'None':
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'token_id': user_details.id_sof,
                            'access_token': user_details.token_sof}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

  # POST Method

    def post(self):

    # Gets the data from the request form

        try:
            access_token = self.request.POST['access_token']
            token_id = self.request.POST['token_id']

      # Checks if the username was stored previously

            stored_credentials = Token.query(Token.id_sof
                    == token_id).get()
            if stored_credentials == None:

        # Stores the credentials in a Token Entity
        # TODO: Generate a valid username for a new user in the user_credentials

                user_credentials = Token(id_sof=token_id,
                        token_sof=access_token)
                user_credentials.put()

        # TODO: Return the username owner of the keys

                response = {'username': user_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(201)
            else:

        # We store the new set of credentials

                stored_credentials.id_sof = token_id
                stored_credentials.token_sof = access_token
                stored_credentials.put()

        # TODO: Return the username owner of the keys

                response = \
                    {'username': stored_credentials.nombre_usuario}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
        except:
            response = \
                {'error': 'You must provide a valid pair of access_token and token_id in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


class OauthGooglePlusHandler(SessionHandler):

  # GET Method

    def get(self):
        """ - Returns the Github access_token for a user authenticated
    Keyword arguments: 
    self -- info about the request build by webapp2
    """

        username = self.request.get('username', default_value='None')
        if not username == 'None':
            user_details = Token.query(Token.nombre_usuario
                    == username).get()
            if not user_details == None:
                response = {'token_id': user_details.id_google,
                            'access_token': user_details.token_google}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(200)
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

  # POST Method

    def post(self):

      # Gets the data from the request form

        action = self.request.get('action')
        if action == 'login':
            try:
                access_token = self.request.POST['access_token']
                token_id = self.request.POST['token_id']
            except:
                response = \
                    {'error': 'You must provide a valid pair of access_token and token_id in the request'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)

        # Checks if the username was stored previously

            stored_credentials = ndb_pb.buscaToken(token_id, 'google')
            if stored_credentials == None:

          # Generate a valid username for a new user

                user_id = ndb_pb.insertaUsuario('google', token_id,
                        access_token)
                session_id = self.login(str(user_id.id()))

          # Returns the session cookie

                self.response.set_cookie('session', value=session_id,
                        path='/', domain=domain, secure=True)
                self.response.set_status(201)
            else:

          # We store the new set of credentials (change insertaUsuario)

                user_id = ndb_pb.modificaToken(token_id, access_token,
                        'google')
                session_id = self.login(str(user_id.id()))

          # Returns the session cookie

                self.response.set_cookie('session', value=session_id,
                        path='/', domain=domain, secure=True)
                self.response.set_status(200)
        elif action == 'logout':

            cookie_value = self.request.cookies.get('session')
            print 'Cookie value: ' + cookie_value

        # Logout

            logout_status = self.logout(cookie_value)

        # Delete cookie

            self.response.delete_cookie('session')
            print 'LOGOUT: ' + str(logout_status)
            self.response.set_status(200)
        else:
            response = {'error': 'Invalid value for the action param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


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


class ContactFormsHandler(webapp2.RequestHandler):

    def post(self):

    # Get params

        action = self.request.get('action', default_value='')
        if action == 'contact':

      # Subject is an optional param

            subject = self.request.get('subject', default_value='')
            message = self.request.get('message', default_value='')
            sender = self.request.get('sender', default_value='')
            if not sender == '' and not message == '':
                subject = 'Contacto: ' + subject + ' de: ' + sender
                mail.send_mail('deus@conwet.com', 'deus@conwet.com',
                               subject, message)
            else:
                response = \
                    {'error': 'You must provide a sender and message param'}
                self.response.content_type = 'application/json'
                self.response.write(json.dumps(response))
                self.response.set_status(400)
        elif action == 'subscribe':

            self.response.set_status(501)
        else:
            response = {'error': 'Invalid value for action param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)


app = webapp2.WSGIApplication([
    (r'/api/componentes', ComponentListHandler),
    (r'/api/oauth/twitterTimeline', OAuthTwitterTimelineHandler),
    (r'/api/componentes/(.*)', ComponentHandler),
    (r'/api/oauth/twitter', OAuthTwitterHandler),
    (r'/api/oauth/github', OAuthGithubHandler),
    (r'/api/oauth/linkedin', OauthLinkedinHandler),
    (r'/api/oauth/instagram', OAuthInstagramHandler),
    (r'/api/oauth/facebook', OauthFacebookHandler),
    (r'/api/oauth/stackOverflow', OauthStackOverflowHandler),
    (r'/api/oauth/googleplus', OauthGooglePlusHandler),
    (r'/api/contact', ContactFormsHandler),
    ], debug=True)
