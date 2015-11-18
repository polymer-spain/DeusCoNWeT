angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope', function ($scope, $timeout, $rootScope) {
  'use strict';

  /* Network infomation */
  $scope.toggleHelp = false;
  $scope.twitterData = {};
  $scope.githubData = {};
  $scope.instagramData = {};
  $scope.facebookData = {};
  
  $scope.instagramData.token = '2062815740.34af286.169a9c42e1404ae58591d066c00cb979';
  $scope.twitterData.token = '3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf';
  $scope.githubData.username = 'mortega5';
  $scope.facebookData.token = $rootScope.user.tokens.facebook;

  $scope.listComponents = [
    {
      name: 'twitter-timeline',
      attributes: {
        'access-token': $scope.twitterData.token,
        'secret-token': 'OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock',
        'consumer-key': 'J4bjMZmJ6hh7r0wlG9H90cgEe',
        'consumer-secret': '8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf',
        'endpoint': $scope.domain + '/api/aux/twitterTimeline',
        'language': '{{idioma}}',
        'count': 200,
        'component_base': 'bower_components/twitter-timeline/static/'

      }
    },
    {
      name: 'github-events',
      attributes: {
        username: $scope.githubData.username,
        token: $scope.githubData.token || '',
        mostrar: '10',
        language: '{{idioma}}',
        component_directory: 'bower_components/github-events/'
      }
    },
    {
      name: 'instagram-timeline',
      attributes: {
        'access-token': $scope.instagramData.token,
        endpoint: $scope.domain + '/api/aux/instagramTimeline',
        language: '{{idioma}}',
        component_directory: 'bower_components/instagram-timeline/static/'
      }
    },
    {
      name: 'facebook-wall',
      attributes: {
        language: '{{idioma}}',
        component_directory: 'bower_components/facebook-wall/',
        'access_token': $scope.facebookData.token
      }
    }
  ];
  $scope.listComponentAdded = []; // added on dragdrop.js
  $scope.modifySelected = $scope.modifySelected || '';
  /* Authentication */

  $scope.menuStatus = false;
  $scope.sort = [false, false, false];
  $scope.showElement = false;
  $scope.listaOpciones = [false, false, false];

  $scope.showMenu = function () {
    if (!$scope.menuStatus) {
      document.querySelector('#menu-icon').icon = 'arrow-forward';
      $scope.menuStatus = true;

      $timeout(function () {
        $scope.showElement = true;
      }, 350);
    } else {
      document.querySelector('#menu-icon').icon = 'arrow-back';
      $scope.menuStatus = false;
      $scope.showElement = false;
      $scope.selected = '';
      $scope.showSingle = '';
      $scope.listaOpciones = [false, false, false];

      // Develop has commented them
      document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
      document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
      document.querySelector('#arrowModify').icon = 'arrow-drop-down';


    }
  };

  $scope.ocultar = function (event) {
    $scope.listaOpciones = [false, false, false];
    switch (event) {
      case 'add':
        document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
        document.querySelector('#arrowModify').icon = 'arrow-drop-down';
        break;
      case 'delete':
        document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
        document.querySelector('#arrowModify').icon = 'arrow-drop-down';
        break;
      case 'modify':
        document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
        document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
    }
  };
  $scope.setList = function (event) {
    switch(event){
      case 'add':
        $scope.listaOpciones = [!$scope.listaOpciones[0], false, false];
        if (!$scope.listaOpciones[0]) {
          document.querySelector('#arrowAdd').icon = 'arrow-drop-up';
          document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
          document.querySelector('#arrowModify').icon = 'arrow-drop-down';
        }
        else {
          document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
        }
        break;
      case 'delete':
        $scope.listaOpciones = [false, !$scope.listaOpciones[1], false];
        if (!$scope.listaOpciones[1]){
          document.querySelector('#arrowDelete').icon = 'arrow-drop-up';
          document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
          document.querySelector('#arrowModify').icon = 'arrow-drop-down';
        }
        else {
          document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
        }
        break;
      case 'modify':
        $scope.listaOpciones = [false, false, !$scope.listaOpciones[2]];
        if (!$scope.listaOpciones[2]){
          document.querySelector('#arrowModify').icon = 'arrow-drop-up';
          document.querySelector('#arrowAdd').icon = 'arrow-drop-down';
          document.querySelector('#arrowDelete').icon = 'arrow-drop-down';
        }
        else {
          document.querySelector('#arrowModify').icon = 'arrow-drop-down';
        }
        break;
    }
  };

  $scope.showlist = function (event) {
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

  $scope.isSelected = function (event) {
    return $scope.selected === event && event !== undefined;
  };

  $scope.setSelected = function (event) {
    if ($scope.selected === event){
      $scope.selected = '';
      $scope.showSingle = '';
      if ($scope.showlist(event)) {
        $scope.setList(event);
      }
    }
    else {
      $scope.selected = event;
      $timeout(function(){
        $scope.showSingle = event;
      }, 350);
    }
  };

  $scope.isMenuHidden = function(event) {
    return !($scope.menuStatus || $scope.isSelected(event));
  };

  $scope.setSort = function(event) {
    switch(event){
      case 'add':
        $scope.sort = [!$scope.sort[0], false, false];
        break;
      case 'delete':
        $scope.sort = [false, !$scope.sort[1], false];
        break;
      case 'modify':
        $scope.sort = [false, false, !$scope.sort[2]];
        break;
    }
  };

  $scope.setModifySelected = function(elementName) {
    $scope.modifySelected = $scope.modifySelected !== elementName ? elementName : '';
  };

  $scope.isModifySelected = function(elementName) {
    return elementName === $scope.modifySelected;
  };
  
  $scope.deleteTimeline = function(elementName) {
    angular.element(document.querySelector('#container')).find(elementName).remove();
    var index = $scope.listComponentAdded.indexOf(elementName);
    $scope.listComponentAdded.splice(index, 1);
  };

  $scope.showToggleHelp = function (e){
    var element = e.target;
    var id = element.getAttribute('data-dialog') || element.parentElement.getAttribute('data-dialog');
    var dialog = document.getElementById(id);
    if (dialog) {
      dialog.open();
    }
  };
}]);
