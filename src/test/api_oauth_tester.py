# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

# Script para hacer pruebas a la API de Oauth de PicBit (api/oauth/{red_social})
# Uso: ./api_oauth_tester red_social

connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
headers = {"User-Agent": "PicBit-App"}

def make_request(method, request_uri, params, status_ok):
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
  	responseData = response.read()
  	if not response.status == status_ok:
  		print ">>> STATUS: ERROR" + str(response.status)
  		print responseData
  	else:
  		print ">>> STATUS: OK"
  		print response.getheader('Set-Cookie')

def main():
	red_social=sys.argv[1]
	basePath = "/api/oauth/" + red_social
	
	#Logins
	# TEST 1
	request_uri = basePath + "?action=login"
	print "\nTEST 1: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
	params = urllib.urlencode({'token_id': "idGoogle", 'access_token': "googleTEST"})
	make_request("POST", request_uri, params,201)

	# TEST 2
	request_uri = basePath + "?action=login"
	print "\nTEST 2: Haciendo petición POST a " + request_uri + " (login y actualizar credenciales)\n Status esperado: 200"
	params = urllib.urlencode({'token_id': "idGoogle", 'access_token': "googleModifyTEST"})
	make_request("POST", request_uri, params,200)	

	# TEST 3
	request_uri = basePath + "?action=login"
	print "\nTEST 3: Haciendo petición POST a " + request_uri + " (login)\n Status esperado: 201"
	params = urllib.urlencode({'token_id': "idGoogle2", 'access_token': "googleTEST"})
	make_request("POST", request_uri, params,201)

	#Logouts
	# TEST 4
	request_uri = basePath + "?action=logout"
	print "\nTEST 4: Haciendo petición POST a " + request_uri + " (logout sin cookie de sesion)\n Status esperado: 400"
	params = urllib.urlencode({})
	make_request("POST", request_uri, params,400)

	# TEST 5
	# print "TEST 5: Haciendo petición POST a " + request_uri + "(logout con cookie de sesion)\n Status esperado: 200"
	#request_uri = basePath + "?action=login"
	#params = urllib.urlencode({'token_id': "idGoogle", 'access_token': "googleTEST"})
	#make_request("POST", request_uri, params,201)

	# TEST 6
	# Get (Sin cookie)
	request_uri = basePath + "?action=login"
	print "\nTEST 6: Haciendo petición GET a " + request_uri + " (obtener credenciales)\n Status esperado: 400"
	params = urllib.urlencode({})
	make_request("GET", request_uri, params,400)

	# Cerramos conexión
	connection.close()


if __name__ == "__main__":
    main()