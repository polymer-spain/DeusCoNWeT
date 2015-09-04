# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

connection = None
nTest = 0
nTestOK = 0
nTestError = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Módulo con operaciones para realizar pruebas a la API REST del sistema 
def openConnection(remote=True):
	global connection
	if remote:
		connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
	else:
		connection = httplib.HTTPConnection("localhost:8080")

def closeConnection():
	global connection
	connection.close()

def make_request(method, request_uri, params, status_ok, session, printHeaders=False):
	"""
	Metodo make_request: Realiza llamadas HTTP a la API REST, retornando la
	cookie de sesion enviada por el servidor. 
	Parametros:
		method: metodo HTTP de la peticion
		request_uri: URL de la peticion
		params: parametros de la peticion
		status_ok: status HTTP de retorno esperado de la peticion
		session: cookie de sesion para adjuntar en la peticion
		printHeaders: Si es True, se imprimirán los Headers de peticion y respuesta
	"""
	global connection, nTest, nTestOK, nTestError
	nTest += 1
	print "Realizando petición ", method, " ", request_uri
	headers = {"User-Agent": "PicBit-App"}
	session_cookie = None
	# Adds the cookie session header
	if not session == None:
		headers['Cookie']  = session
		if printHeaders:
			print "\tHEADERS " + headers['Cookie']
	
	# Request to API endpoint
	connection.request(method, request_uri, params, headers)
  	response = connection.getresponse()
	session_cookie = response.getheader('Set-Cookie')
  	responseData = response.read()
  	
  	# Prints the result of the request
  	if not response.status == status_ok:
  		nTestError += 1
  		print bcolors.FAIL + "\t!!! STATUS: ERROR (STATUS " + str(response.status) + ")"
  		print "\tDatos de la respuesta: " + responseData + bcolors.ENDC +"\n"
  	else:
  		nTestOK += 1
  		print bcolors.OKGREEN + "\t>>> STATUS: OK (STATUS " + str(response.status) + ")"
  		print "\tRESPUESTA: ", responseData + bcolors.ENDC + "\n"
  	
  	# Print the response session cookie, if proceed
	if not session_cookie == None and printHeaders:
  			print "\tCookie de la respuesta: " + session_cookie + "\n"
  	
  	return session_cookie

def tests_status():
	print "==============================="
	print bcolors.BOLD + "Tests ejecutados: " + str(nTest)
	print "Test Ok: ", nTestOK
	print "Tests Erróneos: ", nTestError, bcolors.ENDC
	print "==============================="