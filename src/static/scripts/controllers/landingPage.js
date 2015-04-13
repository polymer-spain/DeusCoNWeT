

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */
angular.module('PolymerBricks')
  .controller('landingCtrl', function ($scope,$location,$anchorScroll) {
  'use strict';
  $scope.selected = 'section1';

  $scope.setSelected = function(sel){
    $scope.selected = sel;
    $scope.goto(sel);
  };

  $scope.goto = function(sel) {
    // set the location.hash to the id of
    // the element you wish to scroll to.
    $location.hash(sel);

    // call $anchorScroll()
    $anchorScroll();
  };

  $scope.isSelected = function(sel) {
    return $scope.selected === sel; 
  }
})
