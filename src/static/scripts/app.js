(function (document) {

  'use strict';
  /**
	 * @ngdoc overview
	 * @name picbit
	 * @description
	 * # PicBit
	 *
	 * Main module of the application.
	*/
  var app = angular
  .module('picbit', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ng-polymer-elements'
  ]);
  app.config(function ($locationProvider, $routeProvider,$httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    $routeProvider
    /* Español */
      .when('/', {
      templateUrl: 'views/landingPage.html',
      controller: 'landingCtrl'
    })
      .when('/user/:userId', {
      templateUrl: 'views/userHome.html',
      controller: 'userHomeCtrl',
      resolve: {
        auth: ["$q", "$cookie", function($q, $cookie){

          var session = $cookie.get('session');

          if (session) {
            return $q.when(session);
          } else {
            return $q.reject({authenticated: false})
          }
        }]
      }
    })
      .when('/about', {
      templateUrl: 'views/about.html',
      controller: 'aboutCtrl'
    })
      .when('/contact', {
      templateUrl: 'views/contact.html',
      controller: 'contactCtrl'
    })
      .when('/user/:userId/profile', {
      templateUrl: 'views/profile.html',
      controller: 'ProfileCtrl',
      /* Para poder editar el perfil en localhost
    resolve: {
        auth: ["$q", "$cookie", function($q, $cookie){

          var session = $cookie.get('session');

          if (session) {
            return $q.when(session);
          } else {
            return $q.reject({authenticated: false})
          }
        }]
      }*/
    })
      .when('/privacy',{
      templateUrl: 'views/privacy.html',
      controller: 'privacyCtrl'
    })
    /* Por defecto */
      .otherwise({redirectTo: '/'})
    ;
    $locationProvider.html5Mode(true)
  });

  app.run(["$rootScope", "$location", function($rootScope, $location) {
    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
      if (eventObj.authenticated === false) {
        $location.path("/");
      }
    });
  }]);
})(wrap(document));