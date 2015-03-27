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
  /* Funcion de retorno de log in*/
  $scope.logged = function(e){
    console.log(e.detail);

    $scope.$apply(function(){
      $scope.hidePopup();
      $location.path('/user/'+e.detail.redSocial+'_'+e.detail.userId);
    });
  };
  $scope.changeView = function(view){
    $location.path(view); // path not hash
  };
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
    $scope.popup = true;
  };
  $scope.hidePopup = function(){
    $scope.popup = false;
  };

});
