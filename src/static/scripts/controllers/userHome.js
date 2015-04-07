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

  $scope.list = '{ "github":"githubButton","facebook":"facebookButton","twitter":"twitterButton"}';
  
  $scope.menuStatus = false;
  $scope.showMenu = function(){

    if (!$scope.menuStatus){
      document.querySelector('#menu-icon').icon='arrow-forward';
      $scope.menuStatus = !$scope.menuStatus;
    }
    else {
      document.querySelector('#menu-icon').icon='arrow-back';  
      $scope.menuStatus = !$scope.menuStatus;
      $scope.selected = '';
    }
  };
  $scope.isSelected = function(event) {
    return $scope.selected === event; 
  }
  $scope.setSelected = function(event) {
    if ($scope.selected === event)
      $scope.selected = '';
    else 
      $scope.selected = event;
  };
  $scope.isMenuHidden = function(event) {
    return !$scope.menuStatus
  }
});
