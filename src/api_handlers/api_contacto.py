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
import json
import httplib
import ndb_pb

# Imports for ContactHandler
from google.appengine.api import mail


class ContactHandler(webapp2.RequestHandler):
    """ Class that represent the contact resource, used for customer support.
    Method:
    post -- Sends an email to deus@conwet.com with the info specified in the request.
    """
    def post(self):
        """ Sends an email to deus@conwet.com with the info specified in the request.
            Keyword arguments: 
                self -- info about the request built by webapp2
        """
        # Get params
        # Subject is an optional param
        try:
            subject = self.request.POST['subject']
            message = self.request.POST['message']
            sender = self.request.POST['sender']
            # Sends an email to deus@conwet
            subject = 'Contacto: ' + subject + ', de: ' + sender
            mail.send_mail('deus@conwet.com', 'deus@conwet.com', subject, message)
            self.response.set_status(201)
        except KeyError:
            response = {'error': 'You must provide a sender and message param'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))
            self.response.set_status(400)
        

class SubscriptionHandler(webapp2.RequestHandler):
    """ Handler for the subscription resource
    Method:
    post -- Creates a new subscription to the system.
    """
    
    # POST Method
    def post(self):
        """ Creates a new subscription to the system.
            Keyword arguments: 
                self -- info about the request built by webapp2
        """
        try:
            # Get params
            email = self.request.POST['email']
            name = self.request.POST['name']
            surname = self.request.POST['surname']
            if not ndb_pb.usuarioSuscrito(email):
                ndb_pb.nuevoUsuarioBeta(email, name, surname)
                self.response.set_status(201)
            else:
                self.response.set_status(200)
        except KeyError:
            response = {'error': 'You must provide an email, name and surname as params in the request'}
            self.response.content_type = 'application/json'
            self.response.write(json.dumps(response))    
            self.response.set_status(400)
