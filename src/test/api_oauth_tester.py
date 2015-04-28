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
		headers['Set-Cookie']  = "session=" + session
		print "HEADERS " + headers['Set-Cookie']
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
  	responseData = response.read()
  	if not response.status == status_ok:
  		print ">>> STATUS: ERROR!! " + str(response.status)
  		print responseData
  	else:
  		print ">>> STATUS: OK"
  		session_cookie = response.getheader('Set-Cookie')
  		print session_cookie
  	return session_cookie

def main():
	red_social=sys.argv[1]
	if red_social == "googleplus" or redsocial=="facebook":
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

		# TEST 2
		request_uri = basePath + "?action=login"
		print "\nTEST 2: Haciendo petición POST a " + request_uri + " (login de sesion iniciada anteriormente)\n Status esperado: 200"
		token_id = "id" + red_social
		access_token = red_social + "ModifyTEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		make_request("POST", request_uri, params,200, None)	

		# TEST 3
		request_uri = basePath + "?action=login"
		print "\nTEST 3: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
		token_id = "id" + red_social + "2"
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token': access_token})
		make_request("POST", request_uri, params,201, None)

		#Logouts
		# TEST 4
		request_uri = basePath + "?action=logout"
		print "\nTEST 4: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("POST", request_uri, params,400, None)

		# TEST 5
		print "\nTEST 5: Haciendo petición POST a " + request_uri + " (logout con cookie de sesion)\n Status esperado: 200"
		# Se desloguea el usuario logueado en el test1
		request_uri = basePath + "?action=logout"
		make_request("POST", request_uri, params,200,session)

		# TEST 6
		# Get (Sin cookie)
		request_uri = basePath + "?action=login"
		print "\nTEST 6: Haciendo petición GET a " + request_uri + " (obtener credenciales)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,400, None)

		# TEST 7
		# Login (prueba de nueva sesión y actualizar credenciales)
		request_uri = basePath + "?action=login"
		print "\nTEST 7: Haciendo petición POST a " + request_uri + " (prueba de nueva sesión y actualizar credenciales)\n Status esperado: 200"
		token_id = "id" + red_social
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})	
		make_request("POST", request_uri, params,200, None)	

	elif red_social=="stackoverflow" or red_social=="instagram" or red_social=="linkedin"
	basePath = "/api/oauth/" + red_social
		session = None
		#Logins
		# TEST 1
		request_uri = basePath + "?action=login"
		print "\nTEST 1: Haciendo petición POST a " + request_uri + " (añadir nuevo par de credenciales)\n Status esperado: 201"
		token_id = "id" + red_social
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		session = make_request("POST", request_uri, params, 201, None)

		# TEST 2
		request_uri = basePath + "?action=login"
		print "\nTEST 2: Haciendo petición POST a " + request_uri + " (login de sesion iniciada anteriormente)\n Status esperado: 200"
		token_id = "id" + red_social
		access_token = red_social + "ModifyTEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		make_request("POST", request_uri, params,200, None)	

		# TEST 3
		request_uri = basePath + "?action=login"
		print "\nTEST 3: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
		token_id = "id" + red_social + "2"
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token': access_token})
		make_request("POST", request_uri, params,201, None)

		# TEST 6
		# Get (Sin cookie)
		request_uri = basePath + "?action=login"
		print "\nTEST 6: Haciendo petición GET a " + request_uri + " (obtener credenciales)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,400, None)



	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()