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
		var generateThumbnail = function(element) {
			var canvasHeight = 100;
			var canvas = document.createElement('canvas');

			var ratio = canvasHeight / element.height;
			var canvasWidth = element.width * ratio;
			canvas.width = canvasWidth;
			canvas.height = canvasHeight;
			var context = canvas.getContext('2d');
			context.drawImage(element, 0, 0, canvasWidth, canvasHeight);

			var dataURL = canvas.toDataURL();
			//var thumb = dataURItoBlob(dataURL);
			return dataURL;
		};
		if (event.files && event.files[0].type.indexOf('image') !== -1){
			$scope._uploadFile = event.files[0];
			var reader = new FileReader();
			reader.onload = function (){
				var image = new Image();
				image.onload = function(){
					$scope._uploadFile = generateThumbnail(image);
					$('#userPicture')
					.attr('src', $scope._uploadFile);
				};
				image.src = reader.result;
			};
			reader.readAsDataURL(event.files[0]);
		}
	};
	// Envia los datos del usuario al servidor
	$scope.submitForm = function(){
		$('html').css('cursor','wait');
		var values = '';
		var $inputs = $('#userInformation input');
		var changes = false;
		for (var i =0;i<$inputs.length;i++){
			var $target = $($inputs[i]);
			if (i>0) {
				values+='&';
			}
			if ($target.attr('data-field') !== 'image'){
				values += $target.attr('data-field') + '=' + $target.val();

				if ($scope.user[$target.attr('data-field') !== $target.val()]){
					changes = true;
				}
			}
		}
		if ($scope._uploadFile){
			var thumbnail = $scope._uploadFile.replace(/data:image\/[^;]*;base64,/,'');
			$backend.uploadImage(thumbnail, function(response){
				values += '&image=' + response.data.link;
				$backend.updateProfile(values, $scope.user.user_id).then(function(){
					$scope.showToastr('info','Perfil actualizado');
					$('html').css('cursor','');
				}, function(){
					$('html').css('cursor','');
				});
			});
		} else if (changes) {
			$backend.updateProfile(values, $scope.user.user_id).then(function(){
				$scope.showToastr('info','Perfil actualizado');
				$('html').css('cursor','');
			}, function(){
				$('html').css('cursor','');
			});
		}
	};

	// Comprueba si ya esta registrado un token de una determinada red socialNetwork
	// Valida las clases.
	$scope.existToken = function(socialNetwork){
		return $scope.user && $scope.user.tokens[socialNetwork];
	};
	function loginCallback(e){
		//falta registralo
		$scope.$apply(function(){
			var socialNetwork = e.detail.redSocial;
			var token = e.detail.token;
			var token_id = e.detail.token_id || undefined;
			$rootScope.user = $rootScope.user || {tokens:{}};
			$rootScope.user.tokens[socialNetwork] = token;

			var registerTokenError = function(){
				$scope.showToastr('error',$scope.language.add_token_error);
				$rootScope.user.tokens[socialNetwork] = '';
			};

			switch(socialNetwork) {
				case 'googleplus':
					var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + token;
					$http.get(uri).success(function (responseData) {
						token_id = responseData.id;
					});
					break;
				case 'twitter':
					uri = $backend.endpoint + '/api/oauth/twitter/authorization/' + e.detail.oauth_verifier;
					$http.get(uri).success(function (responseData) {
						token_id = responseData.token_id;
					});
					break;
				default:
					break;
				}
				$backend.setNewNetwork(token, token_id, socialNetwork).error(registerTokenError);
			});
		}
		(function(){
			$('#socialNetwork google-login').bind('google-logged', loginCallback);
			$('#socialNetwork github-login').bind('github-logged', loginCallback);
			$('#socialNetwork instagram-login').bind('instagram-logged', loginCallback);
			$('#socialNetwork twitter-login').bind('twitter-logged', loginCallback);
			$('#socialNetwork login-facebook').bind('facebook-logged', loginCallback);
		})();
	}]);
