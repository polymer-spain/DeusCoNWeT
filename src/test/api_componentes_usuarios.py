# -*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto 
# (api/componentes y api/usuarios)
# Uso: python api_componentes_usuarios.py

def main():
	basepath_componentes = "api/componentes"
	basepath_usuarios = ""
	session1 = None
	session_error = "session=session_error"


	# PRE-TESTs. Login de usuario en el sistema, utilizando Google+
	request_uri = "/api/oauth/googleplus/login"
	print "PRETEST 1: Login de usuario 1 en el sistema\n Ignorar el status de este caso"
	token_id_login = "idgoogle"
	access_token_login = "googleTEST"
	params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
	 'user_identifier': user_id1 })
	session1 = test_utils.make_request("POST", request_uri, params, 200, None, True)

	if option = None:

		TESTs relativos a la modificación de info de usuario (añadir un componente al usuario)
		# TEST 1
		print "TEST 1: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (El componente no existe en el sistema)"
		print "Status esperado: 200 (El recurso no se modifica)"
		params = urllib.urlencode({'component': 'componenteError'})
		test_utils.make_request("POST", request_uri, params, 200, session1)
		
		# TEST 2
		print "TEST 2: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (Cookie de sesión correcta)"
		print "Status esperado: 200"
		params = urllib.urlencode({'component': 'instagram-timeline'})
		test_utils.make_request("POST", request_uri, params, 200, session1)

		# TESTs relativos a la obtención de componentes de usuario
		# TEST 3
		print "TEST 3: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(parámetro de filtrado por usuario)"
		print "Status esperado: 204"
		request_uri = basepath + "?filter=user"
		test_utils.make_request("GET", request_uri, params, 200, session1)

		# TEST 4
		print "TEST 4: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
		print "Status esperado: 200"
		request_uri = basepath + "?social_network=twitter&filter=user&format=reduced"
		test_utils.make_request("GET", request_uri, params, 200, session1)

		# TEST 5
		print "TEST 5: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista completo)"
		print "Status esperado: 200"
		request_uri = basepath + "?social_network=twitter&filter=user&format=complete"
		test_utils.make_request("GET", request_uri, params, 200, session1)
		

	elif option = 'borrado':
		#TODO- TESTs relativos al borrado de componentes de usuario

	
	# POST-TESTs. Logout de usuario en el sistema
	request_uri = '/api/oauth/googleplus/logout'
	params = urllib.urlencode({})
	print "POSTEST 1: Logout de usuario 1 en el sistema"
	print "Ignorar el status de este caso"
	test_utils.make_request("POST", request_uri, params, 200, session1, True)

	# Cerramos conexión e imprimimos el ratio de test ok vs erróneos
	test_utils.closeConnection()
	test_utils.tests_status()

if __name__ == "__main__":
	main()
