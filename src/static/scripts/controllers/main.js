/*global angular, document, window, console*/
angular.module("picbit").controller("MainController", ["$scope", "$location", "$timeout", "$backend", "$http", "$window", "$cookies", "$rootScope", "RequestLanguage", function ($scope, $location, $timeout, $backend, $http, $window, $cookies, $rootScope, RequestLanguage) {

  "use strict";

  if ($cookies.get("user")) {
    $backend.getUser($cookies.get("user")).then(function(response) {
      $rootScope.user = response.data;
    });
  }

  $rootScope.isLogged = $rootScope.user ? true : false; // Registr el stado de logueado
  $scope.domain = "https://" + $location.host(); // Dominio bajo el que ejecutamos
  $scope.shadow = false; // Sombra del popup
  $scope.sended = false; // popup de notificar
  $scope.idioma = $cookies.get("language") || $window.navigator.language;

  $scope.languageRequest = function(file){
    RequestLanguage.language(file).success(function (data){
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
    });
  };

  $scope.changelanguage = function (language) {
    var file;
    $scope.idioma = language;
    $cookies.put("language", language);
    file = $scope.idioma === "es" ? "es_es.json" : "en_en.json";
    $scope.languageRequest(file);
    document.querySelector("#language").$.label.innerHTML = $scope.languageSelected;
  };

  /* Monitorizamos el lenguage */

  if ($scope.idioma === "es") {
    $scope.languageRequest("es_es.json");
    $scope.idioma = "es";
    $cookies.put("language", "es");
  } else {
    $scope.languageRequest("en_en.json");
    $scope.idioma = "en";
    $cookies.put("language", "en");

  }
  $scope.loginProcess = function(userData){
    /* Cogemos el identificador del usuario */
    function newUser(userData) {
      $rootScope.register = {token: userData.token, redSocial: userData.redSocial, tokenId: userData.userId};
      $scope.changeView("/selectId"); 
    }
    if ($location.$$path.indexOf("profile") === -1) {
      $backend.getUserId(userData.userId, userData.redSocial)
        .then(function (responseUserId) { /* Si devuelve un 200, ya existe el usuario*/
        /* Pedimos la información del usuario y la almacenamos para poder acceder a sus datos */
        $rootScope.user = responseUserId.data;
        $backend.sendData(userData.token, userData.userId, responseUserId.data.user_id, userData.redSocial)
          .then(function() {
          $scope.changeView("/user/" + $rootScope.user.user_id);
        }, function(responseLogin) {
          console.error("Error " + responseLogin.status + ": al intentar mandar los datos de login"); 
        });
      }, newUser(userData));
    } else {
      $backend.sendData(e.detail.token, $rootScope.user.user_id, e.detail.redSocial);
    }
  };

  $scope.logged = function (e) {
    $scope.$apply(function () {
      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario

      if (e.detail.redSocial === "googleplus") { // Comprobamos si es google para buscar el id
        var uri;
        uri = "https://www.googleapis.com/plus/v1/people/me?access_token=" + e.detail.token;
        $http.get(uri).success(function (responseData) {
          e.detail.userId = responseData.id;
          $scope.loginProcess(e.detail);
        });
      } else if (e.detail.redSocial === "twitter") {
        var uri;
        uri = this.endpoint + "/api/oauth/twitter/authorization/" + oauthVerifier;
        $http.get(uri).success(function (responseData) {
          e.detail.userId = responseData.token_id;
          $scope.loginProcess(e.detail);
        }).error(function() {
          console.log("Problemas al intentar obtener el token_id de un usuario" );
        };

      } else {
        $scope.loginProcess(e.detail);
      } 
    });
  };

  $scope.changeView = function (view) {
    $location.hash("");
    $location.path(view); // path not hash
  };
  /* NOTE Necesario porque el dropmenu no hace correctamente el binding: 
   * Si sabe la direccion pero no manda a ella porque el binding se hace posterior
  */
  $scope.goto = function(addr) {
    switch(addr) {
      case "home":
        $scope.changeView("user/" + $rootScope.user.user_id);
        break;
      case "profile":
        $scope.changeView("user/" + $rootScope.user.user_id + "/profile");
        break;
    }
  };
  $scope.logout = function () {
    $backend.logout().then(function() {
      $scope.changeView("/");
    }, function(response){
      console.error("Error " + response.status + ": Fallo al intentar realizar un logout del usurio " + $rootScope.user.name);
    });
  };
  $scope.showPopup = function () {
    if (!$rootScope.isLogged) {
      $scope.popup = true;
      $scope.shadow = true;
      window.onkeydown = $scope.listenEscKeydown;
    } else {
      $scope.changeView("user/213");
    }
  };
  $scope.hidePopup = function () {
    $scope.popup = false;
    $scope.shadow = false;
    window.removeEventListener("onkeydown", $scope.listenEscKeydown);
  };

  $window.addEventListener("scroll", function() {
    $scope.$apply(function() {
      var size = 	document.body.scrollTop;
      $scope.scrolled = size > 0;
    });
  });

  $scope.dropmenu  =  function(){
    document.querySelector("#dropmenu").toggle();
  };

  $scope.listenEscKeydown = function (event) {
    $scope.$apply(function() {
      if (event.keyCode === 27) {
        $scope.hidePopup();
      }
    });
  };

  /* Escuhas de los botones*/
  (function(){
    document.querySelector("body").addEventListener("google-logged", $scope.logged);
    document.querySelector("body").addEventListener("linkedin-logged", $scope.logged);
    document.querySelector("body").addEventListener("github-logged", $scope.logged);
    document.querySelector("body").addEventListener("instagram-logged", $scope.logged);
    document.querySelector("body").addEventListener("twitter-logged", $scope.logged);
    document.querySelector("body").addEventListener("facebook-logged", $scope.logged);
    document.querySelector("body").addEventListener("sof-logged", $scope.logged);
  })()
}]);
