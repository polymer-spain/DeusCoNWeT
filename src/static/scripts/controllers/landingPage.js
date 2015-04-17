

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

  $scope.selected = 1;

  $scope.cambiarAnchor = function(section){
    $location.hash(section);
    $anchorScroll();    
  };

  $scope.setStyle = function(el,el2){
    document.querySelector(el).removeAttribute('selected')
    document.querySelector(el2).setAttribute('selected',true);

  };

  $scope.wheel = function(e) {
    e.preventDefault();
    document.onmousewheel = '';
    var scrolled;
    e.wheelDelta<0 ? scrolled=1 : scrolled=-1;
    /* Section 1*/
    if ($scope.selected===1 && e.wheelDelta<0) {
      $scope.selected +=scrolled;
      $scope.cambiarAnchor('section2'); 
      $scope.setStyle('#disc1','#disc2');
      /* Section 2*/
    } else if ($scope.selected === 2) {
      $scope.selected +=scrolled
      $scope.cambiarAnchor('section'+$scope.selected); 
      $scope.setStyle('#disc2','#disc'+$scope.selected);
      /* Section 3*/
    }else if ($scope.selected === 3 && e.wheelDelta>0) {
      $scope.selected += scrolled;
      $scope.cambiarAnchor('section2');
      $scope.setStyle('#disc3','#disc2');
    };
    setTimeout(function(){
      document.onmousewheel = $scope.wheel;
    },500);
  };
  document.onmousewheel = $scope.wheel;
  if ($location.path === '/')
    $scope.cambiarAnchor('section1');

  $scope.setSelected = function(sel){
    $scope.setStyle('#disc'+$scope.selected,'#disc'+sel);
    $scope.selected = sel;
    $scope.cambiarAnchor("section"+sel);
  };

  $scope.isSelected = function(sel) {
    return $scope.selected === sel; 
  }
});