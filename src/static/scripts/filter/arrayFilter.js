/*global angular*/
angular.module("picbit").filter("arrayFilter", function() {
	"use strict";

	return function (items, arrayFilter) {
		var filtered = [];
		angular.forEach(items, function(item) {
			if (arrayFilter.indexOf(item.name) === -1) {
					filtered.push(item);
			}
		});//forEach
		return filtered;
	};//return function
});//filter
