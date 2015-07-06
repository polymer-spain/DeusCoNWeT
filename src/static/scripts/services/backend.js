/*global angular */
angular.module("picbit").service("$backend", function ($http, $location) {

  "use strict";

  this.endpoint = "https://" + $location.host();

  /* Envia el token y el identificador del token correspondiente a una red social */
  this.sendData = function (token, tokenId, redSocial, callback, errorCallback) {
    var request, uri, params;
    uri = this.endpoint + "/api/oauth/" + redSocial;
    params = "token_id=" + tokenId + "&access_token=" + token + "&action=login";
    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };
    $http(request).success(function (data) {
      if (callback) {
        callback(data);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };

  /* Contacto: envia un email al backend */
  this.sendEmail = function (message, sender, subject, callback, errorCallback) {
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
    $http(request).success(function (data, status) {
      if (callback) {
        callback(data, status);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };

  this.sendSub = function (name, sender, surname, callback, errorCallback) {
    var request, uri, params;
    uri = this.endpoint + "/api/subscriptions";
    params = "name=" + name + "&email=" + sender + "&surname=" + surname;
    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };

    $http(request).success(function (data, status) {

      if (callback) {
        callback(data, status);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };

  this.logout = function (callback, errorCallback) {
    var request, uri, params;

    uri = this.endpoint + "/api/oauth/googleplus";
    params = "action=logout";

    request = {
      method: "post",
      url: uri,
      headers: {"Content-Type": "application/x-www-form-urlencoded"},
      data: params
    };
    $http(request).success(function (data, status) {
      if (callback) {
        callback(data, status);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        callback(data, status);
      }
    });
  };


});
