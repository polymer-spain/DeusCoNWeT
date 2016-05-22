/*global angular, document, console*/
angular.module('picbit').controller('MainController', ['$scope', '$location', '$timeout', '$backend', '$http', '$window', '$cookies', '$rootScope', 'RequestLanguage', function ($scope, $location, $timeout, $backend, $http, $window, $cookies, $rootScope, RequestLanguage) {

  'use strict';

/*  if ($cookies.get('user')) {
    $backend.getUser($cookies.get('user')).then(function(response) {
      $rootScope.user = response.data;
    });
  }*/

  $rootScope.isLogged = $rootScope.user ? true : false; // Registrar el estado de logueado
  $scope.domain = 'https://' + $location.host(); // Dominio bajo el que ejecutamos
  if ($location.host() == 'localhost') {
    $scope.domain = 'http://localhost:8080';
  }
  $scope.sended = false; // popup de notificar
  $scope.idioma = $cookies.get('language') || $window.navigator.language;
  $scope.popupOpened = false;

  /* Listen popup when he's close */
  $scope.loadListener = function(){
    document.querySelector('#loginModal').addEventListener('iron-overlay-closed', function(){
      $scope.$apply(function() {
        $scope.popupOpened = false;
      });
    });
  };
  $scope.languageRequest = function(file){
    RequestLanguage.language(file).success(function (data){
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
    });
  };

  $scope.changelanguage = function (language, closeMenu) {
    var file;
    $scope.idioma = language;
    $cookies.put('language', language);
    file = $scope.idioma === 'es' ? 'es_es.json' : 'en_en.json';
    $scope.languageRequest(file);

    if(closeMenu) {
      document.querySelector('#language').close();
    }
  };

  /* Monitorizamos el lenguage */

  if ($scope.idioma === 'es') {
    $scope.languageRequest('es_es.json');
    $cookies.put('language', 'es');
  } else {
    $scope.languageRequest('en_en.json');
    $cookies.put('language', 'en');
  }

  $scope.loginProcess = function(userData){
    /* Cogemos el identificador del usuario */
    $rootScope.registerToken = userData.token
    function newUser(userData) {
      $rootScope.register = {token: userData.token, redSocial: userData.redSocial, tokenId: userData.userId, oauthVerifier: userData.oauth_verifier};
      $scope.changeView('/selectId');
    }
    $rootScope.token = userData.token;
    if ($location.$$path.indexOf('profile') === -1) {
      $backend.getUserId(userData.userId, userData.redSocial)
        .then(function (responseUserId) { /* Si devuelve un 200, ya existe el usuario*/
        /* Pedimos la información del usuario y la almacenamos para poder acceder a sus datos */
        $rootScope.user = responseUserId.data;
        $backend.sendData(userData.token, userData.userId, responseUserId.data.user_id, userData.redSocial, userData.oauth_verifier)
          .then(function() {
          $scope.changeView('/user/' + $rootScope.user.user_id);
        }, function(responseLogin) {
          console.error('Error ' + responseLogin.status + ': al intentar mandar los datos de login'); 
        });
      }, function(){newUser(userData)});
    } else {
      $backend.sendData(userData.token, $rootScope.user.user_id, userData.redSocial);
    }
  };

  $scope.logged = function (e) {
    $scope.$apply(function () {
      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario

      if (e.detail.redSocial === 'googleplus') { // Comprobamos si es google para buscar el id
        var uri;
        uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + e.detail.token;
        $http.get(uri).success(function (responseData) {
          e.detail.userId = responseData.id;
          $scope.loginProcess(e.detail);
          // ¿Por qué twitter si tiene salida de error si no funciona la peticion mientras que los demas(Google+ y facebook) no?)
        });
      } else if (e.detail.redSocial === 'twitter') {
        var uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
        $http.get(uri).success(function (responseData) {
          e.detail.userId = responseData.token_id;
          $scope.loginProcess(e.detail);
        }).error(function() {
          console.log('Problemas al intentar obtener el token_id de un usuario' );
        });
      } else {
        $scope.loginProcess(e.detail);
      }
    });
  };

  $scope.changeView = function (view, name) {
    $location.hash('');
    if (name) {
      $scope.user ? $location.path('user/' + $scope.user.user_id) : $location.path('');
    }else {
      $location.path(view); // path not hash
    }
  };

  /* NOTE its needed because the dropmenu do not correctly the binding.
   * Its know path but it dont redirect to them because the binding is done after.
   */
  $scope.goto = function(addr, parent) {
    switch(addr) {
      case 'home':
        $scope.changeView('user/' + $rootScope.user.user_id);
        break;
      case 'profile':
        $scope.changeView('user/' + $rootScope.user.user_id + '/profile');
        break;
    }
    if (parent){
      document.getElementById(parent).close();
    }
  };

  $scope.logout = function (parent) {
    $backend.logout().then(function() {
      if (parent){
        document.getElementById(parent).close();
      }
      $scope.changeView('/');
    }, function(response){
      console.error('Error ' + response.status + ': Fallo al intentar realizar un logout del usurio ' + $rootScope.user.name);
    });
  };
  $scope.showPopup = function (e) {
    var element = e.target;
    var id = element.getAttribute('data-dialog') || element.parentElement.getAttribute('data-dialog');
    var dialog = document.getElementById(id);
    if (dialog && !$rootScope.isLogged) {
      dialog.open();
      $scope.popupOpened = true;
    }
  };
  $scope.hidePopup = function() {
    var element = document.getElementById('loginModal');

    if (element) {
      element.close();
    }
  };

  $window.addEventListener('scroll', function() {
    $scope.$apply(function() {
      var size = 	document.body.scrollTop;
      $scope.scrolled = size > 0;
    });
  });

  $scope.dropmenu  =  function(){
    document.querySelector('#dropmenu').toggle();
  };

  $scope.calculateWidthUserDropdown = function() {
    return '200px';
  };

  /* Escuhas de los botones*/
  (function(){
    document.querySelector('body').addEventListener('google-logged', $scope.logged);
    document.querySelector('body').addEventListener('linkedin-logged', $scope.logged);
    document.querySelector('body').addEventListener('github-logged', $scope.logged);
    document.querySelector('body').addEventListener('instagram-logged', $scope.logged);
    document.querySelector('body').addEventListener('twitter-logged', $scope.logged);
    document.querySelector('body').addEventListener('facebook-logged', $scope.logged);
    document.querySelector('body').addEventListener('sof-logged', $scope.logged);
  })();
}]);
