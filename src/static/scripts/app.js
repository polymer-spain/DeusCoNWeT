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
			templateUrl: 'views/landingPage.html',
			controller: 'landingCtrl'
		})
		.when('/user/:userId', {
			templateUrl: 'views/userHome.html',
			controller: 'userHomeCtrl'
		})
		.when('/sandbox', {
			templateUrl: 'static/views/sandbox.html',
			controller: 'SandboxCtrl'
		})
		.when('/components/:componentID',{
			templateUrl: 'static/views/repositorio.html',
			controller: 'ComponentCtrl'
		})
		.when('/search',{
			templateUrl: 'static/views/search.html',
			controller: 'SearchCtrl'
		})
		.when('/profile/:userId', {
			templateUrl: 'static/views/profile.html',
			controller: 'ProfileCtrl'
		});
	});

	document.addEventListener('polymer-ready', function() {
		// Perform some behaviour

	});
	// wrap document so it plays nice with other libraries

})(wrap(document));