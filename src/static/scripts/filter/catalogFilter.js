/*global angular*/
angular.module("picbit").filter("catalogFilter", function() {
	"use strict";

	return function (input, name, star) {
		star = parseInt(star) || 0;
		name = name || '';
		var result = [];
		
		angular.forEach(input, function(item){
			if (item.rate >= star && item.name.indexOf(name) != -1){
				result.push(item);
			}
		});
		return result;
	}
});
