# -*- coding: utf8 -*-
import sys
import httplib, urllib
import json

connection = None

# Módulo con operaciones para realizar pruebas a la API REST del sistema 
def openConnection():
	global connection
	connection = httplib.HTTPSConnection("test-backend.example-project-13.appspot.com")
	# connection = httplib.HTTPConnection("localhost:8080")

def closeConnection():
	global connection
	connection.close()

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
	global connection
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