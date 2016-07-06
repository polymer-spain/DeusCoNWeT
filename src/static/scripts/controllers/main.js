/*global angular, document, console*/
angular.module('picbit').controller('MainController', ['$scope', 'RequestLanguage', '$location', '$cookies', '$backend', '$http', '$rootScope', function ($scope, RequestLanguage, $location, $cookies, $backend, $http, $rScope) {

	'use strict';
	if ($location.host() === "localhost"){
		$scope.domain = "http://" + $location.host() + ":" + $location.port();
	}else {
		$scope.domain = 'https://' + $location.host(); // Dominio bajo el que ejecutamos
	}

	// Language control
	$scope.idioma = $cookies.get('language') || window.navigator.language.toLowerCase().split('-')[0];
	$scope.setLanguage = function(lang){
		var file = lang + "_"+ lang + ".json";
		$scope.idioma = lang;
		RequestLanguage.language(file).success(function (data){
			$scope.language = data;
			$scope.languageSelected = data.lang[$scope.idioma];
		});
	};
	$scope.setLanguage($scope.idioma);

	$scope.logout = function (parent) {
		$('html').css('cursor','wait');
		$backend.logout().then(function() {
			$('html').css('cursor','');
			if (parent){
				document.getElementById(parent).close();
			}
			$location.path('/');
		}, function(){
			$('html').css('cursor','');
			$location.path('/');
			//console.error('Error ' + response.status + ': Fallo al intentar realizar un logout del usurio ' + $rScope.user.name);
		});
	};

	// Login callback function
	$scope.loginProcess = function(userData){
		$rScope.token = userData.token;
		// buscamos si existe el usuario
		$backend.getUserId(userData.userId, userData.redSocial)
		.then(function (responseUserId) {
			/* Pedimos la información del usuario y la almacenamos para poder acceder a sus datos */
			var user = responseUserId.data;
			// actualizamos los datos del usuario en el servidor
			$backend.sendData(userData.token, userData.userId, responseUserId.data.user_id, userData.redSocial, userData.oauth_verifier)
			.then(function() {
				// Si todo va bien, le mandamos a su dashboard
				$location.path('/user/' + user.user_id);
			}, function(responseLogin) {
				console.error('Error ' + responseLogin.status + ': al intentar mandar los datos de login');
			});
		}, function(){// Si response con error, significa que no existe el usuario
			$rScope.register = {token: userData.token, redSocial: userData.redSocial, tokenId: userData.userId, oauthVerifier: userData.oauth_verifier};
			$location.path('/selectId');
		});
	};
	
	$scope.goto = function(view){
		if (view.indexOf(':user') > -1){
			view = view.replace(/:user/g,$rScope.user.user_id);
		}
		$location.path(view); // path not hash

	};
	var loginCallback = function (e) {
		//$scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
		$('#login-popup').modal('hide');

		var socialNetwork = e.detail.redSocial;
		var uri;
		switch(socialNetwork) {
			case 'googleplus':
			uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + e.detail.token;
			$http.get(uri).success(function (responseData) {
				e.detail.userId = responseData.id;
				$scope.loginProcess(e.detail);
			});
			break;
			case 'twitter':
			uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
			$http.get(uri).success(function (responseData) {
				e.detail.userId = responseData.token_id;
				$scope.loginProcess(e.detail);
			}).error(function() {
				console.log('Problemas al intentar obtener el token_id de un usuario' );
			});
			break;
			default:
			$scope.loginProcess(e.detail);
			break;
		}
	};

	// Binding login callback
	(function(){
		$('#login-popup google-login')[0].addEventListener('google-logged', loginCallback);
		$('#login-popup twitter-login')[0].addEventListener('twitter-logged', loginCallback);
		$('#login-popup login-facebook')[0].addEventListener('facebook-logged', loginCallback);
	})();

	// avoid language errors
	$scope.$watch('language.delete', function(newValue) {
		$('.icon-delete > span').html(newValue);
	});

}]);// end angular.module
