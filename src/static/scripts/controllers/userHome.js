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
		{name:'twitter-timeline',rate:5, img:'http://www.coetail.com/seriously/files/2016/04/twitter-logo.png', description:'Muestra el timeline de twitter texto muy largo para provocar un overflow y ver que ocurre en la imagen que representa', attributes: {
			"access-token": "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
			"secret-token": "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
			"consumer-key": "J4bjMZmJ6hh7r0wlG9H90cgEe",
			"consumer-secret": "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
			endpoint: $scope.domain + "/api/aux/twitterTimeline",
			component_base: "bower_components/twitter-timeline/static/",
			language: "{{idioma}}",
			count: "200"
		}},
		{name:'github-events',rate:4, img:'https://wasin.io/wp-content/uploads/2015/05/showimage.png', description:'Muestra los eventos sucedidos en github',	attributes: {
			username: "mortega5",
			token: "" || "",
			mostrar: "10",
			language: "{{idioma}}",
			component_directory: 'bower_components/github-events/'
		}
		},
		{name:'instagram-timeline',rate:1, img:'http://www.seawolfkayak.com/wp-content/uploads/2015/12/instaicon2.png', description:'Muestra las fotos de Instagram',	accessToken: "TODO",
		 endpoint: "TODO" + "/api/aux/instagramTimeline",
		 language: "{{idioma}}"

		},
	];
	$scope.removeStarFilter = function(){
		$scope.starFilter = '';
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
			if ($scope.listComponentAdded[i][id]){
				finded = true;
				$scope.listComponentAdded.slice(i,1);
			}
		}
	}
	$scope.blurList = function(e){
		if ($scope.itemDescription = $scope.listComponentAdded){
			// del activated
			var index = $(e.currentTarget).attr('data-index');
			var id = $scope.listComponentAdded.splice(index,1);
			$scope.showList = $scope.listComponentAdded;
			$(id[0].name).parent().remove();
		}
	}
	$('#userHome').click(function(event){
		if (!event.target.hasAttribute('data-button') && !event.target.hasAttribute('data-list')){
			$('.component-list').removeClass('active');
			$('.menu-buttons').children().removeClass('active');
		}
	})

}]);
