#!/usr/bin/python
# -*- coding: utf-8 -*-
# Test_utils.py: Módulo con operaciones para realizar pruebas a la API REST del sistema

import sys
import httplib
import urllib
import json
import time
import ssl
# Global vars
connection = None
remoteConnection = True
nTest = 0
nTestOK = 0
nTestError = 0
nPreTest = 0

# Auxiliar class to color the program outputs
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def openConnection(remote=True):
    global connection,remoteConnection
    if remote:
        connection = httplib.HTTPSConnection("centauro.ls.fi.upm.es",443,context=ssl._create_unverified_context())
    else:
        connection = httplib.HTTPConnection("localhost:8001")
        remoteConnection = False

def closeConnection():
    global connection
    connection.close()

def do_login_or_signup(social_network, token_id, access_token, user_identifier):
    """
    Metodo do_login_or_signup: Realiza el login o el registro en PicBit
    Contemplado como preTest, para el testeo de las APIs de PicBit.
    Retorna el id de sesion generado
    Parametros:
        social_network: Red social mediante la que se desea realizar el login en el sistema
        token_id: token id de usuario
        access_token: access_token de usuario
        user_identifier: id de usuario
    """
    print "PRETEST: Login/Sign-up de usuario ", user_identifier, " en el sistema"
    session = None
    if social_network in ["googleplus", "facebook"]:
        request_uri = "/api/oauth/" + social_network + "/login"
        params = urllib.urlencode({'token_id': token_id, 'access_token': access_token})
        session = make_request("POST", request_uri, params, 200, None, True, True)
        # Si no se ha podido realizar el login en el sistema, registramos al usuario (Signup)
        if session == None:
            request_uri = "/api/oauth/" + social_network + "/signup"
            params = urllib.urlencode({'token_id': token_id, 'access_token': access_token,
                'user_identifier': user_identifier})
            session = make_request("POST", request_uri, params, 201, None, True, True)
    return session

def do_logout(social_network, session, printSession=False):
    request_uri = '/api/oauth/' + social_network + '/logout'
    params = urllib.urlencode({})
    print "POSTEST: Logout de usuario en el sistema"
    print "Ignorar el status de este caso"
    make_request("POST", request_uri, params, 200, session, printSession)


def make_request(method, request_uri, params, status_ok, session, printHeaders=False, preTest=False):
    """
    Metodo make_request: Realiza llamadas HTTP a la API REST, retornando la
    cookie de sesion enviada por el servidor.
    Parametros:
        method: metodo HTTP de la peticion
        request_uri: URL de la peticion
        params: parametros de la peticion
        status_ok: status HTTP de retorno esperado de la peticion
        session: cookie de sesion para adjuntar en la peticion
        printHeaders: Si es True, se imprimirán los Headers de peticion y respuesta (Valor por defecto: False)
        preTest: Indica si la petición a realizar se corresponde con un pre-test, y no es significativo el status HTTP de retorno
                (Valor por defecto: False)
    """
    global connection, nTest, nTestOK, nTestError, remoteConnection, nPreTest
    nTest += 1
    print "Realizando petición ", method, " ", request_uri
    headers = {"User-Agent": "PicBit-App","Content-Type":"application/x-www-form-urlencoded"}
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
        if not preTest:
            nTestError += 1
        else:
            nPreTest += 1

        # We print a Log for the response obtained from the server
        print bcolors.FAIL + "\t!!! STATUS: ERROR (STATUS " + str(response.status) + ")"
        print "\tDatos de la respuesta: " + responseData + bcolors.ENDC +"\n"

    else:
        if not preTest:
            nTestOK += 1
            text_color = bcolors.OKGREEN
        else:
            nPreTest += 1
            text_color = bcolors.OKBLUE

        # We print a Log for the response obtained from the server
        print text_color + "\t>>> STATUS: OK (STATUS " + str(response.status) + ")"
        print "\tRESPUESTA: ", responseData + bcolors.ENDC + "\n"

    # Prints the response session cookie, if proceed
    if not session_cookie == None and printHeaders:
        print "\tCookie de la respuesta: " + session_cookie + "\n"

    # We introduce a sligth latency (1 second) in order to emulate a "remote" behavior of the tests against the dev_server
    if not remoteConnection:
        time.sleep(1)

    # We return the session cookie of the request, useful for the subsequent calls to the PicBit REST API
    return session_cookie

def tests_status():
    print '==============================='
    print bcolors.BOLD + 'Tests totales: ', nTest
    print 'Pre-Tests: ', nPreTest
    print 'Tests: ', nTest - nPreTest
    print '-------------------------------'
    print 'Test Ok: ', nTestOK
    print "Tests Erróneos: ", nTestError, bcolors.ENDC
    print '==============================='
