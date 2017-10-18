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
from twython import Twython, exceptions
import mongoDB
from mongoDB import User, FacebookPosts, Token
import urllib2
import urllib
import json
import yaml
import os
import datetime

basepath = os.path.dirname(__file__)
configFile = os.path.abspath(os.path.join(basepath, "config.yaml"))
with open(configFile, "r") as ymlfile:
    cfg = yaml.load(ymlfile)


class OAuthTwitterTimelineHandler(webapp2.RequestHandler):

    def get(self):
        consumer_key = self.request.get('consumer_key', default_value='')
        consumer_secret = self.request.get('consumer_secret', default_value='')
        access_token = self.request.get('access_token', default_value='')

        cookie_value = self.request.cookies.get("session")
        # Check if the user cookies
        if not cookie_value:
            self.response.content_type = "application/json"
            response = {'error':'Could not authenticate you. Cookie session missing'}
            self.response.write(json.dumps(response))
            self.response.set_status(401)
        else:
            userInfo = mongoDB.getSessionOwner(cookie_value)
            userSession = User.objects(id=userInfo)
            if len(userSession) == 0:
                self.response.content_type = "application/json"
                response = {'error':'Invalid session cookie'}
                self.response.write(json.dumps(response))
                self.response.set_status(401)
                count = self.request.get('count', default_value='20')
                return None
            tokens = userSession[0]['tokens']
            twitter_token = None

            for token in tokens:
                if token['social_name'] == 'twitter':
                    twitter_token = token
            print "Token encontrado", twitter_token
            if not twitter_token:
                self.response.content_type = "application/json"
                response = {'error':'Access token is not valid'}
                self.response.write(json.dumps(response))
                self.response.set_status(401)
                count = self.request.get('count', default_value='20')
            else:
                secret = mongoDB.getSecret(twitter_token)
                print access_token, secret, consumer_key, consumer_secret
                tw = Twython(consumer_key, consumer_secret, access_token, secret)
                try:
                    response = tw.get_home_timeline()
                    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
                    self.response.headers['Content-Type'] = 'application/json'
                    self.response.write(json.dumps(response))
                    self.response.set_status(200)
                except exceptions.TwythonAuthError:
                    self.response.content_type = "application/json"
                    response = {'error':'Could not authenticate you'}
                    self.response.write(json.dumps(response))
                    self.response.set_status(401)

class OAuthFacebookAccessToken(webapp2.RequestHandler):
  def get(self):
    access_token = self.request.get("access_token", default_value="")
    if not access_token:
      self.response.headers.add_header('Access-Control-Allow-Origin', '*')
      self.response.headers['Content-Type'] = 'application/json'
      response = {'error':'access_token is required'}
      self.response.write(json.dumps(response))
      self.response.set_status(404)
    
    else:
      url = "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" % (cfg['APP_ID'], cfg['APP_SECRET'], access_token)
      print url
      response = urllib2.urlopen(url).read()
      self.response.headers.add_header('Access-Control-Allow-Origin', '*')
      self.response.headers['Content-Type'] = 'application/json'
      self.response.write(response)


class OAuthFacebookTimeline(webapp2.RequestHandler):
    def get(self):
      access_token = self.request.get("access_token", default_value="")
      locale = self.request.get("locale", default_value="es_es")

      # Check if access token is missing
      if not access_token:
        self.response.headers.add_header('Access-Control-Allow-Origin', '*')
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write({"error":"access_token is required"})
        self.response.set_status(400)
      else:
        # Get facebook config
        url = cfg['FACEBOOK_CONFIG']['url']
        params ={}
        params['fields'] = cfg['FACEBOOK_CONFIG']['fields']
        params['locale'] = locale
        params['access_token'] = access_token
        try:
          # Try to get the user posts and user id
          url = "%s?%s" % (url, urllib.urlencode(params))
          responseTimeline = urllib2.urlopen(url)
          posts = responseTimeline.read()
          responseTimeline.close()
          
          # Get user_id
          url_id = cfg['FACEBOOK_CONFIG']['url_id'] + '&access_token='+ access_token
          response = urllib2.urlopen(url_id)
          responseId = json.loads(response.read())
          response.close()
          user_id = responseId['id']

          # Register posts
          mongoDB.createPosts(user_id, json.loads(posts))
          
          # Get friends
          url_friends = cfg['FACEBOOK_CONFIG']['url_friends'] + "?access_token=" + access_token
          response = urllib2.urlopen(url_friends)
          responseFriends = json.loads(response.read())
          
          # Get all post of your friends
          user_list = [ str(user['id']) for user in responseFriends['data'] ]
          print user_list

          # Get all post of your friends (based on cache)                 
          friends_posts = FacebookPosts.objects(user_id__in=user_list)
          friends_posts = [ json.loads(str(post['post'])) for post in friends_posts]
          print len(friends_posts)
          post_json = json.loads(posts)
          
          # sort by date
          all_post = friends_posts + post_json['data']
          all_post.sort(key=lambda k: k['updated_time'], reverse=True )

          self.response.headers.add_header('Access-Control-Allow-Origin', '*')
          self.response.headers['Content-Type'] = 'application/json'
          self.response.write(json.dumps(all_post))

        except urllib2.HTTPError as e:
          self.response.headers.add_header('Access-Control-Allow-Origin', '*')
          self.response.headers['Content-Type'] = 'application/json'
          self.response.set_status(e.code)
          self.response.write(e.read())



class instagramRequest(webapp2.RequestHandler):
  def get(self):
    access_token = self.request.get("access_token", default_value="")
    count = self.request.get("count", default_value="")
    min_id = self.request.get("min_id", default_value="")
    max_id = self.request.get("max_id", default_value="")
    #   media_id = self.request.get("media_id", default_value="")
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

    self.response.headers.add_header('Access-Control-Allow-Origin', '*')
    self.response.headers['Content-Type'] = 'application/json'
    self.response.write(respuesta)
