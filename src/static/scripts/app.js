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
    .config(function ($locationProvider, $routeProvider,$httpProvider) {

    $routeProvider
    /* Español */
      .when('/', {
      templateUrl: 'views/es/landingPage.html',
      controller: 'landingCtrl'
    })
      .when('/user/:userId', {
      templateUrl: 'views/es/userHome.html',
      controller: 'userHomeCtrl'
    })
      .when('/about', {
      templateUrl: 'views/es/about.html',
      controller: 'aboutCtrl'
    })
      .when('/contact', {
      templateUrl: 'views/es/contact.html',
      controller: 'contactCtrl'
    })
      .when('/privacy',{
      templateUrl: 'views/es/privacy.html',
      controller: 'privacyCtrl'
    })

    /* Ingles */
      .when('/en', {
      templateUrl: 'views/en/landingPage.html',
      controller: 'landingCtrl'
    })
      .when('/en/user/:userId', {
      templateUrl: 'views/en/userHome.html',
      controller: 'userHomeCtrl'
    })
      .when('/en/about', {
      templateUrl: 'views/en/about.html',
      controller: 'aboutCtrl'
    })
      .when('/en/contact', {
      templateUrl: 'views/es/contact.html',
      controller: 'contactCtrl'
    })
      .when('/en/privacy',{
      templateUrl: 'views/en/privacy.html',
      controller: 'privacyCtrl'
    })
    /* Por defecto */
      .otherwise({redirectTo: '/'})
    ;
    $locationProvider.html5Mode(true)
  });
  document.addEventListener('polymer-ready', function() {
    // Perform some behaviour

  });
  // wrap document so it plays nice with other libraries

})(wrap(document));