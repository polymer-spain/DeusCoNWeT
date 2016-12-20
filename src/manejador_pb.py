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
sys.path.insert(0, '/var/www/src/api_handlers/')
sys.path.insert(0, '/var/www/src/api_handlers/lib/')
import yaml
import api_usuarios, api_componentes, api_oauth, api_auxiliar
import mimetypes
api_url =[
    (r'/api/componentes', api_componentes.ComponentListHandler),
    (r'/api/componentes/(.*)/valoracionComponente', api_componentes.ComponentRatingHandler),
    (r'/api/componentes/(.*)', api_componentes.ComponentHandler),

    (r'/api/usuarios', api_usuarios.UserListHandler),
    (r'/api/usuarios/([A-Za-z0-9]*)/profile', api_usuarios.ProfileHandler),
    (r'/api/usuarios/([A-Za-z0-9]*)/credentials', api_usuarios.UserCredentialsHandler),
    (r'/api/usuarios/([A-Za-z0-9]*)/assign', api_usuarios.AssignComponentsHandler),
    (r'/api/usuarios/(.*)', api_usuarios.UserHandler),

    (r'/api/aux/twitterTimeline', api_auxiliar.OAuthTwitterTimelineHandler),
    (r'/api/aux/instagramTimeline', api_auxiliar.instagramRequest),

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

    (r'/api/oauth/linkedin/credenciales', api_oauth.LinkedinContainerHandler),
    (r'/api/oauth/linkedin/credenciales/(.*)', api_oauth.LinkedinCredentialHandler),

    (r'/api/oauth/instagram/credenciales', api_oauth.InstagramContainerHandler),
    (r'/api/oauth/instagram/credenciales/(.*)', api_oauth.InstagramCredentialHandler),
    #(r'/api/subscriptions', api_contacto.SubscriptionHandler),
    ]


## LOAD STATIC URL FROM app.yaml
basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "app.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)
class handler(webapp2.RequestHandler):
  def get(self, path):
    if not path:
      path = 'index.html'
    static_folder = self.app.config.get('static_folder', 'static')
    abspath = os.path.join(basepath, static_folder, path)
    print 'Base path: ' + abspath + ', path: ' + path + ', basepath: ' + basepath + ', static:' + static_folder
    try:
      f = open(abspath,'r')
      self.response.out.write(f.read())
      self.response.headers.add_header('Content-Type', mimetypes.guess_type(abspath)[0])
    except:
      self.response.set_status(404)


def createStatic(handler):
    url = handler['url']
    file = handler['static_files']
    return (url, handlerStaticUrl(file))

## LOAD APP
static_url = [(r'/(.*)',handler)]
full_url = api_url + static_url
app = webapp2.WSGIApplication(full_url, debug=True)

# MAIN
def main():
    from paste import httpserver
    from paste.cascade import Cascade
    from paste.urlparser import StaticURLParser
    import threading
    import signal
    
    threads = list()

    # Deploy app
    ssl = os.path.abspath(os.path.join(basepath, '../ssl/ssl.pem'))
    static_app = StaticURLParser("static/")
    application = Cascade([static_app,app])
    httpserver.serve(application, host='0.0.0.0', port=443 , server_version=1.0,ssl_pem=ssl)

if __name__ == '__main__':
    main()
