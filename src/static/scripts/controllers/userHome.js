angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope', function ($scope, $timeout, $rootScope) {
  'use strict';
  $scope.selectedList = ['test1','test2'];
  $scope.componentList = ['test1','test2','test3'];
  $scope.addedList = [];
  
  $scope.selectListButton = function(e){
    var $target = $(e.currentTarget);
    $target.parent().children().removeClass('active')
    $target.addClass('active');
  };

  $scope.activeAddCmpList = function(){
    var $list = $('.component-list');
    if (!$list.hasClass('active')){
      $list.addClass('active');
    }
    $scope.selectedList = $scope.componentList;
  };

  $scope.activeDelCmpList = function(){
    var $list = $('.component-list');
    if (!$list.hasClass('active')){
      $list.addClass('active');
    }
    $scope.selectedList = $scope.addedList;
  }
  
  $('#userHome').click(function(){
    console.log('TODO ocultar la lista');
  })

}]);
