# -*- coding: utf8 -*-
import sys, urllib
import test_utils

# Script para hacer pruebas a la API de Componentes de PicBit (api/componentes)
# Uso: ./api_componentes_tester [borrado]

def main():
	test_utils.openConnection()
	basepath = "/api/componentes"
	session1 = None
	option = None
	# Obtenemos parámetros opcionales del programa
	if len(sys.argv) == 2:
		option = sys.argv[2]

	if option == None:
		# PRE-TEST 1: Hacer login en el sistema mediante googleplus
		request_uri = "/api/oauth/googleplus/login"
		print "\nPRETEST 1: Haciendo petición POST a " + request_uri + " (login)\n Ignorar el status de este caso"
		token_id_login = "idgoogle"
		access_token_login = "googleTEST"
		params = urllib.urlencode({'token_id': token_id_login, 'access_token':access_token_login})
		session1 = test_utils.make_request("POST", request_uri, params, 201, None)

		# print "##############################################################################"
		# # TEST 1
		# print "TEST 1: : Obtener la lista de componentes. Debe retornar una lista vacia de componentes"
		# print "Status esperado: 204 "
		# request_uri = basepath
		# params = urllib.urlencode({})
		# test_utils.make_request("GET", request_uri, params, 204, session1)	

		# # TESTs relativos a la operación PUT lista de componentes (Subir un componente al sistema) 
		# # TEST 2
		# print "TEST 2: Subir un componente al sistema, proporcionando una URI incorrecta."
		# print "Status esperado: 404 "
		# # request_uri = basepath
		# params = urllib.urlencode({'url': 'https://github.com/JuanFryS/badURI',
	 #            'component_id': 'twitterTimeline',
	 #            'description': 'Web component for obtain the timeline of Twitter using Polymer',
	 #            'social_network': 'Twitter',
	 #            'input_type': 'None',
	 #            'output_type': 'tweet',
	 #            'listening': 'None'
		# })
		# test_utils.make_request("GET", request_uri, params, 204, session1)

		# print "##############################################################################"

		# # TEST 3
		# print "TEST 3: Subir un componente al sistema, proporcionando un parametro erróneo (red social)."
		# print "Status esperado: 400 "
		# request_uri = basepath
		# params = urllib.urlencode({'url': 'https://github.com/JuanFryS/twitter-timeline',
	 #            'component_id': 'twitterTimeline',
	 #            'description': 'Web component for obtain the timeline of Twitter using Polymer',
	 #            'social_network': 'RedError' ,
	 #            'input_type': 'None',
	 #            'output_type': 'tweet',
	 #            'listening': 'None'
		# })
		# test_utils.make_request("PUT", request_uri, params, 400, None)

		# # TEST 4
		# print "TEST 4: Subir un componente al sistema, proporcionando menos parámetros de los necesarios."
		# print "Status esperado: 400 "
		# # request_uri = basepath
		# params = urllib.urlencode({'url': 'https://github.com/JuanFryS/twitter-timeline',
	 #            'component_id': 'twitterTimeline',
	 #            'description': 'Web component for obtain the timeline of Twitter using Polymer',
	 #            'social_network': 'Twitter' ,
	 #            'input_type': 'None',
	 #            'output_type': 'tweet'
		# })
		# test_utils.make_request("PUT", request_uri, params, 400, None)

		# # Subimos dos componentes al sistema
		# # TEST 5
		# print "TEST 5: Subir un componente al sistema (componente 1)."
		# print "Status esperado: 200 "
		# # request_uri = basepath
		# params = urllib.urlencode({'url': 'https://github.com/JuanFryS/twitter-timeline',
	 #            'component_id': 'twitterTimeline',
	 #            'description': 'Web component for obtain the timeline of Twitter using Polymer',
	 #            'social_network': 'Twitter' ,
	 #            'input_type': 'None',
	 #            'output_type': 'tweet',
	 #            'listening': 'None'
		# })
		# test_utils.make_request("PUT", request_uri, params, 200, None)
		
		# # TEST 6: Subir un componente al sistema (componente 2).
		# print "TEST 6: Subir un componente al sistema (componente 2)."
		# print "Status esperado: 200 "
		# # request_uri = basepath
		# params = urllib.urlencode({'url': 'https://github.com/JuanFryS/instagram-timeline',
	 #            'component_id': 'instagram-timeline',
	 #            'description': 'Web component for obtain the timeline of the social network Instagram using Polymer',
	 #            'social_network': 'Instagram',
	 #            'input_type': 'None',
	 #            'output_type': 'photo',
	 #            'listening': 'None'
		# })
		# test_utils.make_request("PUT", request_uri, params, 200, None)

		# print "##############################################################################"
		
		# # TESTs Metodo GET Lista de componentes 
		# # TEST 7
		# print "TEST 7: Obtener la lista de componentes, sin proporcionar una cookie de sesion"
		# print "Status esperado: 401 "
		# request_uri = basepath
		# params = urllib.urlencode({})
		# test_utils.make_request("GET", request_uri, params, 401, None)	

		# # TEST 8
		# print "TEST 8: Obtener la lista de componentes, proporcionando una cookie de sesion (Sin parámetros)"
		# print "Status esperado: 200 "
		# request_uri = basepath
		# params = urllib.urlencode({})
		# test_utils.make_request("GET", request_uri, params, 200, session1)


		# # Casos de obtención de lista de componentes, aplicando criterios de filtrado
		# # TEST 9
		# print "TEST 9: Obtener la lista de componentes, proporcionando una cookie de sesion"
		# print "(parámetro de filtrado por red social)"
		# print "Status esperado: 200 "
		# request_uri = basepath + "?social_network=twitter"
		# params = urllib.urlencode({})
		# test_utils.make_request("GET", request_uri, params, 200, session1)

		# # TODO TESTs Metodo GET Componente (obtener info de un componente en particular)
		# print "TEST 10: Obtener la lista de componentes, proporcionando una cookie de sesion (Sin parámetros)"
		# print "Status esperado: 200 "
		# request_uri = basepath
		# params = urllib.urlencode({})
		# test_utils.make_request("GET", request_uri, params, 200, session1)	
		
		# # TODO TESTs Metodo POST Componente (modificar info de un componente)
		

		# POST-TEST 1: Hacer logout en el sistema mediante googleplus
	elif option == 'borrado':
		# TODO TESTs Metodo DELETE Componente 
		pass

	test_utils.closeConnection()
if __name__ == "__main__":
	main()