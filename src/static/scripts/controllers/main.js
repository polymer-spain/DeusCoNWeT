'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */

angular.module('PolymerBricks')
  .controller('MainCtrl', function ($scope,$location,$timeout) {

  $scope.status = false;

  $scope.logged = function(e){
    $scope.$apply(function(){
      // escondemos el popup y cambiamos la direccion del usuario
      $scope.hidePopup();
      // cambiamos el botton

      var button = document.querySelector('#nameId');
      // Selecionar el nombre del usuario
      button.innerHTML="Desconectar"
      // Seleccionar la imagen del perfin
      // button.src=""
      // Cambiamos a la funcion de logout
      $scope.status = true;
      $location.path('/user/'+e.detail.redSocial+'_'+e.detail.userId);
    });
  };

  $scope.changeView = function(view){
    $location.path(view); // path not hash
  };

  $scope.logout = function() {
    var button = document.querySelector('#nameId');
    // Selecionar el nombre del usuario
    button.innerHTML="Entrar"
    $location.path('/');
    $scope.status = false;
  }
  /* Escuhas de los botones*/
  document.querySelector('body').addEventListener('google-logged',$scope.logged);
  document.querySelector('body').addEventListener('linkedin-logged',$scope.logged);
  document.querySelector('body').addEventListener('github-logged',$scope.logged);
  document.querySelector('body').addEventListener('instagram-logged',$scope.logged);
  document.querySelector('body').addEventListener('twitter-logged',$scope.logged);
  document.querySelector('body').addEventListener('facebook-logged',$scope.logged);
  document.querySelector('body').addEventListener('sof-logged',$scope.logged);

  $scope.popup = false;

  $scope.showPopup = function(){
    if (!$scope.status)
      $scope.popup = true;
    else 
      $scope.logout();
  };
  $scope.hidePopup = function(){
    $scope.popup = false;
  };

});
