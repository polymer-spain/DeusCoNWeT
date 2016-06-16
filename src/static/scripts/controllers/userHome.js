angular.module('picbit').controller('UserHomeController', ['$scope', '$timeout','$rootScope', function ($scope, $timeout, $rootScope) {
	'use strict';
	$scope.showList = ['test1','test2'];
	$scope.componentList = [
		{
			name: "twitter-timeline",
			attributes: {
				accessToken: "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
				secretToken: "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
				consumerKey: "J4bjMZmJ6hh7r0wlG9H90cgEe",
				consumerSecret: "8HIPpQgL6d3WWQMDN5DPTHefjb5qfvTFg78j1RdZbR19uEPZMf",
				endpoint: $scope.domain + "/api/aux/twitterTimeline",
				language: "{{idioma}}",
				count: "200"
			}
		},
		{
			name: "github-events",
			attributes: {
				username: "mortega5",
				token: "" || "",
				mostrar: "10",
				language: "{{idioma}}",
				component_directory: 'bower_components/github-events/'
			}
		},
		{
			name: "instagram-timeline",
			attributes: {
				accessToken: "TODO",
				endpoint: "TODO" + "/api/aux/instagramTimeline",
				language: "{{idioma}}"
			}
		}
	];
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

	$scope.activeAddCmpList = function(e){
		var $list = $('.component-list');
		if (!$list.hasClass('active')){
			$list.addClass('active');
		} else if($scope.showList == $scope.componentList) {
			$list.removeClass('active');
		}
		$scope.showList = $scope.componentList;
		$scope.itemDescription = "Arrastra el elemento para añadirlo al dashboard";
	};
	$scope.activeDelCmpList = function(){
		var $list = $('.component-list');
		if (!$list.hasClass('active')){
			$list.addClass('active');
		} else if($scope.showList == $scope.addedList) {
			$list.removeClass('active');
		}
		$scope.showList = $scope.listComponentAdded;
		$scope.itemDescription = "";
	}
	$scope.clicked = function(e){
		if ($scope.itemDescription = $scope.listComponentAdded){
			// del activated
			var index = $(e.currentTarget).attr('data-index');
			var id = $scope.listComponentAdded.splice(index,1);
			$scope.showList = $scope.listComponentAdded;
			$(id[0].name).remove();
		} else {
			// add activated
		}
	}
	$('#userHome').click(function(event){
		if (!event.target.hasAttribute('data-button') && !event.target.hasAttribute('data-list')){
			$('.component-list').removeClass('active');
			$('.menu-buttons').children().removeClass('active');
		}
	})

}]);
