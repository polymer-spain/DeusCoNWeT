
# -*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto (funcionalidades de alto nivel) 
# (api/componentes y api/usuarios)
# Uso: python api_componentes_usuarios_tester.py [dashboard | dashboard_borrado | dashboard_predeterminados | --help]

def main():
	components_basepath = "/api/componentes"
	users_basepath = "/api/usuarios"
	session1 = None
	session2 = None
	session_error = "session=session_error"
	user_id1 = "id_usuario_dashboard_1"
	user_id2 = "id_usuario_dashboard_2"

	# Sets the option param
	option = None
	if len(sys.argv) == 2:
		option = sys.argv[1] 

	if option in ["dashboard", "dashboard_borrado", "dashboard_predeterminados"]:
		# We open the connection with the server
		test_utils.openConnection(False) # Realizamos pruebas en local (remote=False)

		# PRE-TESTs. Login de usuario en el sistema, utilizando Google+
		request_uri = "/api/oauth/googleplus/login"
		print "PRETEST 1: Login de usuario 1 ( " + user_id1 + " ) en el sistema"
		print "Ignorar el status de salida de este TEST"
		print "Status esperado: 200 "
		token_id_login = "id_component_users_test_token"
		access_token_login = "googleTEST"
		params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
		 'user_identifier': user_id1 })
		session1 = test_utils.make_request("POST", request_uri, params, 200, None, True, True)


		request_uri = "/api/oauth/googleplus/login"
		print "PRETEST 2: Login de usuario ( " + user_id2 + " )en el sistema"
		print "Ignorar el status de salida de este TEST"
		print "Status esperado: 200 "
		token_id_login = "id_component_users_test_token2"
		access_token_login = "googleTEST2"
		params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
		 'user_identifier': user_id2 })
		session2 = test_utils.make_request("POST", request_uri, params, 200, None, True, True)

		# PRE-TESTs. Añadimos dos componentes a utilizar en las pruebas
		print "PRETEST 3: Subir un componente al sistema (para asegurarnos de que existe en el sistema)."
		print "Componente no predeterminado. Id: linkedin-timeline"
		print "Ignorar el status de salida de este TEST"
		print "Status esperado: 201 "
		params = urllib.urlencode({'url': 'https://github.com/JuanFryS/linkedin-timeline',
	            'component_id': 'linkedin-timeline',
	            'description': 'Web component to obtain the timeline of the social network Linkedin using Polymer',
	            'social_network': 'linkedin',
	            'input_type': 'None',
	            'output_type': 'photo',
	            'versions': 'stable',
	            'predetermined': 'False'
		})
		test_utils.make_request("PUT", components_basepath, params, 201, None, preTest=True)


		if option == "dashboard":

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
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session1)

			# TEST 3
			print "TEST 3: Modificar info de usuario, caso añadir un componente al dashboard del usuario 2 (Cookie de sesión correcta)"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id2
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session2)

			# TESTs relativos a la obtención de componentes de usuario
			# TEST 4
			print "TEST 4: Obtener la lista de componentes, proporcionando una cookie de sesion"
			print "(parámetro de filtrado por usuario)"
			print "Status esperado: 200"
			request_uri = components_basepath + "?filter=user"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# TEST 5
			print "TEST 5: Obtener la lista de componentes, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
			print "Status esperado: 204 (El usuario no tiene componentes de la red social Twitter)"
			request_uri = components_basepath + "?social_network=twitter&filter=user&list_format=reduced"
			test_utils.make_request("GET", request_uri, params, 204, session1)
			
			# TEST 6
			print "TEST 6: Obtener la lista de componentes, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista reducido)"
			print "En este caso obtenemos los componentes de instagram del usuario"
			print "Status esperado: 200"
			request_uri = components_basepath + "?social_network=linkedin&filter=user&list_format=reduced"
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# TEST 7
			print "TEST 7: Obtener la lista de componentes, proporcionando una cookie de sesion"
			print "(Combinamos el parámetro de filtrado por red social y el filtrado por usuario con el formato de lista completo)"
			print "Status esperado: 200"
			request_uri = components_basepath + "?social_network=linkedin&filter=user&list_format=complete"
			test_utils.make_request("GET", request_uri, params, 200, session1)
			
			# TEST 8
			print "TEST 8: Obtener info de usuario"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1
			test_utils.make_request("GET", request_uri, params, 200, session1)

			# TEST 9
			print "TEST 9: Obtener info de usuario, con formato de lista de componentes detallado"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1 + "?component_info=detailed"
			test_utils.make_request("GET", request_uri, params, 200, session1)

		elif option == 'dashboard_borrado':
			component_rel_uri = "/linkedin-timeline"

			# PRETEST 4
			print "PRETEST 4: Añadimos el componente al dashboard de usuario, si no está añadido ya"
			print "Status esperado: 200 (Ignorar status de este caso)"
			request_uri = users_basepath + "/" + user_id1
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session1, preTest=True)

			# PRETEST 5
			print "PRETEST 5: Obtenemos la info de usuario, con objeto de ver los componentes que tiene incluidos en su dashboard"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1 + "?component_info=detailed"
			params = urllib.urlencode({})
			test_utils.make_request("GET", request_uri, params, 200, session1, preTest=True)

			# TESTs relativos al borrado de componentes de usuario
			# Pruebas de casos de error
			# TEST 10
			print "TEST 10: Borrar el componente del usuario, sin cookie"
			print "Status esperado: 401"
			request_uri = components_basepath + component_rel_uri 
			test_utils.make_request("DELETE", request_uri, params, 401, None)
			
			# TEST 11
			print "TEST 11: Borrar el componente del usuario, proporcionando una cookie incorrecta"
			print "Status esperado: 400"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("DELETE", request_uri, params, 400, session_error)
			
			# TEST 12
			print "TEST 12: Borrar el componente del usuario, a un componente que no existe"
			print "Status esperado: 400"
			request_uri = components_basepath + "/component_error"
			test_utils.make_request("DELETE", request_uri, params, 400, session_error)

			# Casos de éxito
			# TEST 13
			print "TEST 13: Eliminar componente del usuario 1, con cookie de sesión correcta"
			print "Status esperado: 200"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("DELETE", request_uri, params, 200, session1)

			# TEST 14
			print "TEST 14: Obtener info de usuario 1"
			print "(No debe aparecer el componente eliminado en la lista de componentes de usuario)"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1
			test_utils.make_request("GET", request_uri, params, 200, session1)		
			
			# TEST 15
			print "TEST 15: Volver a añadir el componente"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id1
			params = urllib.urlencode({'component': 'linkedin-timeline'})
			test_utils.make_request("POST", request_uri, params, 200, session1)

			# TEST 16
			print "TEST 16: Eliminar el componente del dashboard del usuario 1"
			print "Status esperado: 200"
			params = urllib.urlencode({})
			request_uri = components_basepath + component_rel_uri + "?scope=user"
			test_utils.make_request("DELETE", request_uri, params, 200, session1)		
					
			# TEST 17
			print "TEST 17: Obtener lista filtrada de componentes (filter=user), proporcionando la cookie de sesión del usuario 1"
			print "(No debe aparecer el componente eliminado)"
			print "Status esperado: 204"
			request_uri = components_basepath + "?filter=user&list_format=complete"
			test_utils.make_request("GET", request_uri, params, 204, session1)		
			
			# TEST 18
			print "TEST 18: Intentar eliminar el componente del dashboard del usuario 1, estando eliminado ya"
			print "Status esperado: 404"
			request_uri = components_basepath + component_rel_uri + "?scope=user"
			test_utils.make_request("DELETE", request_uri, params, 404, session1)		

			# TEST 19
			print "TEST 19: Obtener info sobre el componente"
			print "(Para verificar que no se ha eliminado por error el componente general)"
			print "Status esperado: 200"
			request_uri = components_basepath + component_rel_uri
			test_utils.make_request("GET", request_uri, params, 200, session1)		
		
		
		elif option == 'dashboard_predeterminados':
			user_id3 = "id_usuario3"
			session3 = None

			# PRETESTs 4 y 5: Añadimos los componentes que se van a añadir de forma predeterminada al dashboard de usuario (Si no están añadidos ya)
			print "PRETEST 4: Subir un componente predeterminado al sistema (insignia-fb-prededeterminada)."
			print "Status esperado: 201 "
			request_uri = "/api/componentes"
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/insignia-fb-prededeterminada',
		            'component_id': 'insignia-fb-prededeterminada',
		            'description': 'Web component to obtain the timeline of Twitter using Polymer',
		            'social_network': 'facebook' ,
		            'input_type': 'None',
		            'output_type': 'post',
		            'versions': 'stable',
		            'predetermined': "True"
			})
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)
			
			# PRETEST 6
			print "PRETEST 6: Añadimos un componente cualquiera al sistema (No predeterminado)"
			print "Status esperado: 201 "
			versions_list = ["stable", "usability_defects"]
			params = urllib.urlencode({'url': 'https://github.com/JuanFryS/google-inbox',
		            'component_id': 'google-inbox',
		            'description': 'Web component to obtain mails from your gmail account',
		            'social_network': 'googleplus',
		            'input_type': 'None',
		            'output_type': 'text',
		            'versions': versions_list,
		            'predetermined': "False"
			}, doseq=True)
			test_utils.make_request("PUT", request_uri, params, 201, None, preTest=True)
			
			# TEST 20: Creamos un nuevo usuario en el sistema (Realizando login mediante googleplus)
			request_uri = "/api/oauth/googleplus/login"
			print "TEST 20: Login de usuario 1 en el sistema\n Ignorar el status de este caso"
			print "Ignorar el status de salida de este TEST"
			print "Status esperado: 200 "
			token_id_login = "id_user3_test_token"
			access_token_login = "googleTEST"
			params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
			 'user_identifier': user_id3 })
			session3 = test_utils.make_request("POST", request_uri, params, 201, None, True)

			# TEST 21
			print "TEST 21: Intentamos añadir un componente predeterminado al usuario"
			print "Status esperado: 304 (Ya estaba añadido anteriormente)"
			request_uri = users_basepath + "/" + user_id3
			params = urllib.urlencode({'component': 'insignia-fb-prededeterminada'})
			test_utils.make_request("POST", request_uri, params, 304, session3)		
			
			# TEST 22: Añadimos un componente cualquiera al usuario
			print "TEST 22: Añadimos un componente cualquiera al usuario"
			print "Status esperado: 200"
			request_uri = users_basepath + "/" + user_id3
			params = urllib.urlencode({'component': 'google-inbox'})
			test_utils.make_request("POST", request_uri, params, 200, session3, preTest=True)
			
			# TEST 23
			print "TEST 23: Listamos los detalles sobre los componentes de usuario."
			print "(Deben aparecer los componentes predeterminados y el añadido)"
			print "Status esperado: 200"
			params = urllib.urlencode({})
			request_uri = components_basepath + "?filter=user&list_format=complete"
			test_utils.make_request("GET", request_uri, params, 200, session3)		

		# POST-TESTs. Logout de usuario en el sistema
		request_uri = '/api/oauth/googleplus/logout'
		params = urllib.urlencode({})
		print "POSTEST 1: Logout de usuario 1 en el sistema"
		print "Ignorar el status de este caso"
		test_utils.make_request("POST", request_uri, params, 200, session1, True)

		# Cerramos conexión e imprimimos el ratio de test ok vs erróneos
		test_utils.closeConnection()
		test_utils.tests_status()

	elif option == "help":
		print "Script para hacer pruebas a la API de Componentes y Usuarios de PicBit, en conjunto (funcionalidades de alto nivel) "
		print "(api/componentes y api/usuarios)"
		print "Uso: python api_componentes_usuarios_tester.py [dashboard | dashboard_borrado | dashboard_predeterminados| help]"

if __name__ == "__main__":
	main()
