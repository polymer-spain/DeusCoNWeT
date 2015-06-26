# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de Usuarios de PicBit (api/usuarios)
# Uso: ./api_usuarios_tester

connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
# connection = httplib.HTTPConnection("localhost:8080")

def make_request(method, request_uri, params, status_ok, session):
	"""
	Metodo make_request: Realiza llamadas HTTP a la API REST, retornando la
	cookie de sesion enviada por el servidor. 
	Parametros:
		method: metodo HTTP de la peticion
		request_uri: URL de la peticion
		params: parametros de la peticion
		status_ok: status HTTP de retorno esperado de la peticion
		session: cookie de sesion para adjuntar en la peticion
	"""
	print "Realizando petición", method, request_uri
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
	session1 = None
	session_error = "session_error"
	user_id = "idGoogle"
	user_id_error = "idError"
	basepath = "/api/usuarios/"

	# PRETEST: Inicio de sesion con Google+ en el sistema
	request_uri = "/api/oauth/googleplus?action=login"
	print "\nPRETEST 1: Haciendo petición POST a " + request_uri + " (login)\n Ignorar el status de este caso"
	token_id_login = "idgoogle"
	access_token_login = "googleTEST"
	params = urllib.urlencode({'token_id': token_id_login, 'access_token':access_token_login})
	session1 = make_request("POST", request_uri, params, 201, None)
	
	print "-----------------------------------------------------------------------"
	# TESTs Relativos a la obtención de lista de usuarios
	# TEST 1
	print "TEST 1: GET lista de usuarios (sin proporcionar una cookie de sesion)"
	print " Status esperado: 401"
	params = urllib.urlencode({})
	make_request("GET", basepath, params, 401, None)

	# TEST 2
	print "TEST 2: GET lista de usuarios (proporcionando una cookie de sesion no válida)"
	print " Status esperado: 400"
	make_request("GET", basepath, params, 400, session_error)
	
	# TEST 3
	print "TEST 3: GET lista de usuarios (proporcionando una cookie de sesion válida)"
	print " Status esperado: 200 (O 204 si la lista de usuarios está vacía)"
	make_request("GET", basepath, params, 200, session1)

	# print "-----------------------------------------------------------------------"
	# TESTs Relativos a la obtención de información sobre un usuario
	# TEST 4: GET Usuario (sin proporcionar una cookie de sesión)
	# TEST 5: GET Usuario, caso obtención de información pública de un usuario en concreto
	# 		  (proporcionando una cookie de sesión diferente al recurso usuario solicitado)

	# print "-----------------------------------------------------------------------"
	# TEST 6: GET Usuario, caso obtención de información privada de un usuario en concreto
	#         (cookie de sesión coincide con recurso usuario solicitado)
	# TEST 7: GET Usuario (usuario no existente en el sistema)

	# print "-----------------------------------------------------------------------"
	# TESTs Relativos a la Modificación de información de un usuario en particular
	# TEST 8: POST Usuario (sin cookie de sesión)
	# TEST 9: POST Usuario (Con cookie de sesión distinta a la del recurso usuario)
	# TEST 10: POST Usuario, caso parámetros incorrectos (Cookie de sesión correcta)
	# TEST 11: POST Usuario, caso añadir un componente con su correspondiente valoración (Cookie de sesión correcta)
	# TEST 12: POST Usuario, caso modificar todos los campos del usuario, cambiando ámbito de email y teléfono a privado
	#         (cookie de sesión correcta)

	# print "-----------------------------------------------------------------------"
	# Comprobamos caso de uso de obtención de información privada de usuario
	# TEST 13: GET Usuario, (cookie de sesión distinta al recurso solicitado)
	# TEST 14: GET Usuario, (cookie de sesión asociada al usuario solicitado)
	# Cambiamos el ámbito de campos de usuario a público
	# TEST 15: POST Usuario, caso cambiar a ámbito público el email y telefono de usuario (cookie de sesión correcta)

	# print "-----------------------------------------------------------------------"
	# TESTs Relativos a la eliminación de un usuario del sistema
	# TEST 16: DELETE Usuario (cookie de sesión incorrecta)
	# TEST 17: DELETE Usuario (usuario no existente en el sistema)
	# TEST 18: DELETE Usuario (cookie de sesión correcta)



if __name__ == "__main__":
    main()