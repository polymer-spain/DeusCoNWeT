/*global angular, document*/
angular.module("picbit").controller("SelectidController", ["$scope", "$backend", "$rootScope", function ($scope, $backend, $rootScope) {
  "use strict";
  $scope.userIdError = false;

  $scope.errorMessage = "";
  $scope.sendUsername = function (event, userId) {
    if (!document.querySelector("#username_input").validity.valid) {
      $scope.errorMessage = $scope.language.select_id.invalid_username;
      $scope.userIdError = true;
    } else if ((event.type === "click" || (event.type === "keyup" && event.which === 13)) && userId) {
      $backend.getUser(userId)
        .then(function(){
        $scope.userIdError = true;
        $scope.errorMessage = $scope.language.select_id.userIdError;
      }, function() {
        $backend.signup($rootScope.register.token, $rootScope.register.tokenId, userId, $rootScope.register.redSocial, $rootScope.register.oauthVerifier)
          .then(function() {
          $scope.userIdError = false;
          $rootScope.register = undefined;
          /*TODO mandar al tutorial de bienvenida, y almacenar los datos en $rootScope.user*/
          $scope.changeView("/user/" + userId);
        });
      });
    } else {
      $scope.errorMessage = "";
      $scope.userIdError = false;
    }
  };
}]);
