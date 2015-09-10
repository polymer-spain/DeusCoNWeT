/*global angular*/
angular.module("picbit").controller("SelectidController", ["$scope", "$backend", "$rootScope", "$cookies", function ($scope, $backend, $rootScope, $cookies) {
  "use strict";
  $scope.userIdError = false;
  $scope.sendUsername = function (event, userId) {
    if ((event.type === "click" || (event.type === "keyup" && event.which === 13)) && userId) {
      $backend.getUser(userId).then(function(){
        $scope.userIdError = true;
      }, function() {
        $backend.sendData($rootScope.register.token, $rootScope.register.tokenId, userId, $rootScope.register.redSocial)
          .then(function() {
          $scope.userIdError = false;
          $rootScope.register = undefined;
          $scope.logOutButton();
          /*TODO mandar al tutorial de bienvenida, y almacenar los datos en $rootScope.user*/
          $scope.changeView("/user/" + userId);
        });
      });
    }
  };
}]);
