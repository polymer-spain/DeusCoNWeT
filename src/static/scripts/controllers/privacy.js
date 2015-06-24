'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainController
 * @description
 * # ComponentCtrl
 * Controller of the pruebaApp
 */

angular.module('picbit')
  .controller('PrivacyController', function($scope, $routeParams,$timeout) {
  $scope.mailTo = function () {

    var link = "mailto:deus@conwet.com"
    + "?cc=deus@conwet.com"
    + "&subject=" + "beta"
    + "&body=" +document.querySelector('#mensaje').value;
    window.location.href = link;
  }
});