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
      .when('/formulario', {
      templateUrl: 'views/formulario.html',
      controller: 'FormularioCtrl'
    })
      .when('/search',{
      templateUrl: 'static/views/search.html',
      controller: 'SearchCtrl'
    })
      .when('/user/:userId/profile', {
      templateUrl: 'views/profile.html',
      controller: 'ProfileCtrl'
		
    })
      .otherwise({redirectTo: '/'})
    ;
    $locationProvider.html5Mode(true)
  });
  document.addEventListener('polymer-ready', function() {
    // Perform some behaviour

  });
	
  // wrap document so it plays nice with other libraries

})(wrap(document));