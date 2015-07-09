# -*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Usuarios de PicBit (api/usuarios)
# Uso: ./api_usuarios_tester [borrado]


def main():
	option = None
	session1 = None
	session2 = None
	session_error = "session_error"
	user_id1 = "idUsuario1"
	user_id2 = "idUsuario2"
	user_id_error = "idError"
	basepath = "/api/usuarios/"
	
	if len(sys.argv) == 2:
		option = sys.argv[1]

	# PRETESTs: Inicio de sesion con Google+ en el sistema
	request_uri = "/api/oauth/googleplus/login"
	print "PRETEST 1: Login de usuario 1 en el sistema\n Ignorar el status de este caso"
	token_id_login = "idgoogle"
	access_token_login = "googleTEST"
	params = urllib.urlencode({'token_id': token_id_login, 'access_token': access_token_login,
	 'user_identifier': user_id1 })
	session1 = test_utils.make_request("POST", request_uri, params, 201, None, True)
	
	print "PRETEST 2: Login de usuario 2 en el sistema"
	print "Ignorar el status de este caso"
	token_id_login2 = "idgoogle2"
	access_token_login2 = "googleTEST2"
	params = urllib.urlencode({'token_id': token_id_login2, 'access_token': access_token_login2,
	 'user_identifier': user_id2 })
	session2 = test_utils.make_request("POST", request_uri, params, 200, None, True)
	
	if option == None:
		params = urllib.urlencode({})

		# TESTs Relativos a la obtención de lista de usuarios
		# TEST 1
		print "TEST 1: Obtener lista de usuarios (sin proporcionar una cookie de sesion)"
		print " Status esperado: 401"
		test_utils.make_request("GET", basepath, params, 401, None)

		# TEST 2
		print "TEST 2: Obtener lista de usuarios (proporcionando una cookie de sesion no válida)"
		print " Status esperado: 400"
		test_utils.make_request("GET", basepath, params, 400, session_error)
		
		# TEST 3
		print "TEST 3: Obtener lista de usuarios (proporcionando una cookie de sesion válida)"
		print " Status esperado: 200 (O 204 si la lista de usuarios está vacía)"
		test_utils.make_request("GET", basepath, params, 200, session1)
		
		# TESTs Relativos a la obtención de información sobre un usuario
		# TEST 4
		print "TEST 4: Obtener info de usuario (sin proporcionar una cookie de sesión)"
		print "Status esperado: 401"
		request_uri = basepath + idUsuario1
		test_utils.make_request("GET", request_uri, params, 401, None)		
		
		# TEST 5
		print "TEST 5: Obtener info de usuario (no existente en el sistema)"
		print "Status esperado: 404"
		request_uri = basepath + idError
		test_utils.make_request("GET", request_uri, params, 404, session1)		

		# TEST 6 
		print "TEST 6: Obtener info de usuario, caso obtención de información pública de un usuario en concreto"
		print "(proporcionando una cookie de sesión diferente al recurso usuario solicitado)"
		print "Status esperado: 200"
		request_uri = basepath + idUsuario1
		test_utils.make_request("GET", request_uri, params, 200, session2)

		# TEST 7 
		print "TEST 7: Obtener info de usuario, caso obtención de información privada de un usuario en concreto"
		print "(cookie de sesión coincide con recurso usuario solicitado)"
		print "Status esperado: 200"
		request_uri = basepath + idUsuario1
		test_utils.make_request("GET", request_uri, params, 200, session1)

		
		# TESTs Relativos a la Modificación de información de un usuario en particular
		# TEST 8
		print "TEST 8: Modificar info de usuario 1(sin cookie de sesión)"
		print "Status esperado: 401"
		request_uri = basepath + idUsuario1
		test_utils.make_request("POST", request_uri, params, 401, None)

		# TEST 9
		print "TEST 9: Modificar info de usuario 1 (Con cookie de sesión distinta a la del recurso usuario)"
		print "Status esperado: 401"
		request_uri = basepath + idUsuario1
		test_utils.make_request("POST", request_uri, params, 401, session2)

		# TEST 10: Modificar info de usuario, caso parámetros incorrectos (Cookie de sesión correcta)
		# TEST 11: Modificar info de usuario, caso añadir un componente con su correspondiente valoración (Cookie de sesión correcta)
		# TEST 12: Modificar info de usuario, caso modificar todos los campos del usuario, cambiando ámbito de email y teléfono a privado
		#         (cookie de sesión correcta)

		
		# Comprobamos caso de uso de obtención de información privada de usuario
		# TEST 13: GET Usuario, (cookie de sesión distinta al recurso solicitado)
		# TEST 14: GET Usuario, (cookie de sesión asociada al usuario solicitado)
		# Cambiamos el ámbito de campos de usuario a público
		# TEST 15: POST Usuario, caso cambiar a ámbito público el email y telefono de usuario (cookie de sesión correcta)
	elif option == 'borrado':

		# TESTs Relativos a la eliminación de un usuario del sistema
		# TEST 16: DELETE Usuario (cookie de sesión incorrecta)
		# TEST 17: DELETE Usuario (usuario no existente en el sistema)
		# TEST 18: DELETE Usuario (cookie de sesión correcta)

	# POSTESTs: Inicio de sesion con Google+ en el sistema
	params = urllib.urlencode({})
	print "POSTEST 1: Login de usuario 1 en el sistema"
	print "Ignorar el status de este caso"
	test_utils.make_request("POST", request_uri, params, 201, session1, True)
	
	print "POSTEST 2: Login de usuario 2 en el sistema"
	print "Ignorar el status de este caso"
	test_utils.make_request("POST", request_uri, params, 200, session2, True)
	

if __name__ == "__main__":
    main()