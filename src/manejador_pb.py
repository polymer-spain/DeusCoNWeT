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
import api_usuarios, api_componentes, api_contacto, api_oauth_refactored, api_auxiliar


app = webapp2.WSGIApplication([
    (r'/api/componentes', api_componentes.ComponentListHandler),
    (r'/api/componentes/(.*)', api_componentes.ComponentHandler),
    
    (r'/api/usuarios', api_usuarios.UserListHandler),
    (r'/api/usuarios/(.*)', api_usuarios.UserHandler),
    
    (r'/api/aux/twitterTimeline', api_auxiliar.OAuthTwitterTimelineHandler),
    
    (r'/api/oauth/twitter', api_oauth_refactored.TwitterContainerHandler),
    (r'/api/oauth/twitter/login', api_oauth_refactored.TwitterLoginHandler),
    (r'/api/oauth/twitter/logout', api_oauth_refactored.TwitterLogoutHandler),
    (r'/api/oauth/twitter/authorization', api_oauth_refactored.TwitterAuthorizationHandler),
    (r'/api/oauth/twitter/requestToken', api_oauth_refactored.TwitterRequestLoginHandler),
    (r'/api/oauth/twitter/(.*)', api_oauth_refactored.TwitterHandler),

    (r'/api/oauth/facebook/login', api_oauth_refactored.FacebookLoginHandler),
    (r'/api/oauth/facebook/logout', api_oauth_refactored.FacebookLogoutHandler),
    (r'/api/oauth/facebook/(.*)', api_oauth_refactored.FacebookHandler),
    
    (r'/api/oauth/googleplus/login', api_oauth_refactored.GooglePlusLoginHandler),
    (r'/api/oauth/googleplus/logout', api_oauth_refactored.GooglePlusLogoutHandler),
    (r'/api/oauth/googleplus/(.*)', api_oauth_refactored.GooglePlusHandler),
    
    (r'/api/oauth/stackoverflow', api_oauth_refactored.StackOverflowContainerHandler),
    (r'/api/oauth/stackoverflow/(.*)', api_oauth_refactored.StackOverflowHandler),

    (r'/api/oauth/github', api_oauth_refactored.GitHubContainerHandler),
    (r'/api/oauth/github/(.*)', api_oauth_refactored.GitHubHandler),

    (r'/api/oauth/linkedin', api_oauth_refactored.LinkedinContainerHandler),
    (r'/api/oauth/linkedin/(.*)', api_oauth_refactored.LinkedinHandler),

    (r'/api/oauth/instagram', api_oauth_refactored.InstagramContainerHandler),
    (r'/api/oauth/instagram/(.*)', api_oauth_refactored.InstagramHandler),

    (r'/api/subscriptions', api_contacto.SubscriptionHandler),
    ], debug=True)
