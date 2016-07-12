/*global angular*/
angular.module("picbit")
.controller("UserProfileController", ["$scope", "$rootScope","$backend","$http",
function ($scope, $rootScope, $backend, $http) {
	"use strict";

	// Cambia la seleccion entre las difernetes pestañas
	$scope.selectSection = function(e){
		var $target = $(e.currentTarget);
		var sectionTarget = $target.attr('data-target');

		$('.information').children().removeClass('active');
		$('.tabs').children().removeClass('active');

		$target.parent().addClass('active');
		$(sectionTarget).addClass('active');
	};

	// Permite cambiar la imagen de un usuario, basandose
	// en el input que ha dado
	$scope.changePicture = function(event){
		if (event.files && event.files[0].type.indexOf('image') !== -1){
			var reader = new FileReader();
			$backend.uploadImage(event.files[0]);
			reader.onload = function (e) {
				$('#userPicture')
				.attr('src', e.target.result);
			};
			reader.readAsDataURL(event.files[0]);
		}
	};


	// Envia los datos del usuario al servidor

	$scope.submitForm = function(){
		var values = {};
		var $inputs = $('#userInformation input');

		for (var i =0;i<$inputs.length;i++){
			var $target = $($inputs[i]);
			values[$target.attr('data-field')] = $target.val();
		}
		// TODO comprobar que se han cambiado datos respecto a los recibidos
		console.log('TODO send to server: ', values);
	};

	// Comprueba si ya esta registrado un token de una determinada red socialNetwork
	// Valida las clases.
	$scope.existToken = function(socialNetwork){
		return $scope.user && $scope.user.tokens[socialNetwork];
	};
	$scope.showToastr = function(type, message, time){
		toastr.options = {
			"closeButton": false,
			"debug": false,
			"newestOnTop": false,
			"progressBar": false,
			"positionClass": "toast-top-right",
			"preventDuplicates": false,
			"onclick": null,
			"showDuration": "300",
			"hideDuration": "1000",
			"timeOut": "5000",
			"extendedTimeOut": time || "5000",
			"showEasing": "swing",
			"hideEasing": "linear",
			"showMethod": "fadeIn",
			"hideMethod": "fadeOut"
		};
		toastr[type](message);
	};
	function loginCallback(e){
		//falta registralo
		$scope.$apply(function(){
			var socialNetwork = e.detail.redSocial;
			var token = e.detail.token;
			var registerTokenError = function(){
				$scope.showToastr('error',$scope.language.add_token_error);
				$rootScope.user.tokens[socialNetwork] = '';
				$scope.setToken(socialNetwork, '');
			};
			$rootScope.user = $rootScope.user || {tokens:{}};
			$rootScope.user.tokens[socialNetwork] = token;

			// switch(socialNetwork) {
			// 	case 'googleplus':
			// 	var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token;
			// 	$http.get(uri).success(function (responseData) {
			// 		$backend.addTokens(socialNetwork, responseData.id, token, $scope.user.user_id).error(registerTokenError);
			// 	});
			// 	break;
			// 	case 'twitter':
			// 	uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
			// 	$http.get(uri).success(function (responseData) {
			// 		e.detail.userId = responseData.token_id;
			// 		$backend.addTokens(socialNetwork, responseData.token_id, token,
			// 			$scope.user.user_id, e.detail.oauth_verifier).error(registerTokenError);
			// 		}).error(function() {
			// 			console.log('Problemas al intentar obtener el token_id de un usuario' );
			// 		});
			// 		break;
			// 		default:
			// 		$backend.addTokens(socialNetwork, '', token, $scope.user.user_id).error(registerTokenError);
			// 		break;
			// 	}
			});
		}
		(function(){
			$('#socialNetwork google-login')[0].addEventListener('google-logged', loginCallback);
			$('#socialNetwork github-login')[0].addEventListener('github-logged', loginCallback);
			$('#socialNetwork instagram-login')[0].addEventListener('instagram-logged', loginCallback);
			$('#socialNetwork twitter-login')[0].addEventListener('twitter-logged', loginCallback);
			$('#socialNetwork login-facebook')[0].addEventListener('facebook-logged', loginCallback);
		})();
	}]);
