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
    'ng-polymer-elements'
  ])
    .config(function ($locationProvider, $routeProvider,$httpProvider) {

    $routeProvider
      .when('/', {
      templateUrl: 'views/landingPage.html',
      controller: 'landingCtrl'
    })
      .when('/user/:userId', {
      templateUrl: 'views/userHome.html',
      controller: 'userHomeCtrl'
    })
      .when('/about', {
      templateUrl: 'views/about.html',
      controller: 'aboutCtrl'
    })
      .when('/contact', {
      templateUrl: 'views/contact.html',
      controller: 'contactCtrl'
    })
      .when('/privacy',{
      templateUrl: 'views/privacy.html',
      controller: 'privacyCtrl'
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