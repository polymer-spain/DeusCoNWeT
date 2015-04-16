

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */
angular.module('PolymerBricks')
  .controller('landingCtrl', function ($scope,$timeout,$location,$anchorScroll) {
  'use strict';

  if ($location.hash() === 'section1'){
    $scope.selected = 1;
  } else if ($location.hash() === 'section2'){
    $scope.selected = 2;
  }
  else if ($location.hash() === 'section3'){
    $scope.selected = 3;
  } else {
    $scope.selected = 1;
  }

  $scope.cambiarAnchor = function(section){
    $location.hash(section);
    $anchorScroll();    
  };

  $scope.setStyle = function(el,el2){
    document.querySelector(el).removeAttribute('selected')
    document.querySelector(el2).setAttribute('selected',true);

  };

  $scope.wheel = function(e) {
    $scope.$apply(function () {
      e.preventDefault();
      document.onmousewheel = '';
      var scrolled;
      e.wheelDelta<0 ? scrolled=1 : scrolled=-1;
      /* Section 1*/
      if ($scope.selected===1 && e.wheelDelta<0) {
        $scope.selected +=scrolled;
        $scope.cambiarAnchor('section2'); 
        /* Section 2*/
      } else if ($scope.selected === 2) {
        $scope.selected +=scrolled

        $scope.cambiarAnchor('section'+$scope.selected); 

        /* Section 3*/
      } else if ($scope.selected === 3 && e.wheelDelta>0) {
        $scope.selected += scrolled;
        $scope.cambiarAnchor('section2');
      };
      document.onmousewheel = $scope.wheel;
    });
  };

  document.onmousewheel = $scope.wheel;

  /*  $scope.setSelected = function(sel){
    $scope.setStyle('#disc'+$scope.selected,'#disc'+sel);
    $scope.selected = sel;
    $scope.cambiarAnchor("section"+sel);
  };*/

  $scope.isSelected = function(sel) {
    return $scope.selected === sel; 
  }
});