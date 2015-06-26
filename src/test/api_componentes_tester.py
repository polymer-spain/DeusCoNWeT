# -*- coding: utf8 -*-
import test_utils
# Script para hacer pruebas a la API de Componentes de PicBit (api/componentes)
# Uso: ./api_componentes_tester [borrado]

def main():
	test_utils.openConnection()
	basepath = "api/componentes/"
	session1 = None

	# PRE-TEST 1: Hacer login en el sistema mediante googleplus
	request_uri = "/api/oauth/googleplus?action=login"
	print "\nPRETEST 1: Haciendo petición POST a " + request_uri + " (login)\n Ignorar el status de este caso"
	token_id_login = "idgoogle"
	access_token_login = "googleTEST"
	params = urllib.urlencode({'token_id': token_id_login, 'access_token':access_token_login})
	session1 = test_utils.make_request("POST", request_uri, params, 201, None)


	# TEST 1
	print "TEST 1: : Obtener la lista de componentes. Debe retornar una lista vacia de componentes"
	print "Status esperado: 204 "
	request_uri = basepath
	params = urllib.urlencode({})
	test_utils.make_request("GET", request_uri, params, 204, session1)	

	# TESTs relativos a la operación PUT lista de componentes (Subir un componente al sistema) 
	# TEST 2
	print "TEST 2: Subir un componente al sistema, proporcionando una URI incorrecta."
	print "Status esperado: 404 "
	request_uri = basepath
	params = urllib.urlencode({})
	test_utils.make_request("GET", request_uri, params, 204, session1)	

	# TEST 3: Subir un componente al sistema, proporcionando un parametro erroneo.
	# Status esperado: 400

	# Subimos dos componentes al sistema
	# TEST 4: Subir un componente al sistema (componente 1).
	# Status esperado: 200

	# TEST 5: Subir un componente al sistema (componente 2).
	# Status esperado: 200

	# TESTs Metodo GET Lista de componentes 
	# TEST 6: Obtener la lista de componentes, sin proporcionar una cookie de sesion
	# Status esperado: 401

	# TEST 7 : Obtener la lista de componentes, proporcionando una cookie de sesion
	# Status esperado: 200

	# TODO TESTs Metodo GET Componente (obtener info de un componente en particular)
	# TODO TESTs Metodo POST Componente (modificar info de un componente)
	# TODO TESTs Metodo DELETE Componente 

	# POST-TEST 1: Hacer logout en el sistema mediante googleplus

if __name__ = "__main__":
	main()