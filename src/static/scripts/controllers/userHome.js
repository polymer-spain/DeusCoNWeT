angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope', function ($scope, $timeout, $rootScope) {
	'use strict';
	$scope.listComponentAdded = [];
	$scope.itemDescription = "";
	$scope.selectListButton = function(e){
		e.stopPropagation();
		var $target = $(e.currentTarget);
		if ($target.hasClass('active')){
			$target.removeClass('active');
		} else {
			$target.parent().children().removeClass('active')
			$target.addClass('active');
		}

	};

	$scope.catalogList = [
		{name:'twitter-timeline',
		 rate:5,
		 img:'images/components/twitter-logo.png',
		 description:'Muestra el timeline de twitter texto muy largo para provocar un overflow y ver que ocurre en la imagen que representa',
		 hasToken: $rootScope.user && $rootScope.user.tokens['twitter']  ? true:false,
		 attributes: {
			 "access-token": $rootScope.user ? $rootScope.user.tokens.twitter : "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
			 "secret-token": "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
			 "consumer-key": "J4bjMZmJ6hh7r0wlG9H90cgEe",
			 "consumer-secret": "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
			 endpoint: $scope.domain + "/api/aux/twitterTimeline",
			 component_base: "bower_components/twitter-timeline/static/",
			 language: "{{idioma}}",
			 count: "200"
		 }
		},
		{name:'github-events',
		 rate:4,
		 img:'images/components/github-icon.png',
		 hasToken:$rootScope.user && $rootScope.user.tokens['github'] ? true:false,
		 description:'Muestra los eventos sucedidos en github',
		 attributes: {
			 username: "mortega5",
			 token: $rootScope.user ? $rootScope.user.tokens.github:'',
			 mostrar: "10",
			 language: "{{idioma}}",
			 component_directory: 'bower_components/github-events/'
		 }
		},
		{
			name:'instagram-timeline',
			rate:1,
			hasToken:$rootScope.user && $rootScope.user.tokens['instagram'] ? true:false,
			img:'images/components/instagram-icon.png',
			description:'Muestra las fotos de Instagram',
			accessToken: "TODO",
			endpoint: "TODO" + "/api/aux/instagramTimeline",
			language: "{{idioma}}"

		},
		{
			name: 'googleplus-timeline',
			rate:4,
			hasToken:$rootScope.user && $rootScope.user.tokens['googleplus'] ? true:false,
			img:'images/components/google-icon.svg',
			description:'Muestra las entradas en google+',
			attributes: {
				'token': $rootScope.user ? $rootScope.user.tokens.google:'ya29.CjMHAzmtu3cGQaJ77v0nq0xoJ9F_VTNkJWx-mUmQQlyDU4nn8KlTBO3mWyqFw32XTAQofVc',
				'language':'{{idioma}}'
			}
		},
		{
			name: 'facebook-wall',
			rate: 3,
			hasToken:$rootScope.user && $rootScope.user.tokens['facebook'] ? true:false,
			img: 'images/components/facebook-icon.png',
			attributes: {
				language: '{{idioma}}',
				component_directory: 'bower_components/facebook-wall/',
				access_token: $rootScope.user ? $rootScope.user.tokens.facebook: 'NO IMPLEMENTED',
			}
		}
	];
	$scope.removeStarFilter = function(){
		$scope.starFilter = undefined;
	}
	$scope.removeTextFilter = function(){
		$scope.textFilter = '';
	}
	$scope.activeDelCmpList = function(){
		var $list = $('.component-list');
		if (!$list.hasClass('active')){
			$list.addClass('active');
		} else if($scope.showList == $scope.addedList) {
			$list.removeClass('active');
		}
	}
	$scope.removeElement = function(id){
		var finded = false;

		for (var i = 0;i< $scope.listComponentAdded.length && !finded;i++){
			if ($scope.listComponentAdded[i].name == id){
				finded = true;
				$scope.listComponentAdded.splice(i,1);

			}
		}
	}
	$scope.blurList = function(e){
		if ($scope.itemDescription = $scope.listComponentAdded){
			// del activated
			var index = $(e.currentTarget).attr('data-index');
			var id = $scope.listComponentAdded.splice(index,1)[0];
			$scope.showList = $scope.listComponentAdded;
			var element = '[id-element="' + id.name + '"]';
			$(element)[0].setAttribute('disabled',false);
			$(id.name).parent().remove();
		}
	}
	$('#userHome').click(function(event){
		if (!event.target.hasAttribute('data-button') && !event.target.hasAttribute('data-list')){
			$('.component-list').removeClass('active');
			$('.menu-buttons').children().removeClass('active');
		}
	})

	$(document).on('keydown', function(e){
		e.stopPropagation();
		if (e.keyCode === 27 && $('#login-modal').is(':visible')){
			$('#login-modal').modal('toggle');	
		} else if (e.keyCode === 27 && $('#store-modal').is(':visible')){
			$('#store-modal').modal('toggle');	
		}
	})
	$('#store-modal').on('hidden.bs.modal',function(){
		if ($('#login-modal').is(':visible')){
			$('#login-modal').modal('toggle');
		}
	})
	$scope.toggleCatalog = function(){
		if ($('#login-modal').is(':visible')){
			$('#login-modal').modal('toggle');
		}
		$('#store-modal').modal('toggle');
	}
	
	$scope.closeModal = function(selector){
		$(selector).modal('toggle');
	}
	$scope.login = function(name, e){
		$scope.loginSelected = name.split('-')[0];
		$('#login-modal').modal('toggle');
	};
}]);
