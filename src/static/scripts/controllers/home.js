

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */
angular.module('PolymerBricks')
.controller('HomeCtrl', function ($scope,$http,$modal) {
	'use strict';
	/*
	if (navigator.userAgent.match('Firefox') !==null){
		console.log('Detecta firefox');
	};*/
	$scope.orderBy='asc';
	$scope.sortBy='name';
	$scope.webComponents = $scope.webComponents || [];
	if ((localStorage.getItem('components'))!=='undefined' && (localStorage.getItem('components'))!==null) {
		$scope.webComponents = JSON.parse(localStorage.getItem('components'));
	} else {
		$scope.webComponents = [];	
	}
	
	$scope.changeView = $scope.$parent.changeView;


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
	$scope.init = function ()
	{
		var callback = function(respunesta){
			console.log(respuesta);
		}
			getAllComponent($scope.orderBy,$scope.sortBy,callback);
	};

	$scope.respuesta = '';
	$scope.open = function () {
		var validInput = document.getElementById('input');


		if (validInput.validity.valid && validInput.value!=='') {
			google.appengine.api.polymerBricks.uploadComponent(validInput.value);
		}

	};

	$scope.loadModal = function (code) {
		var modalInstance = [];
		if (code === 201) {
			modalInstance = $modal.open({
				templateUrl: 'myModalContent.html',
				controller: 'ModalInstanceCtrl',
			});
		} else if (code === 404) {
			modalInstance = $modal.open({
				templateUrl: 'myModalContentError.html',
				controller: 'ModalInstanceCtrl',
			});
		} else {
				modalInstance = $modal.open({
				templateUrl: 'myModalContentRepetido.html',
				controller: 'ModalInstanceCtrl',
			});
		}
	};
	$scope.pulso = function (event) {
		var d = document.querySelector('#inputC');
		d.isInvalid = !event.target.validity.valid;
		if (event.keyCode===13 && event.target.validity.valid){
			$scope.open();
		}
	};

	$scope.changeZ = function (event,z) {

		event.currentTarget.setZ(z);
	};

});

angular.module('PolymerBricks').controller('ModalInstanceCtrl', function ($scope, $modalInstance) {
'use strict';
	$scope.ok = function () {
		$modalInstance.close();
		var validInput = document.getElementById('inputC');
		validInput.setAttribute('value','');
	};
});
