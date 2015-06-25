'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:AboutController
 * @description
 * # AboutController
 * Controller of the pruebaApp
 */

angular.module('picbit')
.controller('SearchCtrl', function ($scope) {

	$scope.orderBy='asc';
	$scope.sortBy='name';
	$scope.webComponents = $scope.$parent.webComponents;

	$scope.setSort = function (sortBy) {
		$scope.sortBy=sortBy;
		getAllComponent($scope.orderBy,$scope.sortBy);
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
		var callback = function(response) {

			$scope.$apply(function() {
				$scope.webComponents = response;
			}
						 )};
		getAllComponents($scope.orderBy,$scope.sortBy,callback);
	};

	$scope.respuesta = '';
	$scope.open = function () {
		var validInput = document.getElementById('inputC');

		if (validInput.validity.valid && validInput.inputValue!==null) {

			google.appengine.api.picbit.uploadComponent(validInput.inputValue);
		}
	};
});
