/*global angular, document, window, console */
angular.module("picbit").controller("MainController", ["$scope", "$location", "$timeout", "$backend", "$http", "$window", "$cookie", "$rootScope", function ($scope, $location, $timeout, $backend, $http, $window, $cookie, $rootScope) {
  "use strict";

  $scope.status = $cookie.get("session") !== undefined; // Registr el stado de logueado
  $scope.domain = "https://" + $location.host(); // Dominio bajo el que ejecutamos
  $scope.shadow = false; // Sombra del popup
  $scope.sended = false; // popup de notificar
  $scope.idioma = $cookie.get("language") || $window.navigator.language;
  $scope.user = {name: "Miguel", id: "2312"}; // Usuario logueado

  $scope.changelanguage = function (language) {
    var file;

    $scope.idioma = language;
    $cookie.put("language", language);
    file = $scope.idioma === "es" ? "es_es.json" : "en_en.json";

    $http.get("../../language/" + file).success(function (data) {
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
      document.querySelector("#language").$.label.innerHTML = $scope.languageSelected;
    }).error(function (data, status) {
      console.error(data, status);
    });
  };

  /* Monitorizamos el lenguage */

  if ($scope.idioma === "es") {
    $http.get("../../language/es_es.json").success(function (data) {
      $scope.language = data;
      $scope.idioma = "es";
      $cookie.put("language", "es");
      $scope.languageSelected = data.lang[$scope.idioma];
    }).error(function (data, status) {
      console.error(data, status);
    });
  } else {
    $http.get("../../language/en_en.json").success(function (data) {
      $scope.language = data;
      $scope.idioma = "en";
      $cookie.put("language", "en");
      $scope.languageSelected = data.lang[$scope.idioma];
    }).error(function (data, status) {
      console.error(data, status);
    });
  }

  $scope.logged = function (e) {
    $scope.$apply(function () {

      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
      if (e.detail.redSocial === "twitter") {
        /* Provisional hasta que se implemente el nombre de usuario */
        if ($location.$$path.indexOf("profile") === -1) {
          $scope.changeView("/user/" + e.detail.redSocial + "_" + e.detail.userId);
        }

      }
      else if (e.detail.redSocial === "googleplus") { // Comprobamos si es google para buscar el id
        var uri;
        uri = "https://www.googleapis.com/plus/v1/people/me?access_token=" + e.detail.token;
        $http.get(uri).success(function (responseData) {
          if ($location.$$path.indexOf("profile") === -1) {
            var userId = responseData.id;
            /* Cogemos el identificador del usuario */
            $backend.getUserId(userId, e.detail.redSocial)
              .then(function (userData) { /* Si devuelve un 200, ya existe el usuario*/
              /* Pedimos la información del usuario y la almacenamos para poder acceder a sus datos */
              $backend.getUser(userData.user_id).then(function(data){
                $rootScope.user = data;
              });
              /* Le mandamos a su home*/
              $scope.logOutButton();
              $scope.changeView("/user/" + userData.user_id);
              $backend.sendData(e.detail.token, userId, e.detail.redSocial);
            }, function () {
              /* Guardamos información para terminar su registro */
              $rootScope.register = {token: e.detail.token, redSocial: e.detail.redSocial, tokenId: userId};
              $scope.changeView("/selectId");
            });
          } else {
            $backend.sendData(e.detail.token, responseData.id, e.detail.redSocial);
          }
        });
      }
      else { /* Resto de redes sociales */
        if ($location.$$path.indexOf("profile") === -1) {
          var tokenId = e.detail.userId;
          /* Cogemos el identificador del usuario */
          $backend.getUserId(tokenId, e.detail.redSocial)
            .then(function (userData) { /* Si devuelve un 200, ya existe el usuario*/
            /* Pedimos la información del usuario y la almacenamos para poder acceder a sus datos */
            $backend.getUser(userData.user_id).then(function(data){
              $rootScope.user = data;
            });
            /* Le mandamos a su home*/
            $scope.logOutButton();
            $scope.changeView("/user/" + userData.user_id);
            $backend.sendData(e.detail.token, tokenId, e.detail.redSocial);
          }, function () {
            /* Guardamos información para terminar su registro */
            $rootScope.register = {token: e.detail.token, redSocial: e.detail.redSocial, tokenId: tokenId};
            $scope.changeView("/selectId");
          });
        } else {
          /*$backend.sendData(e.detail.token, data.id, e.detail.redSocial);*/
        }
      }
      // cambiamos el botton

    });
  };
  $scope.logOutButton = function () {
    // var button = document.querySelector("#nameId");
    // Seleccionar la imagen del perfin
    // button.src=""
    // Cambiamos a la funcion de logout
    $scope.status = true;
  };
  $scope.changeView = function (view) {
    $location.hash("");
    $location.path(view); // path not hash
  };

  $scope.logout = function () {
    //var button = document.querySelector("#nameId");
    // Selecionar el nombre del usuario

    $scope.changeView("/");
    $scope.status = false;
  };
  $scope.showPopup = function () {
    if (!$scope.status) {
      $scope.popup = true;
      $scope.shadow = true;
      window.onkeydown = $scope.listenEscKeydown;
    } else {
      //$scope.changeView("/user/" + $backend.getUser());
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

  /* Gestiona la sesion, mantiene logueado */
  if ($cookie.get("session")) {
    $scope.logOutButton();
    //$scope.changeView("/user/" + $backend.getUser());
  }
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
  document.querySelector("body").addEventListener("google-logged", $scope.logged);
  document.querySelector("body").addEventListener("linkedin-logged", $scope.logged);
  document.querySelector("body").addEventListener("github-logged", $scope.logged);
  document.querySelector("body").addEventListener("instagram-logged", $scope.logged);
  document.querySelector("body").addEventListener("twitter-logged", $scope.logged);
  document.querySelector("body").addEventListener("facebook-logged", $scope.logged);
  document.querySelector("body").addEventListener("sof-logged", $scope.logged);

}]);
