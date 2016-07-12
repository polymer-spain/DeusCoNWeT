/*global angular */
angular.module('picbit').service('$backend', ['$http', '$location', '$rootScope', '$cookies', function ($http, $location, $rootScope, $cookies) {

  'use strict';

  if ($location.host() === "localhost"){
    this.endpoint = "http://" + $location.host() + ":" + $location.port();
  }else {
    this.endpoint = 'https://' + $location.host(); // Dominio bajo el que ejecutamos
  }

  /* Envia el token y el identificador del token correspondiente a una red social */
  /* ¿¿ Control de errores ??*/
  this.sendData = function (token, tokenId, userId, redSocial, oauthVerifier) {
    var request, uri, params;

    uri = this.endpoint + '/api/oauth/' + redSocial + '/login';
    /* Añadimos los parametros necesarios */
    params = 'token_id=' + tokenId + '&access_token=' + token;

    /* Si se indica el userId, se incluye en la peticion */
    params += userId ? '&user_identifier=' + userId : '';

    /* Si se trata de twitter añadimos el oauth_verifier*/
    params += oauthVerifier && redSocial === 'twitter' ? '&oauth_verifier=' + oauthVerifier : '';
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };
    /* Devolvemos la promesa*/
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.signup = function (token, tokenId, userId, redSocial, oauthVerifier) {
    var request, uri, params;

    uri = this.endpoint + '/api/oauth/' + redSocial + '/signup';
    /* Añadimos los parametros necesarios */
    params = 'token_id=' + tokenId + '&access_token=' + token;

    /* Si se indica el userId, se incluye en la peticion */
    params += userId ? '&user_identifier=' + userId : '';

    /* Si se trata de twitter añadimos el oauth_verifier*/
    params += oauthVerifier && redSocial === 'twitter' ? '&oauth_verifier=' + oauthVerifier : '';
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };
    /* Devolvemos la promesa*/
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.getUserId = function (tokenId, redSocial) {
    var request, uri;
    uri = this.endpoint + '/api/oauth/' + redSocial + '/credenciales/' + tokenId;

    request = {
      methor: 'get',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  /* Permite elegir un usuario por user_id */
  this.getUser = function (userId) {
    var request, uri;
    uri = this.endpoint + '/api/usuarios/' + userId;

    request = {
      method: 'get',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.syncGetUser = function (userId) {
    var request, uri;
    uri = this.endpoint + '/api/usuarios/' + userId;
    request = new XMLHttpRequest();

    request.open('GET', uri, false);
    request.send();

    return request;
  };

  /* Contacto: envia un email al backend */
  this.sendEmail = function (message, sender, subject) {
    var request, uri, params;

    uri = this.endpoint + '/api/contact';
    params = 'action=contact&message=' + message + '&sender=' + sender;

    if (subject) {
      params += '&subject=' + subject;
    }
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.sendSub = function (name, sender, surname) {
    var request, uri, params;
    uri = this.endpoint + '/api/subscriptions';
    params = 'name=' + name + '&email=' + sender + '&surname=' + surname;
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.logout = function () {
    var request, uri, socialnetwork;
    socialnetwork = $cookies.get('social_network') || 'googleplus';
    uri = this.endpoint + '/api/oauth/' + socialnetwork + '/logout';
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };
    $rootScope.user = undefined;
    $rootScope.isLogged = false;
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.getSingleToken = function(socialNetwork, tokenid) {
    var request, uri;

    request = new XMLHttpRequest();

    uri = this.endpoint + '/api/oauth/' + socialNetwork + '/credenciales/' + tokenid;
    request.open('GET', uri, false);
    request.send();

    return request;
  };
  this.getTokens = function(tokensId) {
    var access_tokens, item, request, data;
    access_tokens = {};
    while(tokensId.length > 0) {
      item = tokensId.pop();
      request  = this.getSingleToken(item.social_network, item.token_id);
      data = JSON.parse(request.response);
      access_tokens[item.social_network] = data.access_token;
    }
    return access_tokens;
  };

  this.addTokens = function(socialNetwork, token_id,access_token, user_id){
    var uri,
    params={
      token_id:token_id,
      access_token: access_token
    },
    request, verb;

    switch (socialNetwork) {
      case 'github':
      uri = this.endpoint + '/api/oauth/github/credenciales';
      verb = 'POST';
      break;
      case 'twitter':
      uri = '/api/oauth/twitter/signup';
      verb = 'POST';
      params.user_id = user_id;
      break;
      case 'Instagram':
      uri = '/api/instagram/credenciales';
      verb = 'PUT';
      break;
      case 'googleplus':
      uri = '/api/oauth/googleplus/signup';
      verb = 'POST';
      params.user_id = user_id;
      break;
      case 'facebook':
      uri = '/api/oauth/facebook/signup';
      verb = 'POST';
      params.user_id = user_id;
      break;
    }

    request = {
      method: verb,
      url: uri,
<<<<<<< HEAD
      headers: {'Content-Type': 'application/x-www-form-urlencoded',
      params: params
    }
  };

  return $http(request);
};
}]);
