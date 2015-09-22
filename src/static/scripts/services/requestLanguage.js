angular.module("picbit").factory('RequestLanguage', ['$http', function($http) {
  return {
    language: function(param) {
      return $http.get('../../language/'+param)
        .success(function(data) {
        return data;
      })
        .error(function(err) {
        return err;
      });
    }
  }
}])
