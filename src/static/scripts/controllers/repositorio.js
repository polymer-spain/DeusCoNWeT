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
		var callback = function(respuesta){

			$scope.$apply(function() {
				$scope.component = respuesta;
			});
		};
		$timeout(function() {
			getComponent($routeParams.componentID,$scope.userId(),callback);
		},1000);
	};

	if ($scope.$parent.user.id !== undefined) {
		document.querySelector('#rate').setAttribute('readOnly',false);	
	} 

	$scope.valorar = function () {
		$scope.valorado = document.querySelector('#rate').value;

		if ($scope.userId()) {
			var callback = function(){

			}
			rateComponent($scope.component.componentId,$scope.valorado,$scope.userId(),callback);
			$scope.mostrarValorado=true;
			$timeout(function () {
				$scope.mostrarValorado = false;
			},3000);
		} else {
			document.querySelector('#toast').show();
		}

	};
});