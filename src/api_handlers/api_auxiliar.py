# -*- coding: utf8 -*-
#!/usr/bin/env python


import webapp2
import urllib2, httplib
import sys

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
