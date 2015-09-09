# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json
import test_utils


# Script para hacer pruebas a la API de Oauth de PicBit (api/oauth/{social_network})
# Uso: api_oauth_tester {social_network} [borrado]
# Ejemplo: python api_oauth_tester googleplus 

# NOTA: El flujo por github se debe probar a traves del componente de login de github
#       (http://github-login-lab.appspot.com/app/demo.html)

def main():
	test_utils.openConnection()
	social_network = sys.argv[1]
	option = None
	if len(sys.argv) == 3:
		option = sys.argv[2]
	if social_network == "googleplus" or social_network=="facebook":
		basePath = "/api/oauth/" + social_network
		session1 = None
		session2 = None
		token_id1 = "id" + social_network
		token_id2 = "id" + social_network + "2"
		user_id1 = "user" + social_network + "1"
		user_id2 = "user" + social_network + "2"
		access_token2 = social_network + "2TEST"
		# Si no se especifica una opción, se realizan las pruebas relativas al Login, 
		# obtención de credenciales y logout
		if option == None:
			#Tests relativos a los casos de Login
			# TEST 1
			request_uri = basePath + "/login"
			print "TEST 1: Login de sesión correcto (usuario 1)"
			print "Status esperado: 201"
			access_token = social_network + "TEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token': "TEST 1",
				'user_identifier': user_id1})
			session1 = test_utils.make_request("POST", request_uri, params, 201, None)

			# TEST 2
			print "TEST 2: Login de sesion iniciada anteriormente"
			print "Status esperado: 200"
			access_token = social_network + "ModifyTEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token': "TEST 2",
				'user_identifier': user_id1})
			test_utils.make_request("POST", request_uri, params, 200, None)	

			# TEST 3
			print "TEST 3: Login de usuario 2"
			print "Status esperado: 201"
			params = urllib.urlencode({'token_id': token_id2, 'access_token': "TEST 3",
				'user_identifier': user_id2})
			test_utils.make_request("POST", request_uri, params, 201, None)

			# Tests relativos al método GET de credenciales
			# TEST 4
			# Obtener credenciales con cookie	
			request_uri = basePath + "/credenciales/" + token_id2
			print "TEST 4: Obtener credenciales con cookie de sesion, a una credencial que no es propiedad del usuario"
			print "Status esperado: 200 (Solo retorna el id de usuario propietario del token)"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# Obtener credenciales con cookie
			# TEST 5	
			request_uri = basePath + "/credenciales/" + token_id1
			print "TEST 5: Obtener credenciales con cookie de sesion, a una credencial propiedad del usuario"
			print "Status esperado: 200"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session1)

			#Logouts
			# TEST 6
			request_uri = basePath + "/logout"
			print "TEST 6: Logout sin cookie de sesion"
			print "Status esperado: 401"
			params = urllib.urlencode({})
			test_utils.make_request("POST", request_uri, params, 401, None)

			# TEST 7
			# Se desloguea el usuario logueado en el test1
			print "TEST 7: Logout con cookie de sesion (usuario1)"
			print "Status esperado: 200"
			test_utils.make_request("POST", request_uri, params, 200, session1)
			
			# TEST 8
			# Get (Sin cookie)
			request_uri = basePath + "/credenciales/" + token_id2
			print "TEST 8: Obtener credenciales sin cookie"
			print " Status esperado: 200 (con una respuesta informativa)"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, None)

			# TEST 9
			# Login (prueba de nueva sesión y actualizar credenciales)
			request_uri = basePath + "/login"
			print "TEST 9: Prueba de nueva sesión y actualizar credenciales (usuario 1)"
			print "Status esperado: 200"
			access_token = social_network + "Modify2TEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token': "TEST 9",
				'user_identifier': user_id1})	
			test_utils.make_request("POST", request_uri, params, 200, None)

			# TEST 10
			# Obtener credenciales con cookie antigua
			request_uri = basePath + "/credenciales/" + token_id1
			print "TEST 10: Obtener credenciales con cookie de sesión antigua"
			print "Status esperado: 400"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 400, session1)

			# TEST 11 
			# Logout con cookie antigua
			request_uri = basePath + "/logout"
			print "TEST 11: Logout sin cookie de sesion"
			print "Status esperado: 401"
			params = urllib.urlencode({})
			test_utils.make_request("POST", request_uri, params, 401, None)
			print "TESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"
		
		elif option == "borrado":
			# PRE-TEST 1: Login en el sistema de usuario de prueba 1
			request_uri = basePath + "/login"
			print "PRE-TEST 1: Login en el sistema de usuario de prueba 1"
			print "Status esperado: 200"
			access_token = social_network + "tokenTODELETE1"
			params = urllib.urlencode({'token_id': token_id1, 'access_token': access_token, 
				"user_identifier": user_id1})	
			session1 = test_utils.make_request("POST", request_uri, params, 200, None)

			# PRE-TEST 2: Login en el sistema de usuario de prueba 2
			request_uri = basePath + "/login"
			print "PRE-TEST 2: Login en el sistema de usuario de prueba 1"
			print "Status esperado: 200"
			access_token = social_network + "tokenTODELETE2"
			params = urllib.urlencode({'token_id': token_id2, 'access_token': access_token, 
				"user_identifier": user_id2})	
			session2 = test_utils.make_request("POST", request_uri, params, 200, None)

			# TEST 12
			# Borrar credenciales de usuarios de prueba2
			request_uri = basePath + "/credenciales/" + token_id2
			print "TEST 12: Borrar creedenciales sin cookie de sesión"
			print "Status esperado: 401"
			params = urllib.urlencode({})
			test_utils.make_request("DELETE", request_uri, params, 401, None)			

			# TEST 13
			# Borrar credenciales de usuario de prueba1 (Estando logeado)
			request_uri = basePath + "/credenciales/" + token_id1
			print "TEST 13: Borrado de credenciales estando logeado (usuario 1)"
			print "Status esperado: 204"
			params = urllib.urlencode({})
			test_utils.make_request("DELETE", request_uri, params, 204, session1)
			
			# TEST 14
			# Borrar credenciales de usuario de prueba2 (Con una cookie incorrecta)
			request_uri = basePath + "/" + token_id2
			print "TEST 14: Borrado de credenciales estando logeado, pero sin ser propietario de las mismas"
			print "Status esperado: 401"
			params = urllib.urlencode({})
			test_utils.make_request("DELETE", request_uri, params, 401, session1)

			# TEST 15
			# Borrar credenciales de usuario de prueba2 (Estando logeado)
			request_uri = basePath + "/" + token_id2
			print "TEST 15: Borrado de credenciales estando logeado"
			print "Status esperado: 204"
			params = urllib.urlencode({})
			test_utils.make_request("DELETE", request_uri, params, 204, session2)

			# TEST 16
			# Borrar credenciales de usuario de prueba 2 por segunda vez (Caso de error)
			request_uri = basePath + "/" + token_id2
			print "TEST 16: Intento de borrado por segunda vez (credenciales de usuario 2)"
			print "Status esperado: 404"
			params = urllib.urlencode({})
			test_utils.make_request("DELETE", request_uri, params, 404, session2)

			# POST-TEST 1: Realizar logout en el sistema (usuario 1)
			request_uri = basePath + "/logout"
			print "POST-TEST 1: Logout de usuario 1 con cookie de sesión"
			print "Status esperado: 200"
			# Se desloguea el usuario logueado en el PRE TEST 1
			test_utils.make_request("POST", request_uri, params, 200, session1)

			# POST-TEST 2: Realizar logout en el sistema (usuario 2)
			request_uri = basePath + "/logout"
			print "POST-TEST 2: Logout de usuario 2 con cookie de sesión"
			print "Status esperado: 200"
			# Se desloguea el usuario logueado en el PRE TEST 2
			test_utils.make_request("POST", request_uri, params, 200, session2)

			print "\nTESTs finalizados. Comprobar el borrado de las entidades de tipo Token en datastore"

	elif social_network=="stackoverflow" or social_network=="instagram" or social_network=="linkedin":
		session1 = None
		session2 = None
		token_id1 = "id" + social_network
		access_token1 = social_network + "TEST"
		token_id2 = "idERROR" + social_network + "2"
		user_id1 = "user" + social_network + "1"

		# Iniciamos dos sesiones distintas en googleplus para realizar las pruebas
		request_uri = "/api/oauth/googleplus/login"
		print "PRETEST 1: Login de usuario 1 por Googleplus\n Ignorar el status de este caso"
		token_id_login = "idgoogle"
		access_token_login = "googleTEST"
		params = urllib.urlencode({'token_id': token_id_login, 'access_token':access_token_login, 
			"user_identifier": user_id1})
		session1 = test_utils.make_request("POST", request_uri, params, 201, None)

		request_uri = "/api/oauth/googleplus/login"
		print "PRETEST 2: Login de usuario 2 por Googleplus\n Ignorar el status de este caso"
		token_id_login2 = "idgoogle2"
		access_token_login2 = "googleTEST"
		params = urllib.urlencode({'token_id': token_id_login2, 'access_token':access_token_login2})
		session2 = test_utils.make_request("POST", request_uri, params, 201, None)
		
		if option == None:
			# Tests a la API seleccionada
			# TESTs relativos a la creacion/actualizacion de credenciales (POST /api/oauth/{social_network})
			# TEST 1
			# Añadir credenciales nuevas al sistema (Sin cookie de sesion)
			request_uri = "/api/oauth/" + social_network
			print "TEST 1: Añadir nuevo par de credenciales, sin cookie de sesión"
			print "Status esperado: 401"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token1})
			test_utils.make_request("POST", request_uri, params, 401, None)

			# TEST 2
			print "TEST 2: Añadir nuevo par de credenciales"
			print "Status esperado: 201"
			access_token1 = social_network + "ModifyTEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token1})
			test_utils.make_request("POST", request_uri, params, 201, session1)	

			# TEST 3
			print "TEST 3: Actualizar par de credenciales"
			print "Status esperado: 200"
			access_token1 = social_network + "ModifyTEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token1})
			test_utils.make_request("POST", request_uri, params, 200, session1)	
			
			# TEST 4
			print "TEST 4: Actualizar par de credenciales con cookie de sesión incorrecta"
			print "Status esperado: 400"
			access_token1 = social_network + "ModifyTEST"
			params = urllib.urlencode({'token_id': token_id1, 'access_token':access_token1})
			test_utils.make_request("POST", request_uri, params, 400, session2)	
			
			# TEST 5
			print "TEST 5: Actualizar credenciales proporcionando un solo parámetro"
			print "Status esperado: 400"
			params = urllib.urlencode({'token_id': token_id2})
			test_utils.make_request("POST", request_uri, params, 400, session1)

			# TEST relativos a la obtencion de credenciales (GET /api/oauth/{social_network}/{token_id})
			# TEST 6
			# Get (Sin cookie)
			request_uri = "/api/oauth/" + social_network + "/credenciales/" + token_id1
			print "TEST 6: Obtener credenciales sin cookie de sesión"
			print "Status esperado: 200 (Con un mensaje informativo)"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, None)

			# TEST 7
			# TODO Get (Con Cookie)
			print "TEST 7: Obtener credenciales con cookie"
			print "Status esperado: 200"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# TEST 8 
			# TODO GET credenciales (Con una cookie de sesion incorrecta)
			print "TEST 8: Obtener credenciales con cookie incorrecta"
			print "Status esperado: 400"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 400, session2)
			
			# TEST 9
			# TODO GET credenciales (Cookie de sesion correcta, a un token id no existente en el sistema)
			request_uri = "/api/oauth/" + social_network + "credenciales/tokenERROR"
			print "TEST 9: Intento de obtener un token no existente en el sistema"
			print "Status esperado: 404"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 404, session2)
		elif option == 'borrado':
			pass
			# # TODO TESTs borrar credenciales de usuario activo (Conjunto de pruebas de delete)


		# POST-TEST 1: Realizar logout en el sistema (usuario 1)
		# Se desloguea el usuario logueado en el PRE TEST 1
		request_uri = "/api/oauth/googleplus/logout"
		print "POST-TEST 1: Logout de usuario 1 con cookie de sesión"
		print "Status esperado: 200"
		test_utils.make_request("POST", request_uri, params,200, session1)

		# POST-TEST 2: Realizar logout en el sistema (usuario 2)
		# Se desloguea el usuario logueado en el PRE TEST 2
		request_uri = "/api/oauth/googleplus/logout"
		print "POST-TEST 2: Logout de usuario 1 con cookie de sesión"
		print "Status esperado: 200"
		test_utils.make_request("POST", request_uri, params,200, session2)
	
		print "\nTESTs finalizados. Comprobar las entidades de tipo Usuario y Token almacenadas en datastore"
	else:
		print "Error: es obligatorio proporcionar un parámetro válido para indicar que red social se pretende testear"
		print "Uso: python api_oauth_tester.py {googleplus|stackoverflow|facebook|instagram|linkedin|twitter} [borrado]"

	# Cerramos conexión
	test_utils.tests_status()
	test_utils.closeConnection()

if __name__ == "__main__":
    main()