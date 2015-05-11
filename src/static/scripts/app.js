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

    $routeProvider
      .when('/', {
      templateUrl: 'views/landingPage.html',
      controller: 'landingCtrl'
    })
      .when('/user/:userId', {
      templateUrl: 'views/userHome.html',
      controller: 'userHomeCtrl',
      resolve: {
        auth: ["$q", function($q){
          var cookie, session, patron, exp;
          cookie = document.cookie;
          patron = "session"+"=([^&#]*)";
          exp = new RegExp(patron);
          session = exp.exec(cookie);
          session = session ? session[1] : undefined;
          
          if (session) {
            return $q.when(cookie);
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
      .when('/privacy',{
      templateUrl: 'views/privacy.html',
      controller: 'privacyCtrl'
    })
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
