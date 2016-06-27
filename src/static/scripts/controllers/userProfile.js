/*global angular*/
angular.module("picbit")
	.controller("UserProfileController", ["$scope", function ($scope) {
		"use strict";
		
		$scope.selectSection = function(e){
			var $target = $(e.currentTarget);
			var sectionTarget = $target.attr('data-target');
			
			$('.information').children().removeClass('active');
			$('.tabs').children().removeClass('active');
						
			$target.parent().addClass('active');
			$(sectionTarget).addClass('active');
		}

	}]);
