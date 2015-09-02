angular.module('picbit').controller('SelectidController',['$scope','$backend','$rootScope',function ($scope, $backend, $rootScope) {
  'use strict';
  $scope.sendUsername = function (event,user_id) {
    var callback, errorCallback;
    callback = function () {
      $scope.changeView('/profile/');
    };

    if ((event.type === "click" || (event.type === "keyup" && event.which === 13)) && user_id) {
      $backend.getUser(user_id)
        .then(function(){
      }, function() {
        $backend.sendData($rootScope.register.token,$rootScope.register.token_id,user_id,$rootScope.register.redSocial);
        $scope.logOutButton();

        $scope.changeView('/user/' + user_id);
      });

    }
  }
}]);