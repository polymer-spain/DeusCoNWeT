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

    (r'/api/subscriptions', api_contacto.SubscriptionHandler),

    ], debug=True)

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
import re
import pprint as pp
sys.path.insert(1, 'api_handlers/')
sys.path.insert(1, 'api_handlers/lib/')
import yaml
import api_usuarios, api_componentes, api_oauth, api_auxiliar
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
class redirect(webapp2.RequestHandler):
    def get(self):
        print self.request
def handlerStaticUrl(file):
    class handler(webapp2.RequestHandler):
        def get(self):
            path = os.path.join(basepath,file)
            f = open(path,'r')
            self.response.out.write(f.read())
    return handler  
    
def createStatic(handler):
    url = handler['url']
    file = handler['static_files']
    return (url, handlerStaticUrl(file))

static_url = [ url for url in cfg['handlers'] if url.has_key('static_files')]
static_url = [createStatic(handler) for handler in static_url]
## LOAD APP
full_url = api_url + static_url
web_app = webapp2.WSGIApplication(full_url, debug=True)

## MAIN
def main():
    from paste import httpserver
    from paste.cascade import Cascade
    from paste.urlparser import StaticURLParser
    import threading
    
    threads = list()

    # Deploy app
    ssl = os.path.abspath(os.path.join(basepath, 'ssl/ssl.pem'))
    static_app = StaticURLParser("static/")
    app = Cascade([static_app,web_app])
    
    # thread worker
    def worker(server_type):
        if server_type == 'http':
            http_app = webapp2.WSGIApplication([(r'*', redirect)])
            httpserver.serve(http_app, host='0.0.0.0', port=80 , server_version=1.0)
        else:
            httpserver.serve(app, host='0.0.0.0', port=443 , server_version=1.0,ssl_pem=ssl)
    
    # Define threads: http and https server
    t_http = threading.Thread(target=worker,args=('http',))
    t_https = threading.Thread(target=worker, args=('https',))
    print t_http
    print t_https
    # Init threads
    t_http.start()
    t_https.start()
if __name__ == '__main__':
    main()
