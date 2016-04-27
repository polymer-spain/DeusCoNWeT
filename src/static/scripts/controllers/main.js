/*global angular, document, console*/
angular.module('picbit').controller('MainController', ['$scope', 'RequestLanguage', '$location', '$cookies', function ($scope, RequestLanguage, $location, $cookies) {

  'use strict';

  $scope.domain = 'https://' + $location.host(); // Dominio bajo el que ejecutamos

  // Language control
  $scope.idioma = $cookies.get('language') || $window.navigator.language;
  $scope.languageRequest = function(lang){
    var file = lang + "_"+ lang + ".json";
    RequestLanguage.language(file).success(function (data){
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
    });
  };
  $scope.languageRequest($scope.idioma);

}]);
