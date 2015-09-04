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
import urllib2

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


class instagramRequest(webapp2.RequestHandler):
  def get(self):
    access_token = self.request.get("access_token", default_value="")
    count = self.request.get("count", default_value="")
    min_id = self.request.get("min_id", default_value="")
    max_id = self.request.get("max_id", default_value="")
#    media_id = self.request.get("media_id", default_value="")

#    print(media_id)
    peticion = "https://api.instagram.com/v1/users/self/feed?access_token="+access_token

    #Peticion basica
    if (count == "" and min_id == "" and max_id == ""):
      respuesta = urllib2.urlopen(peticion).read()
    #Recargar datos
    elif (min_id != ""):
      respuesta = urllib2.urlopen(peticion+"&min_id="+min_id).read()
#    elif (media_id != ""):
#      peticion = "https://api.instagram.com/v1"
#      respuesta = urllib2.urlopen(peticion+"/media/"+media_id+"/likes").read()
    #Cargar mas datos
    else:
      respuesta = urllib2.urlopen(peticion+"&max_id="+max_id+"&count="+count).read()
    self.response.write(respuesta)
