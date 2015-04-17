'use strict';

/**
 * @ngdoc function
 * @name polymerGeneratedAppApp.controller:SandboxCtrl
 * @description
 * # SandboxCtrl
 * Controller of the polymerGeneratedAppApp
 */
angular.module('PolymerBricks')
  .controller('userHomeCtrl', function ($scope) {
  $scope.menuStatus = false;

  $scope.showMenu = function(){

    if (!$scope.menuStatus){
      document.querySelector('#menu-button').icon='arrow-forward';
      document.querySelector('#menu').className="show";
      setTimeout(function(){
        $scope.$apply(function(){
          $scope.menuStatus = !$scope.menuStatus;
        });
      },500);
    }
    else {
      document.querySelector('#menu-button').icon='arrow-back';  
      document.querySelector('#menu').className="hidden";
      $scope.menuStatus = !$scope.menuStatus;
    }
  };

  $scope.buttonShow = function(event) {
    console.log(event);
    /*    document.querySelector('#menu-button').icon='arrow-forward';
    document.querySelector('#menu').className="show";
    setTimeout(function(){
      $scope.$apply(function(){
        $scope.menuStatus = true;
      });
    },500);*/
  }
});
