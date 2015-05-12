/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */


angular.module('picbit').controller('MainCtrl', function ($scope, $location, $timeout, $backend, $http) {
  'use strict';
  $scope.status = false;
  $scope.domain = "https://" + $location.host();
  $scope.shadow = false;
  $scope.sended = false;


  $scope.logged = function (e) {
    $scope.$apply(function () {

      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
      if (e.detail.redSocial === 'twitter') {
        /* Provisional hasta que se implemente el nombre de usuario */

        $scope.changeView('/user/' + e.detail.redSocial + '_' + e.detail.userId);
      } else if (e.detail.redSocial === 'googleplus') { // Comprobamos si es google para buscar el id
        var uri, button;
        uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + e.detail.token;
        $http.get(uri).success(function (data) {
          /* Provisional hasta que se implemente el nombre de usuario */
          
          $backend.sendData(e.detail.token, data.id, e.detail.redSocial,function(){
            $scope.changeView('/user/' + e.detail.redSocial + '_' + data.id);
          });
        });
      } else {
        $scope.changeView('/user/' + e.detail.redSocial + '_' + e.detail.userId);
        $backend.sendData(e.detail.token, e.detail.userId, e.detail.redSocial);
      }
      // cambiamos el botton
      $scope.logOutButton();

    });
  };
  $scope.logOutButton = function () {
    var button = document.querySelector('#nameId');
    button.innerHTML = "Desconectar";
    // Seleccionar la imagen del perfin
    // button.src=""
    // Cambiamos a la funcion de logout
    $scope.status = true;
  };

  $scope.changeView = function (view) {
    $location.hash('');
    $location.path(view); // path not hash
  };

  $scope.logout = function () {
    var button = document.querySelector('#nameId');
    // Selecionar el nombre del usuario
    button.innerHTML = "Entrar";
    $scope.changeView('/');
    $scope.status = false;
  };

   /* Escuhas de los botones*/
  document.querySelector('body').addEventListener('google-logged', $scope.logged);
  document.querySelector('body').addEventListener('linkedin-logged', $scope.logged);
  document.querySelector('body').addEventListener('github-logged', $scope.logged);
  document.querySelector('body').addEventListener('instagram-logged', $scope.logged);
  document.querySelector('body').addEventListener('twitter-logged', $scope.logged);
  document.querySelector('body').addEventListener('facebook-logged', $scope.logged);
  document.querySelector('body').addEventListener('sof-logged', $scope.logged);
  $scope.popup = false;

  $scope.showPopup = function () {
    if (!$scope.status) {
      $scope.popup = true;
      $scope.shadow = true;
    } else {
      $scope.logout();
    }
  };
  $scope.hidePopup = function () {
    $scope.popup = false;
    $scope.shadow = false;
  };
});
