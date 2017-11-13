angular.module("picbit").controller("PermissionCtrl", ['$scope', '$rootScope', function ($scope, $rootScope) {

  $scope.showLoginButton = function (socialNetwork) {
    return $scope.loginSelected == socialNetwork
  }

  $scope.getScopes = function (socialNetwork) {
    var scopes = "";
    if (socialNetwork) {
      var network_scopes = $rootScope.user.scopes[socialNetwork];
      var version = $scope.getVersion(socialNetwork);
      if (version) {
        scopes = version === "security" ? network_scopes.security : network_scopes.default;
      }
    }
    return scopes;
  }

  $scope.getVersion = function (socialNetwork) {
    var version;
    if (socialNetwork) {
      var index = $scope.catalogList.findIndex(function (component) {
        return component.social_network === socialNetwork;
      });
      if (index > -1) {
        version = $scope.catalogList[index].version;
      }
    }
    return version;
  }
}]);