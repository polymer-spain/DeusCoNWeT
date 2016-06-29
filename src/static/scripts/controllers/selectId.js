/*global angular, document*/
angular.module("picbit").controller("SelectidController", ["$scope", "$backend", "$rootScope", "$location",function ($scope, $backend, $rootScope, $location) {
  "use strict";
  $scope.showSendButton = false;

  /* Check if the username selected is already used. If not send it to DB*/
  $scope.sendUsername = function (event) {
    var element = document.querySelector("#username_input");
    var userId = element.value;
    if (!element.validate()) {
      $scope.errorMessage = $scope.language.select_id.invalid_username;
      element.invalid = true;
    } else if ((event.type === "click" || (event.type === "keyup" && event.which === 13)) && userId) {
      $backend.getUser(userId)
        .then(function(){
        element.invalid = true;
        $scope.errorMessage = $scope.language.select_id.userIdError;
      }, function() {
        $backend.signup($rootScope.register.token, $rootScope.register.tokenId, userId, $rootScope.register.redSocial, $rootScope.register.oauthVerifier)
          .then(function() {
          element.invalid = false;
          $rootScope.register = undefined;
          /*TODO mandar al tutorial de bienvenida, y almacenar los datos en $rootScope.user*/
          $location.path("/user/" + userId + '/profile');
        });
      });
    } else {
      $scope.errorMessage = "";
      element.invalid = false;
    }
  };
  
  /* Clear the input camp*/
  $scope.clearInput = function () {
    document.querySelector('#username_input').value = "";
  };
  
  /* Show button only when the input isn't void */
  document.querySelector("paper-input").addEventListener("bind-value-changed", function(event) {
      $scope.showSendButton = event.detail.value !== "" ? true : false;
  });
}]);
