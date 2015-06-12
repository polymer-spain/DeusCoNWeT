# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de Oauth de PicBit (api/oauth/{red_social})
# Uso: ./api_oauth_tester red_social
# NOTA: El flujo por github se debe probar a traves del componente de login de github
#       (http://github-login-lab.appspot.com/app/demo.html)

connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
# connection = httplib.HTTPConnection("localhost:8080")

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
	red_social = sys.argv[1]
	opcion = None
	if len(sys.argv) == 3:
		opcion = sys.argv[2]
	if red_social == "googleplus" or red_social=="facebook":
		basePath = "/api/oauth/" + red_social
		session1 = None
		session2 = None
		token_id1 = "id" + red_social
		token_id2 = "id" + red_social + "2"
		if opcion == None:
			#Logins
			# TEST 1
			request_uri = basePath + "/login"
			print "\nTEST 1: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
			access_token = red_social + "TEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token})
			session1 = make_request("POST", request_uri, params, 201, None)

			# TEST 2
			request_uri = basePath + "/login"
			print "\nTEST 2: Haciendo petición POST a " + request_uri + " (login de sesion iniciada anteriormente)\n Status esperado: 200"
			access_token = red_social + "ModifyTEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token})
			make_request("POST", request_uri, params,200, None)	

			# TEST 3
			request_uri = basePath + "/login"
			print "\nTEST 3: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
			access_token = red_social + "TEST"
			params = urllib.urlencode({'token_id': token_id2, 'access_token': access_token})
			make_request("POST", request_uri, params,201, None)

			# GETs de credenciales
			# TEST 4
			# Obtener credenciales con cookie	
			request_uri = basePath + "/" + token_id2
			print "\nTEST 4: Haciendo petición GET a " + request_uri 
			print " (obtener credenciales con cookie de sesion, a una credencial que no es propiedad del usuario)"
			print "Status esperado: 401"
			params = urllib.urlencode({})
			make_request("GET", request_uri, params, 401, session1)

			# Obtener credenciales con cookie
			# TEST 5	
			request_uri = basePath + "/" + token_id1
			print "\nTEST 5: Haciendo petición GET a " + request_uri 
			print " (obtener credenciales con cookie de sesion, a una credencial propiedad del usuario)"
			print " Status esperado: 200"
			params = urllib.urlencode({})
			make_request("GET", request_uri, params, 200, session1)

			#Logouts
			# TEST 6
			request_uri = basePath + "/logout"
			print "\nTEST 6: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
			params = urllib.urlencode({})
			make_request("POST", request_uri, params,400, None)

			# TEST 7
			print "\nTEST 7: Haciendo petición POST a " + request_uri + " (logout con cookie de sesion)\n Status esperado: 200"
			# Se desloguea el usuario logueado en el test1
			request_uri = basePath + "/logout"
			make_request("POST", request_uri, params,200,session1)
			
			# TEST 8
			# Get (Sin cookie)
			request_uri = basePath + "/" + token_id2
			print "\nTEST 8: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 400"
			params = urllib.urlencode({})
			make_request("GET", request_uri, params,400, None)

			# TEST 9
			# Login (prueba de nueva sesión y actualizar credenciales)
			request_uri = basePath + "/login"
			print "\nTEST 9: Haciendo petición POST a " + request_uri + " (prueba de nueva sesión y actualizar credenciales)\n Status esperado: 200"
			access_token = red_social + "Modify2TEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token})	
			make_request("POST", request_uri, params,200, None)

			# TEST 10
			# Obtener credenciales con cookies antiguas
			request_uri = basePath + "/" + token_id1
			print "\nTEST 10: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie antigua)\n Status esperado: 400"
			params = urllib.urlencode({})
			make_request("GET", request_uri, params,400, session1)

			# TEST 11 
			# Logout con cookie antigua
			request_uri = basePath + "/logout"
			print "\nTEST 11: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
			params = urllib.urlencode({})
			make_request("POST", request_uri, params,400, None)
			print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"
		
		elif opcion == "borrar":
			# PRE-TEST 1: Login en el sistema de usuario de prueba 1
			request_uri = basePath + "/login"
			print "\nPRE-TEST 1: Haciendo petición POST a " + request_uri
			print " (Login en el sistema de usuario de prueba 1)\n Status esperado: 200"
			access_token = red_social + "tokenTODELETE1"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token})	
			session1 = make_request("POST", request_uri, params,200, None)

			# TEST 12
			# Borrar credenciales de usuarios de prueba2
			request_uri = basePath + "/" + token_id2
			print "\nTEST 12: Haciendo petición DELETE a " + request_uri + " (Borrar creedenciales sin cookie de sesion)"
			print " Status esperado: 401"
			params = urllib.urlencode({})
			make_request("DELETE", request_uri, params,401, None)
			print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"
			
			# PRE-TEST 2: Login en el sistema de usuario de prueba 2
			request_uri = basePath + "/login"
			print "\nPRE-TEST 2: Haciendo petición POST a " + request_uri
			print " (Login en el sistema de usuario de prueba 1)\n Status esperado: 200"
			access_token = red_social + "tokenTODELETE2"
			params = urllib.urlencode({'token_id': token_id2, 'access_token':access_token})	
			session2 = make_request("POST", request_uri, params,200, None)

			# TEST 13
			# Borrar credenciales de usuario de prueba1 (Estando logeado)
			request_uri = basePath + "/" + token_id1
			print "\nTEST 13: Haciendo petición DELETE a " + request_uri + " (Borrado de credenciales estando logeado)"
			print " Status esperado: 204"
			params = urllib.urlencode({})
			make_request("DELETE", request_uri, params,204, session1)
			
			# TEST 14
			# Borrar credenciales de usuario de prueba2 (Con una cookie incorrecta)
			request_uri = basePath + "/" + token_id2
			print "\nTEST 13: Haciendo petición DELETE a " + request_uri + " (Borrado de credenciales estando logeado)"
			print " Status esperado: 401"
			params = urllib.urlencode({})
			make_request("DELETE", request_uri, params,401, session1)

			# TEST 15
			# Borrar credenciales de usuario de prueba2 (Estando logeado)
			request_uri = basePath + "/" + token_id2
			print "\nTEST 13: Haciendo petición DELETE a " + request_uri + " (Borrado de credenciales estando logeado)"
			print " Status esperado: 204"
			params = urllib.urlencode({})
			make_request("DELETE", request_uri, params,204, session2)

			# TEST 16
			# Borrar credenciales de usuario de prueba 2 por segunda vez (Caso de error)
			request_uri = basePath + "/" + token_id2
			print "\nTEST 13: Haciendo petición DELETE a " + request_uri + " (Intento de borado por segunda vez)"
			print " Status esperado: 404"
			params = urllib.urlencode({})
			make_request("DELETE", request_uri, params,404, session2)

			# POST-TEST 1: Realizar logout en el sistema (usuario 1)
			request_uri = basePath + "/logout"
			print "\nPOST-TEST 1: Haciendo petición POST a " + request_uri + " (logout de usuario 1 con cookie de sesion)"
			print " Status esperado: 200"
			# Se desloguea el usuario logueado en el PRE TEST 1
			make_request("POST", request_uri, params,200,session1)

			# POST-TEST 2: Realizar logout en el sistema (usuario 2)
			request_uri = basePath + "/logout"
			print "\nPOST-TEST 2: Haciendo petición POST a " + request_uri + " (logout de usuario 1 con cookie de sesion)"
			print " Status esperado: 200"
			# Se desloguea el usuario logueado en el PRE TEST 2
			make_request("POST", request_uri, params,200,session2)

			print "\nTESTs finalizados. Comprobar el borrado de las entidades de tipo Token en datastore"

	elif red_social=="stackoverflow" or red_social=="instagram" or red_social=="linkedin":
		session = None

		# Iniciamos sesion en googleplus para realizar las pruebas
		request_uri = "/api/oauth/googleplus/login"
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

		# # TEST 4
		# # Get (Sin cookie)
		# print "\nTEST 4: Haciendo petición GET a " + request_uri + " (obtener credenciales sin cookie)\n Status esperado: 400"
		# params = urllib.urlencode({})
		# make_request("GET", request_uri, params,400, None)

		# # TEST 5
		# # TODO Get (Con Cookie)
		# print "\nTEST 5: Haciendo petición GET a " + request_uri + " (obtener credenciales con cookie)\n Status esperado: 200"
		# params = urllib.urlencode({})
		# make_request("GET", request_uri, params, 200, session)	

		# # TODO TEST 6 borrar credenciales de usuario activo

		# print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"
	else:
		print "Error: es obligatorio proporcionar un parámetro válido para indicar que red social se pretende testear"
		print "Uso: python api_oauth_tester.py {googleplus|stackoverflow|facebook|instagram|linkedin|twitter}"
	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()