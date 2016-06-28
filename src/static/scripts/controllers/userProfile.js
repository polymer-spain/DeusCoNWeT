/*global angular*/
angular.module("picbit")
	.controller("UserProfileController", ["$scope", "$rootScope", function ($scope, $rootScope) {
		"use strict";

		$scope.selectSection = function(e){
			var $target = $(e.currentTarget);
			var sectionTarget = $target.attr('data-target');

			$('.information').children().removeClass('active');
			$('.tabs').children().removeClass('active');

			$target.parent().addClass('active');
			$(sectionTarget).addClass('active');
		}
		$scope.changePicture = function(event){
			if (event.files && event.files[0].type.indexOf('image') != -1){
				var reader = new FileReader();
				reader.onload = function (e) {
					$('#userPicture')
						.attr('src', e.target.result);
				};
				reader.readAsDataURL(event.files[0]);
			}
		}

		$scope.submitForm = function(){
			var values = {};
			var $inputs = $('#userInformation input');

			for (var i =0;i<$inputs.length;i++){
				var $target = $($inputs[i]);
				values[$target.attr('data-value')] = $target.val();
			}
			console.log('TODO send to server: ', values);
		}
		$scope.existToken = function(socialNetwork){
			return $scope.user && $scope.user.tokens[socialNetwork];
		}


		function loginCallback(e){
			//falta registralo
			$scope.$apply(function(){
				$rootScope.user = $rootScope.user || {tokens:{}}
				$rootScope.user.tokens[e.detail.redSocial] = e.detail.token;
				console.log('TODO add token to DB. Remove user initialisation');
			})
		}
		(function(){
			$('#socialNetwork google-login')[0].addEventListener('google-logged', loginCallback);
			$('#socialNetwork github-login')[0].addEventListener('github-logged', loginCallback);
			$('#socialNetwork instagram-login')[0].addEventListener('instagram-logged', loginCallback);
			$('#socialNetwork twitter-login')[0].addEventListener('twitter-logged', loginCallback);
			$('#socialNetwork login-facebook')[0].addEventListener('facebook-logged', loginCallback);
		})();
	}]);