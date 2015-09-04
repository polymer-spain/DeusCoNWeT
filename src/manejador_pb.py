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
sys.path.insert(1, 'api_handlers/')
sys.path.insert(1, 'api_handlers/lib/')

import api_usuarios, api_componentes, api_contacto, api_oauth, api_auxiliar


app = webapp2.WSGIApplication([
    (r'/api/componentes', api_componentes.ComponentListHandler),
    (r'/api/componentes/(.*)', api_componentes.ComponentHandler),
    
    (r'/api/usuarios', api_usuarios.UserListHandler),
    (r'/api/usuarios/(.*)', api_usuarios.UserHandler),
    
    (r'/api/aux/twitterTimeline', api_auxiliar.OAuthTwitterTimelineHandler),
    (r'/api/aux/instagramTimeline', api_auxiliar.instagramRequest),
    
    (r'/api/oauth/twitter/login', api_oauth.TwitterLoginHandler),
    (r'/api/oauth/twitter/logout', api_oauth.TwitterLogoutHandler),
    (r'/api/oauth/twitter/authorization', api_oauth.TwitterAuthorizationHandler),
    (r'/api/oauth/twitter/requestToken', api_oauth.TwitterRequestLoginHandler),
    (r'/api/oauth/twitter/credenciales/(.*)', api_oauth.TwitterHandler),

    (r'/api/oauth/facebook/login', api_oauth.FacebookLoginHandler),
    (r'/api/oauth/facebook/logout', api_oauth.FacebookLogoutHandler),
    (r'/api/oauth/facebook/credenciales/(.*)', api_oauth.FacebookHandler),
    
    (r'/api/oauth/googleplus/login', api_oauth.GooglePlusLoginHandler),
    (r'/api/oauth/googleplus/logout', api_oauth.GooglePlusLogoutHandler),
    (r'/api/oauth/googleplus/credenciales/(.*)', api_oauth.GooglePlusHandler),
    
    (r'/api/oauth/stackoverflow', api_oauth.StackOverflowContainerHandler),
    (r'/api/oauth/stackoverflow/credenciales/(.*)', api_oauth.StackOverflowHandler),

    (r'/api/oauth/github', api_oauth.GitHubContainerHandler),
    (r'/api/oauth/github/credenciales/(.*)', api_oauth.GitHubHandler),

    (r'/api/oauth/linkedin', api_oauth.LinkedinContainerHandler),
    (r'/api/oauth/linkedin/credenciales/(.*)', api_oauth.LinkedinHandler),

    (r'/api/oauth/instagram', api_oauth.InstagramContainerHandler),
    (r'/api/oauth/instagram/credenciales/(.*)', api_oauth.InstagramHandler),

    (r'/api/subscriptions', api_contacto.SubscriptionHandler),

    ], debug=True)

