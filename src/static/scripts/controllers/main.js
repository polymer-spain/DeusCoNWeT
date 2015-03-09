'use strict';

/**
 * @ngdoc function
<<<<<<< HEAD
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */

angular.module('PolymerBricks')
.controller('MainCtrl', function ($scope,$location,$timeout) {


	$scope.buscar=false;
	$scope.changeView = function(view){
		if (view === 'profile/'){
			view=view + $scope.user.id.toString();
		}
		$location.path(view); // path not hash
	};
	$scope.logueado=false;
	$scope.profile = 'hola';
	$scope.user = $scope.user || [];
	$scope.init = function (){
		/*google.appengine.api.polymerBricks.getAllComponentsLimit('asc','name',3);*/
	};
	
	$scope.showOn = function () {
		 $timeout(function() {
    			document.querySelector('#search').focus();
			 		$scope.changeView('search');
        });
	};
	$scope.showOff = function (e) {
		if (e.target.value === '') {
				$scope.buscar=false;	
		}
	};
});
