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
import re
# Import API handlers
import sys
import os
import pprint as pp
sys.path.insert(0, '/var/www/src/api_handlers')
sys.path.insert(0, '/var/www/src/api_handlers/lib')
import yaml
import api_usuarios, api_componentes, api_oauth, api_auxiliar
import mimetypes
import logging

## API URLS and handlers
api_url =[
    (r'/api/componentes/bva', api_componentes.BVAHandler),
    (r'/api/componentes', api_componentes.ComponentListHandler),
    (r'/api/componentes/(.*)/valoracionComponente', api_componentes.ComponentRatingHandler),
    (r'/api/componentes/(.*)', api_componentes.ComponentHandler),


    (r'/api/usuarios', api_usuarios.UserListHandler),
    (r'/api/usuarios/([A-Za-z0-9]*)/profile', api_usuarios.ProfileHandler),
    (r'/api/usuarios/([A-Za-z0-9]*)/credentials', api_usuarios.UserCredentialsHandler),
    # (r'/api/usuarios/([A-Za-z0-9]*)/assign', api_usuarios.AssignComponentsHandler),
    (r'/api/usuarios/(.*)', api_usuarios.UserHandler),

    (r'/api/aux/twitterTimeline', api_auxiliar.OAuthTwitterTimelineHandler),
    (r'/api/aux/instagramTimeline', api_auxiliar.instagramRequest),
    (r'/api/aux/facebookToken', api_auxiliar.OAuthFacebookAccessToken),
    (r'/api/aux/facebookTimeline', api_auxiliar.OAuthFacebookTimeline),

    (r'/api/oauth/twitter/signup',api_oauth.TwitterSignUpHandler),
    (r'/api/oauth/twitter/login', api_oauth.TwitterLoginHandler),
    (r'/api/oauth/twitter/logout', api_oauth.TwitterLogoutHandler),
    (r'/api/oauth/twitter/credenciales', api_oauth.TwitterCredentialsHandler),
    (r'/api/oauth/twitter/credenciales/(.*)', api_oauth.TwitterHandler),

    # Special URIs to perform the Server-side Twitter login flow
    (r'/api/oauth/twitter/authorization', api_oauth.TwitterAuthorizationHandler),
    (r'/api/oauth/twitter/authorization/(.*)', api_oauth.TwitterAuthorizationDetailsHandler),
    (r'/api/oauth/twitter/request_token', api_oauth.TwitterRequestLoginHandler),


    (r'/api/oauth/facebook/signup',api_oauth.FacebookSignUpHandler),
    (r'/api/oauth/facebook/login', api_oauth.FacebookLoginHandler),
    (r'/api/oauth/facebook/logout', api_oauth.FacebookLogoutHandler),
    (r'/api/oauth/facebook/credenciales', api_oauth.FacebookCredentialsHandler),
    (r'/api/oauth/facebook/credenciales/(.*)', api_oauth.FacebookHandler),

    (r'/api/oauth/googleplus/signup',api_oauth.GooglePlusSignUpHandler),
    (r'/api/oauth/googleplus/login', api_oauth.GooglePlusLoginHandler),
    (r'/api/oauth/googleplus/logout', api_oauth.GooglePlusLogoutHandler),
    (r'/api/oauth/googleplus/credenciales', api_oauth.GooglePlusCredentialsHandler),
    (r'/api/oauth/googleplus/credenciales/(.*)', api_oauth.GooglePlusHandler),

    (r'/api/oauth/stackoverflow/credenciales', api_oauth.StackOverflowContainerHandler),
    (r'/api/oauth/stackoverflow/credenciales/(.*)', api_oauth.StackOverflowCredentialHandler),

    (r'/api/oauth/github/credenciales', api_oauth.GitHubContainerHandler),
    (r'/api/oauth/github/credenciales/(.*)', api_oauth.GitHubCredentialHandler),

    (r'/api/oauth/pinterest/credenciales', api_oauth.PinterestContainerHandler),
    (r'/api/oauth/pinterest/credenciales/(.*)', api_oauth.PinterestCredentialHandler),

    (r'/api/oauth/linkedin/credenciales', api_oauth.LinkedinContainerHandler),
    (r'/api/oauth/linkedin/credenciales/(.*)', api_oauth.LinkedinCredentialHandler),

    (r'/api/oauth/instagram/credenciales', api_oauth.InstagramContainerHandler),
    (r'/api/oauth/instagram/credenciales/(.*)', api_oauth.InstagramCredentialHandler),
    #(r'/api/subscriptions', api_contacto.SubscriptionHandler),
    ]


## LOAD STATIC URL FROM app.yaml
basepath = os.path.dirname(__file__)
# Load app.yaml
configFile = os.path.abspath(os.path.join(basepath, "app.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)




# Handler for static files. config={static_folder:"STATIC_DIR"} set static folder. Default static
class staticFiles(webapp2.RequestHandler):
  def get(self, path):
    # If url is base (/) load index.html. (Depecrated?)
    if not path:
      path = 'index.html'
    static_folder = self.app.config.get('static_folder', 'static')
    # Get abs path to file
    abspath = os.path.join(basepath, static_folder, path)
    # Try to load the file. If error, throw 404
    try:
      f = open(abspath,'r')
      self.response.out.write(f.read())
      self.response.headers.add_header('Content-Type', mimetypes.guess_type(abspath)[0])
    except:
      self.response.set_status(404)


## Return a handler for URL defined on app.yaml like static
def handlerHelper(files):
  class handler(webapp2.RequestHandler):
    def get(self):
      abspath = os.path.join(basepath, files)
      try:
        f = open(abspath,'r')
        self.response.out.write(f.read())
        self.response.headers.add_header('Content-Type', mimetypes.guess_type(abspath)[0])
      except:
        self.response.set_status(404)
  return handler

# Load URL from app.yaml
def createStatic(handler):
    url = handler['url']
    files = handler['static_files']
    return (url, handlerHelper(files))


## LOAD APP
defined_url = [ url for url in cfg['handlers'] if url.has_key('static_files')]
defined_url = [createStatic(handler) for handler in defined_url]

# Static folder
static_url = [(r'/(.*)',staticFiles)]
# api_urls + app.yaml urls + static_folder
full_url = api_url + defined_url + static_url

app = webapp2.WSGIApplication(full_url, debug=True)



# MAIN
def main(argv, name, app):
    from paste import httpserver
    from paste.cascade import Cascade
    from paste.urlparser import StaticURLParser
    import sys, getopt
    
    PORT = 8080
    HOST = 'localhost'
    SSL = None
    STATIC = 'static/'
    # Load config from arguments
    try:
        opts, args = getopt.getopt(argv,"", ["port=", "host=", "ssl=", "static="])
    except getopt.GetoptError:
        print name + ' [--port PORT] [--host HOST] [--ssl SSL_FILE] [--static STATIC_FOLDER]'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '--port':
            PORT = arg
        elif opt == "--host":
            HOST = arg
        elif opt == "--ssl":
            SSL = arg
        elif opt == "--static":
            STATIC = arg
    # Deploy app
    if STATIC:
        static_app = StaticURLParser("static/")
        app = Cascade([static_app,app])
    if SSL:
        ssl_dir = os.path.abspath(os.path.join(basepath, '../ssl/ssl.pem'))
        httpserver.serve(app, host=HOST, port=PORT , server_version=1.0,ssl_pem=ssl_dir)
    else:
        httpserver.serve(app, host=HOST, port=PORT , server_version=1.0)

if __name__ == '__main__':
    main(sys.argv[1:], sys.argv[0], app)
