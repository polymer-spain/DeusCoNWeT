# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de Oauth de PicBit (api/oauth/{red_social})
# Uso: ./api_oauth_tester red_social

connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
headers = {"User-Agent": "PicBit-App"}

def make_request(method, request_uri, params, status_ok, session):
	session_cookie = None
	if not session == None:
		headers['Cookie']  = session
		print "HEADERS " + headers['Cookie']
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
  	responseData = response.read()
  	if not response.status == status_ok:
  		print "!!! STATUS: ERROR " + str(response.status)
  		print responseData
  	else:
  		print ">>> STATUS: OK"
  		session_cookie = response.getheader('Set-Cookie')
  		print session_cookie
  	return session_cookie

def main():
	red_social=sys.argv[1]
	if red_social == "googleplus" or red_social=="facebook":
		basePath = "/api/oauth/" + red_social
		session = None
		#Logins
		# TEST 1
		request_uri = basePath + "?action=login"
		print "\nTEST 1: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
		token_id = "id" + red_social
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		session = make_request("POST", request_uri, params, 201, None)

		# # TEST 2
		# request_uri = basePath + "?action=login"
		# print "\nTEST 2: Haciendo petición POST a " + request_uri + " (login de sesion iniciada anteriormente)\n Status esperado: 200"
		# token_id = "id" + red_social
		# access_token = red_social + "ModifyTEST"
		# params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		# make_request("POST", request_uri, params,200, None)	

		# # TEST 3
		# request_uri = basePath + "?action=login"
		# print "\nTEST 3: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
		# token_id = "id" + red_social + "2"
		# access_token = red_social + "TEST"
		# params = urllib.urlencode({'token_id': token_id, 'access_token': access_token})
		# make_request("POST", request_uri, params,201, None)

		# TEST 4
		# Obtener credenciales con cookie	
		request_uri = basePath
		print "\nTEST 4: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie de sesion)\n Status esperado: 200"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,200, session)		

		# #Logouts
		# # TEST 5
		# request_uri = basePath + "?action=logout"
		# print "\nTEST 5: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
		# params = urllib.urlencode({})
		# make_request("POST", request_uri, params,400, None)

		# # TEST 6
		# print "\nTEST 6: Haciendo petición POST a " + request_uri + " (logout con cookie de sesion)\n Status esperado: 200"
		# # Se desloguea el usuario logueado en el test1
		# request_uri = basePath + "?action=logout"
		# make_request("POST", request_uri, params,200,session)
		
		# # TEST 7
		# # Get (Sin cookie)
		# request_uri = basePath
		# print "\nTEST 7: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 400"
		# params = urllib.urlencode({})
		# make_request("GET", request_uri, params,400, None)

		# # TEST 8
		# # Login (prueba de nueva sesión y actualizar credenciales)
		# request_uri = basePath + "?action=login"
		# print "\nTEST 8: Haciendo petición POST a " + request_uri + " (prueba de nueva sesión y actualizar credenciales)\n Status esperado: 200"
		# token_id = "id" + red_social
		# access_token = red_social + "Modify2TEST"
		# params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})	
		# make_request("POST", request_uri, params,200, None)

		# TODO TEST 9 
		# Obtener credenciales con cookies antiguas
		request_uri = basePath
		print "\nTEST 9: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 404"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,404, session)

		# # TODO TEST 10 
		# # Logout con cookie antigua (tiene que borrar la cookie y devolver un 200)
		# request_uri = basePath + "?action=logout"
		# print "\nTEST 10: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 200"
		# params = urllib.urlencode({})
		# make_request("POST", request_uri, params,200, session)

		print "TESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"

	elif red_social=="stackoverflow" or red_social=="instagram" or red_social=="linkedin":
		request_uri = "/api/oauth/" + red_social
		session = None
		# TEST 1
		# Añadir credenciales nuevas al sistema
		print "\nTEST 1: Haciendo petición POST a " + request_uri + " (añadir nuevo par de credenciales)\n Status esperado: 201"
		token_id = "id" + red_social
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		session = make_request("POST", request_uri, params, 201, None)

		# TEST 2
		print "\nTEST 2: Haciendo petición POST a " + request_uri + " (actualizar credenciales)\n Status esperado: 200"
		token_id = "id" + red_social
		access_token = red_social + "ModifyTEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		make_request("POST", request_uri, params,200, None)	

		# TEST 3
		print "\nTEST 3: Haciendo petición POST a " + request_uri + " (actualizar credenciales proporcionando un solo parametro)"
		print "Status esperado: 400"
		token_id = "idERROR" + red_social + "2"
		params = urllib.urlencode({'token_id': token_id})
		make_request("POST", request_uri, params,400, None)

		# TEST 4
		# Get (Sin cookie)
		print "\nTEST 4: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,400, None)

		# TEST 5
		# TODO Get (Con Cookie)

		print "TESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"

	elif red_social == "github":
		# Prueba de flujo de login completo
		print "Accede a la siguiente dirección en tu navegador:"
		request_uri = "/api/oauth/github?action=request_token"
		params = urllib.urlencode({})
		headers = {"User-Agent": "PicBit-App"}
		connection.request("POST", request_uri, params, headers)
  		response = connection.getresponse()
  		responseData = response.read()

	else:
		print "Error: es obligatorio proporcionar un parámetro válido para indicar que red social se pretende testear"
		print "Uso: python api_oauth_tester.py {googleplus|stackoverflow|facebook|instagram|linkedin|github|twitter}"
	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()