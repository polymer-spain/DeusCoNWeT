angular.module("picbit").controller("CatalogCtrl", ['$scope', '$rootScope',  function ($scope, $rootScope) {

  $scope.checkToken = function(item, index){
    // check if itrequires token 
    // if it's required, check if it exists
    return !item.social_network || ($rootScope.user.tokens[item.social_network] !== undefined && item.version !== "security") || $rootScope.user.renew[item.social_network];
  }

}]);
  
