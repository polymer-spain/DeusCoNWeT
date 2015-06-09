'use strict';

/**
 * @ngdoc function
 * @name polymerGeneratedAppApp.controller:SandboxCtrl
 * @description
 * # SandboxCtrl
 * Controller of the polymerGeneratedAppApp
 */

angular.module('picbit').controller('UserHomeController', function ($scope,$timeout) {

  $scope.list = [
    {name: 'John'},
    {name: 'Jessie'},
    {name: 'Johanna'},
    {name: 'Joy'},
    {name: 'Mary'},
    {name: 'Peter'},
    {name: 'Sebastian'},
    {name: 'Erika'},
    {name: 'Patrick'},
    {name: 'Samantha'}
  ];
  
  /* Network infomation */
  $scope.twitter = {};
  $scope.github = {};
  $scope.twitter.token = '3072043347-hbcrkzLJfVzTg7BTjgzkKqZx3bbzpYb04IO573x';
  $scope.github.username = 'mortega5'
  
  /* Authentication */
  
  $scope.menuStatus = false;
  $scope.showElement = false;
  $scope.listaOpciones = ['false','false','false'];
  $scope.showMenu = function(){

    if (!$scope.menuStatus){
      document.querySelector('#menu-icon').icon='arrow-forward';
      $scope.menuStatus = true;

      $timeout(function(){
        $scope.showElement = true;
      },350);
    }
    else {
      document.querySelector('#menu-icon').icon='arrow-back';  
      $scope.menuStatus = false;
      $scope.showElement = false;
      $scope.selected = '';
      $scope.showSingle='';
      $scope.listaOpciones = ['false','false','false'];
    }
  };

  $scope.setList = function(event) {
    switch(event){
      case 'add':
        $scope.listaOpciones=[!$scope.listaOpciones[0],'false','false'];
        if (!$scope.listaOpciones[0])
          document.querySelector('#arrowAdd').icon = "arrow-drop-up"
          else
            document.querySelector('#arrowAdd').icon = "arrow-drop-down"
            break;
      case 'delete':
        $scope.listaOpciones=['false',!$scope.listaOpciones[1],'false'];
        if (!$scope.listaOpciones[1])
          document.querySelector('#arrowDelete').icon = "arrow-drop-up"
          else
            document.querySelector('#arrowDelete').icon = "arrow-drop-down"
            break;
      case 'modify':
        $scope.listaOpciones=['false','false',!$scope.listaOpciones[2]];
        if (!$scope.listaOpciones[2])
          document.querySelector('#arrowModify').icon = "arrow-drop-up"
          else
            document.querySelector('#arrowModify').icon = "arrow-drop-down"

            break;
    }
  }
  $scope.hidelist = function(event) {
    switch(event){
      case 'add':
        return $scope.listaOpciones[0];
      case 'delete':
        return $scope.listaOpciones[1];
      case 'modify':
        return $scope.listaOpciones[2];
      default:
        return false;
    }
  };
  $scope.isSelected = function(event) {
    return $scope.selected === event && event != undefined
  }
  $scope.setSelected = function(event) {
    if ($scope.selected === event){
      $scope.selected='';
      $scope.showSingle='';
      if (!$scope.hidelist(event))
        $scope.setList(event);
    }
    else {
      $scope.selected = event;
      $timeout(function(){
        $scope.showSingle=event;
      },350);
    }

  };

  $scope.isMenuHidden = function(event) {
    return !($scope.menuStatus | $scope.isSelected(event))
  }
});
