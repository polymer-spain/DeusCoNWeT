/*global angular, document, console*/
angular.module('picbit').controller('MainController', ['$scope', 'RequestLanguage', '$location', '$cookies', function ($scope, RequestLanguage, $location, $cookies) {

  'use strict';

  $scope.domain = 'https://' + $location.host(); // Dominio bajo el que ejecutamos

  // Language control
  $scope.idioma = $cookies.get('language') || $window.navigator.language;
  $scope.setLanguage = function(lang){
    var file = lang + "_"+ lang + ".json";
    $scope.idioma = lang;
    RequestLanguage.language(file).success(function (data){
      $scope.language = data;
      $scope.languageSelected = data.lang[$scope.idioma];
    });
  };
  $scope.setLanguage($scope.idioma);

  
  // Login callback function
  var loginCallback = function(e){
    
  }
  // Binding login callback
  (function(){
    document.querySelector('body').addEventListener('google-logged', loginCallback);
    document.querySelector('body').addEventListener('linkedin-logged', loginCallback);
    document.querySelector('body').addEventListener('github-logged', loginCallback);
    document.querySelector('body').addEventListener('instagram-logged', loginCallback);
    document.querySelector('body').addEventListener('twitter-logged', loginCallback);
    document.querySelector('body').addEventListener('facebook-logged', loginCallback);
    document.querySelector('body').addEventListener('sof-logged', loginCallback);
  })();


}]);// end angular.module
