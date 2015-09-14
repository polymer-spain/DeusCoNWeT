/*global angular, document, wrap, console*/
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
      controller: "LandingController",
      resolve: {
        auth: ["$cookies", "$backend", "$rootScope", "$q", "$location", function ($cookies, $backend, $rootScope, $q, $location) {
          var cookieSession = $cookies.get("session");
          var userId = $cookies.get("user_id");
          var socialnetwork = $cookies.get("socialnetwork");
          /* Si tiene credenciales, pedimos los datos y le llamos a su pagina principal */
          if (cookieSession && userId && socialnetwork ) {
            $backend.getUser(userId)
              .then(function (response) {
              $rootScope.user = response.data;
              if (!$rootScope.unauthorized) {
                $location.path("/user/" + userId); 
                return $q.when();
              }
            }, function (response) {
              console.error(response.data.error);
              $backend.logout();
              return $q.when();
            });
          }
        }]
      }
    })
      .when("/user/:user_id", {
      templateUrl: "views/userHome.html",
      controller: "UserHomeController",
      resolve: {

        auth: ["$q", "$cookies", "$backend", "$rootScope", "$route", function ($q, $cookies, $backend, $rootScope, $route) {

          var session = $cookies.get("session");
          var userId = $cookies.get("user_id");
          if ($route.current.params.user_id !== userId) {
            return $q.reject({authorized: false});
          }
          else if (session && userId) {
            $backend.getUser(userId).then(function (response) {
              $rootScope.user = response.data;
              return $q.when(session);
            }, function (response) {
              console.error("Error " + response.status + ": al intentar coger los datos del usuario " + userId);
              return $q.reject();
            });

          } else {
            return $q.reject({authenticated: false});
          }
        }]
      }
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
        auth: ["$q", "$cookies", function ($q, $cookies) {

          var session = $cookies.get("session");

          if (session) {
            return $q.when(session);
          } else {
            return $q.reject({
              authenticated: false
            });
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
      controller: "SelectidController"
/*      resolve: {
        auth: ["$q", "$rootScope", function ($q, $rootScope) {

          if ($rootScope.register) {
            return $q.when($rootScope.register);
          } else {
            return $q.reject({
              register: false
            });
          }
        }]
      }*/
    })
    /* Por defecto */
      .otherwise({
      redirectTo: "/"
    });
    $locationProvider.html5Mode(true);
  }]);

  app.run(["$rootScope", "$location", function ($rootScope, $location) {
    $rootScope.$on("$routeChangeError", function (event, current, previous, eventObj) {
      if (!eventObj.authorized) {
        $rootScope.unauthorized = true;
        $location.path("/");
      } else if (!eventObj.authenticated || !eventObj.register) {
          $location.path("/");
        }
    });

  }]);
})(wrap(document));