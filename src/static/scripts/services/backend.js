/*global angular */
angular.module('picbit').service('$backend', ['$http', '$location', '$rootScope', '$cookies',
function ($http, $location, $rootScope, $cookies) {

  'use strict';

  if ($location.host() === "localhost"){
    if ($location.port() === 443) {
      this.endpoint = "https://" + $location.host();
    } else {
      this.endpoint = "http://" + $location.host() + ":" + $location.port();
    }
  } else {
    this.endpoint = 'https://' + $location.host(); // Dominio bajo el que ejecutamos
  }

  // Envia el token y el identificador del token correspondiente a una red social
  // POST /api/oauth/{red_social}/login
  // PARAMS: @token_id
  //         @access_token
  //         [@user_identifier]
  //         [@oauth_verifier]

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
    $http(request);
    return $http(request);
  };

  //Function para crear un usuario en el sistema
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
    return $http(request);
  };

  // Retorna el identificador de un usuario basado en el identicador en una
  // determinada red social.
  this.getUserId = function (tokenId, redSocial) {
    var request, uri;
    uri = this.endpoint + '/api/oauth/' + redSocial + '/credenciales/' + tokenId;

    request = {
      methor: 'get',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };

    return $http(request);
  };

  // Devuelve un usuario basandose en su user_id en el sistema
  this.getUser = function (userId) {
    var request, uri;
    uri = this.endpoint + '/api/usuarios/' + userId;

    request = {
      method: 'get',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };
    return $http(request);
  };

  // (WARNING) Realiza una petición de un usuario de manera asincrona
  this.syncGetUser = function (userId) {
    var request, uri;
    uri = this.endpoint + '/api/usuarios/' + userId;
    request = new XMLHttpRequest();

    request.open('GET', uri, false);
    request.send();

    return request;
  };


  // Elimina y borra las credenciales de un usuario en el sistema
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
    return $http(request);
  };

  // (Warning) Pide el token de una red social basandose en su identificador
  // en dicha red social
  this.getSingleToken = function(socialNetwork, tokenid) {
    var request, uri;
    request = new XMLHttpRequest();

    uri = this.endpoint + '/api/oauth/' + socialNetwork + '/credenciales/' + tokenid;
    request.open('GET', uri, false);
    request.send();

    return request;
  };
  // (Warning) Peticion de tokens de manera recursiva
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

  // Añade un token de una recial al sistema
  this.addTokens = function(socialNetwork, token_id, access_token, user_id, oauth_verifier){
    var uri,
    data = {
      token_id:token_id,
      access_token:access_token
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
      data += '&user_identifier=' + user_id + "&oauth_verifier=" + oauth_verifier;
      break;
      case 'instagram':
      uri = '/api/oauth/instagram/credenciales';
      verb = 'PUT';
      break;
      case 'googleplus':
      uri = '/api/oauth/googleplus/signup';
      verb = 'POST';
      data += '&user_identifier=' + user_id;
      break;
      case 'facebook':
      uri = '/api/oauth/facebook/signup';
      verb = 'POST';
      data += '&user_identifier=' + user_id;
      break;
    }
    request = {
      method: verb,
      url: uri,
      data: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      }
    };
    return $http(request);
  };

  this.uploadImage = function(image, callback) {
    var data = new FormData();
    data.append('image', image);

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
      if (xhr.readyState === 4 && xhr.status === 200) {
        if (callback){
          callback(JSON.parse(xhr.responseText));
        }
      }
    };
    xhr.open('POST', 'https://api.imgur.com/3/upload', true);
    xhr.setRequestHeader('Authorization', 'Client-ID 5bb1a6c31384b7a');
    xhr.send(data);
  };
  this.updateProfile = function(values, user){
    var request, uri;
    uri = this.endpoint + '/api/usuarios/' + user + '/profile';
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: values
    };

    return $http(request);
  };

  this.getComponentInfo = function(){
    var uri = this.endpoint + '/api/componentes';
    var request = {
      method: 'get',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };
    return $http(request);
  };

  this.setNewNetwork = function(access_token, token_id,social_network){
    var uri = this.endpoint + '/api/oauth/' + social_network + '/credenciales';
    var params = 'access_token=' + access_token + '&token_id=' + token_id
    var request = {
      method: social_network === 'github'? 'POST': 'PUT',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };
    return $http(request);
  };
// /api/usuarios/{user_id}/assign
  this.assignComponent = function(user_id){
    var uri = this.endpoint + '/api/usuarios/' + user_id + '/assign';
    var request = {
      method: 'GET',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    };

    return $http(request);
  };
}
]);
