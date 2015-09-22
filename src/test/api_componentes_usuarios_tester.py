# -*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto 
# (api/componentes y api/usuarios)
# Uso: python api_componentes_usuarios.py

def main():
	components_basepath = "/api/componentes"
	users_basepath = "/api/usuarios"
	session1 = None
	session_error = "session=session_error"
	user_id1 = "user_components_test"
	# Sets the option param
	option = None
	if len(sys.argv) == 2:
		option = sys.argv[1] 

	# We open the connection with the server
	test_utils.openConnection()
	# PRE-TESTs. Login de usuario en el sistema, utilizando Google+
	request_uri = "/api/oauth/googleplus/login"
	print "PRETEST 1: Login de usuario 1 en el sistema\n Ignorar el status de este caso"
	print "Ignorar el status de salida de este TEST"
	token_id_login = "id_component_token"
	access_token_login = "googleTEST"
	params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
	 'user_identifier': user_id1 })
	session1 = test_utils.make_request("POST", request_uri, params, 200, None, True)

	# PRE-TEST 2. Añadimos el componente a utilizar en las pruebas
	print "PRETEST 2: Subir un componente al sistema (para asegurarnos de que existe en el sistema)."
	print "Ignorar el status de salida de este TEST"
	print "Status esperado: 201 "
	params = urllib.urlencode({'url': 'https://github.com/JuanFryS/instagram-timeline',
            'component_id': 'instagram-timeline',
            'description': 'Web component to obtain the timeline of the social network Instagram using Polymer',
            'social_network': 'instagram',
            'input_type': 'None',
            'output_type': 'photo'
	})
	test_utils.make_request("PUT", components_basepath, params, 201, None)


	if option == None:
		# TESTs relativos a la modificación de info de usuario (añadir un componente al usuario)
		# TEST 1
		print "TEST 1: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (El componente no existe en el sistema)"
		print "Status esperado: 304 (El recurso no se modifica)"
		request_uri = users_basepath + "/" + user_id1
		params = urllib.urlencode({'component': 'componenteError'})
		test_utils.make_request("POST", request_uri, params, 304, session1)
		
		# TEST 2
		print "TEST 2: Modificar info de usuario, caso añadir un componente al dashboard del usuario 1 (Cookie de sesión correcta)"
		print "Status esperado: 200"
		params = urllib.urlencode({'component': 'instagram-timeline'})
		test_utils.make_request("POST", request_uri, params, 200, session1)

		# TESTs relativos a la obtención de componentes de usuario
		# TEST 3
		print "TEST 3: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(parámetro de filtrado por usuario)"
		print "Status esperado: 200"
		request_uri = components_basepath + "?filter=user"
		params = urllib.urlencode({})
		test_utils.make_request("GET", request_uri, params, 200, session1)

		# TEST 4
		print "TEST 4: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
		print "Status esperado: 204 (El usuario no tiene componentes de la red social Twitter)"
		request_uri = components_basepath + "?social_network=twitter&filter=user&format=reduced"
		test_utils.make_request("GET", request_uri, params, 204, session1)

		# TEST 5
		print "TEST 5: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
		print "En este caso obtenemos los componentes de instagram del usuario"
		print "Status esperado: 200"
		request_uri = components_basepath + "?social_network=instagram&filter=user&format=reduced"
		test_utils.make_request("GET", request_uri, params, 200, session1)

		# TEST 6
		print "TEST 6: Obtener la lista de componentes, proporcionando una cookie de sesion"
		print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista completo)"
		print "Status esperado: 200"
		request_uri = components_basepath + "?social_network=instagram&filter=user&format=complete"
		test_utils.make_request("GET", request_uri, params, 200, session1)
		
		# TEST 7
		print "TEST 7: obtener info de usuario"
		print "Status esperado: 200"
		request_uri = users_basepath + "/" + user_id1
		test_utils.make_request("GET", request_uri, params, 200, session1)

		# TEST 8
		print "TEST 8: obtener info de usuario, con formato de lista de componentes detallado"
		print "Status esperado: 200"
		request_uri = users_basepath + "/" + user_id1 + "?component_info=detailed"
		test_utils.make_request("GET", request_uri, params, 200, session1)

	elif option == 'borrado':
		#TODO- TESTs relativos al borrado de componentes de usuario (iss101)
		# Borrar el componente del usuario
		# Obtener info de usuario (no debe aparecer el componente eliminado en la lista de componentes de usuario)
		# Obtener lista filtrada de componentes (filter=user)
		# Obtener info sobre el componente (para verificar que no se ha eliminado por error el componente general)
		pass
	
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
