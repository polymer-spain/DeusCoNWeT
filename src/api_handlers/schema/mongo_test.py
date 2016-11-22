#!/usr/bin/python
# -*- coding: utf-8 -*-

import schemas
import unittest

# Probar a Insertar un usuario

#def setUp(self):

class TestMongoDB(unittest.TestCase):
  def testInsert(self):
    datos = {"email":"lruiz@conwet.com","phone": 61472589, "description":"Este es mi perfil personal","image": "www.example.com/mi-foto.jpg"}
    id, key = schemas.insertUser("twitter", "lrr9204", "asdfghjklm159753", datos)
    
    self.assertTrue(key, 'El usuario no se ha creado correctamente')
    self.assertEqual(key.email,datos['email'], 'El email del objeto no es igual al definido')
    self.assertEqual(key.phone,datos['phone'], 'El telefono del objeto no es igual al definido')
    self.assertEqual(key.description, datos['description'], 'La descripcion del objeto no es igual al definido')
    self.assertEqual(key.image,datos['image'], 'La imagen del objeto no es igual al definido')
    
    tok = schemas.getToken('lrr9204', "twitter")
    self.assertTrue(tok,'Existe un token');
    schemas.insertToken('lrr9294', "facebook", "poiuytrewq12345", "Luis Ruiz")

    tok_f = schemas.getToken('lrr9294', "facebook")
    self.assertTrue(tok_f, 'Existe el token de facebook')

  #def tearDown(self):
    # TODO drop database
    
if __name__ == '__main__':
        unittest.main()