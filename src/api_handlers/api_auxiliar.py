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
# Imports for OAuthTwitterTimelineHandler
import oauth

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