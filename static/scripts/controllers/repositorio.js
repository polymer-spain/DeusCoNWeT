'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # ComponentCtrl
 * Controller of the pruebaApp
 */

angular.module('PolymerBricks')
.controller('ComponentCtrl', function($scope, $routeParams,$timeout) {
	$scope.componentID = $routeParams.componentID;
	$scope.component = $scope.component || [];

	$scope.userId = function() {
		return $scope.$parent.user.id;
	};
	$scope.mostrarValorado = false;

	$scope.init = function ()
	{
		if (apisToLoad === 0){
			google.appengine.api.polymerBricks.getComponent($routeParams.componentID,$scope.userId());
		}
	};
	if ($scope.$parent.user.id !== undefined) {
		document.querySelector('#rate').setAttribute('readOnly',false);	
	} else {
		document.querySelector('#rate').setAttribute('readOnly',true);	
	}

	$scope.valorar = function () {
		$scope.valorado = document.querySelector('#rate').value;

		if ($scope.userId()) {
			google.appengine.api.polymerBricks.rateComponent($scope.component.componentId,$scope.valorado,$scope.userId());
			$scope.mostrarValorado=true;
			$timeout(function () {
				$scope.mostrarValorado = false;
			},3000);

		} else {

			document.querySelector('#toast').show();
		}

	};
});