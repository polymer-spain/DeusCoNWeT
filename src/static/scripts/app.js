/*global angular, document, wrap*/
(function () {

  "use strict";

  var app = angular.module("picbit", [
    "ngAnimate",
    "ngResource",
    "ngRoute",
    "ngSanitize",
    "ngTouch",
    "ng-polymer-elements"
  ]);

  app.config(["$locationProvider", "$routeProvider", "$httpProvider", function ($locationProvider, $routeProvider, $httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    $routeProvider
    /* Español */
      .when("/", {
      templateUrl: "views/landingPage.html",
      controller: "LandingController"
    })
      .when('/user/:userId', {
      templateUrl: 'views/userHome.html',
      controller: 'UserHomeController'
      /*      Para ejecutar el localhost sin login:
        resolve: {

        auth: ["$q", "$cookie", function($q, $cookie){

          var session = $cookie.get("session");

          if (session) {
            return $q.when(session);
          } else {
            return $q.reject({authenticated: false});
          }
        }]
      }*/
    })
      .when("/about", {
      templateUrl: "views/about.html",
      controller: "AboutController"
    })
      .when("/contact", {
      templateUrl: "views/contact.html",
      controller: "ContactController"
    })
      .when("/user/:userId/profile", {
      templateUrl: "views/profile.html",
      controller: "ProfileController",
      resolve: {
        auth: ["$q", "$cookie", function($q, $cookie){

          var session = $cookie.get("session");

          if (session) {
            return $q.when(session);
          } else {
            return $q.reject({authenticated: false});
          }
        }]
      }
    })
      .when("/privacy", {
      templateUrl: "views/privacy.html",
      controller: "PrivacyController"
    })
      .when("/selectId", {
      templateUrl: "views/selectId.html",
      controller: "SelectidController",
      resolve: {
        auth: ["$q", "$rootScope", function($q, $rootScope) {

          if ($rootScope.register) {
            return $q.when($rootScope.register);
          } else {
            return $q.reject({register: false});
          }
        }]
      }
    })
    /* Por defecto */
      .otherwise({redirectTo: "/"})
    ;
    $locationProvider.html5Mode(true);
  }]);

  app.run(["$rootScope", "$location", function($rootScope, $location) {
    $rootScope.$on("$routeChangeError", function(event, current, previous, eventObj) {
      if (!eventObj.authenticated) {
        $location.path("/");
      } else if (!eventObj.register) {
        $location.path("/");
      }
    });

  }]);
})(wrap(document));
