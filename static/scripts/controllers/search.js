'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the pruebaApp
 */

angular.module('PolymerBricks')
.controller('SearchCtrl', function ($scope) {

	$scope.orderBy='asc';
	$scope.sortBy='name';
	$scope.webComponents = $scope.$parent.webComponents;

	$scope.setSort = function (sortBy) {
		$scope.sortBy=sortBy;
		google.appengine.api.polymerBricks.getAllComponents($scope.orderBy,$scope.sortBy);
	};

	$scope.setOrder = function () {
		if ($scope.orderBy ==='des'){
			$scope.orderBy = 'asc';
		} else {
			$scope.orderBy = 'des';
		}
	};

	$scope.changeList = function (sortBy) {
		$scope.setOrder();
		$scope.setSort(sortBy);
	};
	$scope.init = function (){
		if (apisToLoad === 0){
			google.appengine.api.polymerBricks.getAllComponents($scope.orderBy,$scope.sortBy);
		}else {}
	};

	$scope.respuesta = '';
	$scope.open = function () {
		var validInput = document.getElementById('inputC');

		if (validInput.validity.valid && validInput.inputValue!==null) {

			google.appengine.api.polymerBricks.uploadComponent(validInput.inputValue);
		}
	};
});
