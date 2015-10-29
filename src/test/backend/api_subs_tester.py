# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de subscripciones de PicBit (api/subscriptions)
# Uso: ./api_subs_tester

# Las pruebas se realizan en la version "test-backend"
connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
headers = {"User-Agent": "PicBit-App"}

def make_request(method, request_uri, params, status_ok):
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
  	responseData = response.read()
  	if not response.status == status_ok:
  		print ">>> STATUS: ERROR!! " + str(response.status)
  		print responseData
  	else:
  		print ">>> STATUS: OK"

def main():
	basePath = "/api/subscriptions"
	params = urllib.urlencode({})

	# TEST 1
	# Añadir usuario nuevo a la beta
	request_uri = basePath + "?name=Ana&surname=Lopera&email=alopera@conwet.com"
	print "\nTEST 1: Haciendo petición POST a " + request_uri + " (Añadir nuevo usuario a la beta)\n Status esperado: 201"
	params = urllib.urlencode({'name': 'Ana Isabel', 'surname': 'Lopera','email':'TEST@example.com'})
	session = make_request("POST", request_uri, params, 201)

	# TEST 2
	print "\nTEST 2: Haciendo petición POST a " + request_uri + " (Usuario ya añadido al sistema)\n Status esperado: 200"
	make_request("POST", request_uri, params,200)

	# TEST 3
	# Caso de error
	request_uri = basePath + "?name=Ana&surname=Lopera"
	params = urllib.urlencode({'name': 'Ana Isabel', 'surname': 'Lopera'})
	print "\nTEST 3: Haciendo petición POST a " + request_uri + " (Peticion sin parametro email)\n Status esperado: 400"
	make_request("POST", request_uri, params,400)

	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()
