# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de Oauth de PicBit (api/oauth/{red_social})
# Uso: ./api_oauth_tester red_social

# NOTA: El flujo por github se debe probar a traves del componente de login de github
#       (http://github-login-lab.appspot.com/app/demo.html)

connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")

def make_request(method, request_uri, params, status_ok, session):
	headers = {"User-Agent": "PicBit-App"}
	session_cookie = None
	if not session == None:
		headers['Cookie']  = session
		print "\tHEADERS " + headers['Cookie']
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
	session_cookie = response.getheader('Set-Cookie')
  	responseData = response.read()
  	if not response.status == status_ok:
  		print "\t!!! STATUS: ERROR " + str(response.status)
  		print "\tDatos de la respuesta: "
  		print responseData
  	else:
  		print "\t>>> STATUS: OK"
  		print "\tRESPUESTA: ", responseData
  	#print "Cookie de la peticion: " + str(headers['Cookie'])
	if not session_cookie == None:
  		print "\tCookie de la respuesta: " + session_cookie
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

		# TEST 4
		# Obtener credenciales con cookie	
		request_uri = basePath
		print "\nTEST 4: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie de sesion)\n Status esperado: 200"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,200, session)		


		#Logouts
		# TEST 5
		request_uri = basePath + "?action=logout"
		print "\nTEST 5: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("POST", request_uri, params,400, None)

		# TEST 6
		print "\nTEST 6: Haciendo petición POST a " + request_uri + " (logout con cookie de sesion)\n Status esperado: 200"
		# Se desloguea el usuario logueado en el test1
		request_uri = basePath + "?action=logout"
		make_request("POST", request_uri, params,200,session)
		
		# TEST 7
		# Get (Sin cookie)
		request_uri = basePath
		print "\nTEST 7: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,400, None)

		# TEST 8
		# Login (prueba de nueva sesión y actualizar credenciales)
		request_uri = basePath + "?action=login"
		print "\nTEST 8: Haciendo petición POST a " + request_uri + " (prueba de nueva sesión y actualizar credenciales)\n Status esperado: 200"
		token_id = "id" + red_social
		access_token = red_social + "Modify2TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})	
		make_request("POST", request_uri, params,200, None)


		# TODO TEST 9 
		# Obtener credenciales con cookies antiguas
		request_uri = basePath
		print "\nTEST 9: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie antigua)\n Status esperado: 400"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params,400, session)

		# TODO TEST 10 
		# Logout con cookie antigua (tiene que borrar la cookie y devolver un 200)
		request_uri = basePath + "?action=logout"
		print "\nTEST 10: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 200"
		params = urllib.urlencode({})
		make_request("POST", request_uri, params,200, session)

		print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"

	elif red_social=="stackoverflow" or red_social=="instagram" or red_social=="linkedin":
		session = None

		# Iniciamos sesion en googleplus para realizar las pruebas
		request_uri = "/api/oauth/googleplus?action=login"
		print "\n PRETEST: Haciendo petición POST a " + request_uri + " (login)\n Ignorar el status de este caso"
		token_id = "idgoogle"
		access_token = "googleTEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		session = make_request("POST", request_uri, params, 201, None)

		# Tests a la API seleccionada
		request_uri = "/api/oauth/" + red_social
		# TEST 1
		# Añadir credenciales nuevas al sistema
		print "\nTEST 1: Haciendo petición POST a " + request_uri + " (añadir nuevo par de credenciales)\n Status esperado: 201"
		token_id = "id" + red_social
		access_token = red_social + "TEST"
		params = urllib.urlencode({'token_id': token_id, 'access_token':access_token})
		make_request("POST", request_uri, params, 201, None)

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

		print "\nTEST 5: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie)\n Status esperado: 200"
		params = urllib.urlencode({})
		make_request("GET", request_uri, params, 200, session)	

		print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"

	else:
		print "Error: es obligatorio proporcionar un parámetro válido para indicar que red social se pretende testear"
		print "Uso: python api_oauth_tester.py {googleplus|stackoverflow|facebook|instagram|linkedin|twitter}"

	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()