/*global angular, document, console*/
angular.module('picbit').controller('MainController', ['$scope', 'RequestLanguage', function ($scope, RequestLanguage) {

  'use strict';

  $scope.languageRequest = function(file){
    RequestLanguage.language(file).success(function (data){
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
    });
  };
  $scope.languageRequest('es_es.json');
  
}]);
