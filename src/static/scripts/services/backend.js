/*global angular */
angular.module("picbit").service("$backend", ["$http", "$location", "$rootScope", function ($http, $location, $rootScope) {

  "use strict";
  this.endpoint = "https://" + $location.host();

  /* Envia el token y el identificador del token correspondiente a una red social */
  /* ¿¿ Control de errores ??*/
  this.sendData = function (token, tokenId, userId, redSocial, oauthVerifier) {
    var request, uri, params;

    uri = this.endpoint + "/api/oauth/" + redSocial;
    /* Añadimos los parametros necesarios */
    params = "token_id=" + tokenId + "&access_token=" + token;

    /* Si se indica el userId, se incluye en la peticion */
    params += userId ? "&user_id=" + userId : "";

    /* Si se trata de twitter añadimos el oauth_verifier*/
    params += oauthVerifier && redSocial === "twitter" ? "&oauth_verifier=" + oauthVerifier : "";
    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };
    /* Devolvemos la promesa*/
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.getUserId = function (tokenId, redSocial, oauthVerifier) {
    var request, uri;

    uri = this.endpoint + "/api/oauth/" + redSocial + "/" + tokenId;
    request = {
      methor: "get",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"}
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  /* Permite elegir un usuario por user_id */
  this.getUser = function (userId) {
    var request, uri;
    uri = this.endpoint + "/api/usuarios/" + userId;

    request = {
      method: "get",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"}
    };
    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  /* Contacto: envia un email al backend */
  this.sendEmail = function (message, sender, subject) {
    var request, uri, params;

    uri = this.endpoint + "/api/contact";
    params = "action=contact&message=" + message + "&sender=" + sender;

    if (subject) {
      params += "&subject=" + subject;
    }
    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.sendSub = function (name, sender, surname) {
    var request, uri, params;
    uri = this.endpoint + "/api/subscriptions";
    params = "name=" + name + "&email=" + sender + "&surname=" + surname;
    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };

  this.logout = function () {
    var request, uri, params;

    uri = this.endpoint + "/api/oauth/googleplus";
    params = "action=logout";

    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };

    $rootScope.promise = $http(request);
    return $rootScope.promise;
  };


}]);
