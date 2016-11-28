#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
import sys
import time
import hashlib
sys.path.insert(0, '../')
import ndb_pb as schemas
# Probar a Insertar un usuario

#def setUp(self):

class TestMongoDB(unittest.TestCase):
  def testInsert(self):
    datos = {"email":"lruiz@conwet.com","phone": 61472589, "description":"Este es mi perfil personal","image": "www.example.com/mi-foto.jpg"}
    key = schemas.insertUser("twitter", "lrr9204", "asdfghjklm159753", datos)
    
    self.assertTrue(key, 'El usuario no se ha creado correctamente')
    self.assertEqual(key.email,datos['email'], 'El email del objeto no es igual al definido')
    self.assertEqual(key.phone,datos['phone'], 'El telefono del objeto no es igual al definido')
    self.assertEqual(key.description, datos['description'], 'La descripcion del objeto no es igual al definido')
    self.assertEqual(key.image,datos['image'], 'La imagen del objeto no es igual al definido')
    
    tok = schemas.getToken('lrr9204', "twitter")
    self.assertTrue(tok,'Existe un token');
    schemas.insertToken(key.id, "facebook", "poiuytrewq12345", 'lrr9204')

    tok_f = schemas.getToken('lrr9204', "facebook")
    self.assertTrue(tok_f, 'Existe el token de facebook')
  
  def testLogin(self):
    access_token = "ya29.CjOkA2X3E7QkCsuoT1XhpFSc_9LfqA5cpkJBqccpIzDlFjsLXgtqDgxwhVk7fQUYgxOrCp8"
    token_id = "113947794467742890905"
    user_identifier = "113947794467742890905"
    social_network = 'googleplus'
    user_key = schemas.user_key = schemas.insertUser(social_network,
                            token_id, access_token, {})
    message = str(user_key.id) + str(time.time())
    cypher = hashlib.sha256(message)
    hash_id = cypher.hexdigest()
    # Store in memcache hash-user_id pair
    # memcache.add(hash_id, user_key)
    # Create a new session in the system
    schemas.createSession(str(user_key.id), hash_id)
  def tearDown(self):
    schemas.dropDB()
  
if __name__ == '__main__':
        unittest.main()