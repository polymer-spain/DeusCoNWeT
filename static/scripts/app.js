(function (document) {

	'use strict';
	/**
	 * @ngdoc overview
	 * @name PolymerBricks
	 * @description
	 * # PolymerBricks
	 *
	 * Main module of the application.
	*/
	angular
	.module('PolymerBricks', [
		'ngAnimate',
		'ngCookies',
		'ngResource',
		'ngRoute',
		'ngSanitize',
		'ngTouch',
		'ng-polymer-elements',
		'ui.bootstrap'
	])
	.config(function ($locationProvider, $routeProvider) {

		$routeProvider
		.when('/', {
			templateUrl: 'views/home.html',
			controller: 'HomeCtrl'
		})
		.when('/about', {
			templateUrl: 'views/about.html',
			controller: 'AboutCtrl'
		})
		.when('/sandbox', {
			templateUrl: 'views/sandbox.html',
			controller: 'SandboxCtrl'
		})
		.when('/components/:componentID',{
			templateUrl: 'views/repositorio.html',
			controller: 'ComponentCtrl'
		})
		.when('/search',{
			templateUrl: 'views/search.html',
			controller: 'SearchCtrl'
		})
		.when('/profile/:userId', {
			templateUrl: 'views/profile.html',
			controller: 'ProfileCtrl'
		});
	});

	document.addEventListener('polymer-ready', function() {
		// Perform some behaviour

	});
	// wrap document so it plays nice with other libraries

})(wrap(document));