(function () {

  'use strict';

  var app = angular.module('picbit', [
    'ngAnimate',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch'
  ]);

  app.config(['$locationProvider', '$routeProvider', '$httpProvider', function ($locationProvider, $routeProvider, $httpProvider) {
    $httpProvider.defaults.withCredentials = true;
    $routeProvider
      .when('/', {
        templateUrl: 'views/landingPage.html',
        resolve: {
          auth: ['$cookies', '$backend', '$rootScope', '$q', '$location', function ($cookies, $backend, $rootScope, $q, $location) {
            var cookieSession = $cookies.get('session');
            var userId = $cookies.get('user');
            var socialnetwork = $cookies.get('social_network');
            var requestUser, tokens;
            //Si tiene credenciales, pedimos los datos y le llamos a su pagina principal
            if (cookieSession && userId && socialnetwork) {
              requestUser = $backend.syncGetUser(userId);
              if (requestUser.status === 200) {
                $rootScope.user = JSON.parse(requestUser.response);
                tokens = $backend.getTokens($rootScope.user.token_ids);
                $rootScope.user.tokens = tokens;
                $rootScope.isLogged = true;
                if (!$rootScope.unauthorized) {
                  $location.path('/user/' + userId);
                  return $q.when();
                }
              } else {
                console.error(requestUser.statusText);
                $backend.logout();
                return $q.when();
              }
            }
          }]
        }
      })
      .when('/user/:user_id', {
        templateUrl: 'views/userHome.html',
        controller: 'UserHomeController',
        /*resolve: {
          auth: ['$q', '$rootScope', function ($q, scope) {
            scope.user = {
              "surname": null,
              "email": null,
              "social_nets_use": null,
              "nets": [
                "googleplus"
              ],
              "age": null,
              "token_ids": [],
              "studies": null,
              "user_id": "MIguel",
              "name": null,
              "private_phone": false,
              "references": [
                "/bower_components/facebook-wall-stable/facebook-wall.html",
                "/bower_components/googleplus-timeline-stable/googleplus-timeline.html",
                "/bower_components/traffic-incidents-stable/traffic-incidents.html",
                "/bower_components/finance-search-stable/finance-search.html",
                "/bower_components/pinterest-timeline-stable/pinterest-timeline.html",
                "/bower_components/open-weather-stable/open-weather.html",
                "/bower_components/twitter-timeline-stable/static/twitter-timeline.html"
              ],
              "private_email": false,
              "image": null,
              "website": null,
              "components": "{\"data\": [{\"user_rate\": 0.0, \"component_id\": \"facebook-wall\"}, {\"user_rate\": 0.0, \"component_id\": \"googleplus-timeline\"}, {\"user_rate\": 0.0, \"component_id\": \"traffic-incidents\"}, {\"user_rate\": 0.0, \"component_id\": \"finance-search\"}, {\"user_rate\": 0.0, \"component_id\": \"pinterest-timeline\"}, {\"user_rate\": 0.0, \"component_id\": \"open-weather\"}, {\"user_rate\": 0.0, \"component_id\": \"twitter-timeline\"}]}",
              "description": null,
              "tech_exp": null,
              "gender": null,
              "phone": null,
              "tokens": {
                "googleplus": "ya29.GmGGBE9MfOTWE1ApFNajTquQzIWbpZ1YQKv6p2JdzWhmXmMEZW1eIF7p0lXJBnKlKHPRmN--WvTQTr3otDd5F_UegJEeOcbzBo7LmLREx4UJ-bNR07MmdFrLXkfDNjorN425",
                "twitter": "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf"
              }
            };
            scope.catalogList = [
              {
                "version": "stable",
                "social_network": "facebook",
                "attributes": {
                  "access_token": "",
                  "component_directory": "bower_components/facebook-wall/"
                },
                "tokenAttr": "access_token",
                "url": "https://github.com/Mortega5/facebook-wall",
                "img": "images/components/facebook-icon.png",
                "rate": "0",
                "description": "Web component to obtain the timeline of Facebook messages using Polymer",
                "component_id": "facebook-wall",
                "$$hashKey": "object:31"
              },
              {
                "version": "stable",
                "social_network": "googleplus",
                "attributes": {
                  "token": "ya29.GmGGBE9MfOTWE1ApFNajTquQzIWbpZ1YQKv6p2JdzWhmXmMEZW1eIF7p0lXJBnKlKHPRmN--WvTQTr3otDd5F_UegJEeOcbzBo7LmLREx4UJ-bNR07MmdFrLXkfDNjorN425",
                  "api_key": "AIzaSyAArT6pflqm1-rj9Nwppuj_4z15FFh4Kis"
                },
                "tokenAttr": "token",
                "url": "https://github.com/ailopera/googleplus-timeline",
                "img": "images/components/google-icon.svg",
                "rate": "0",
                "description": "Web component to obtain the timeline of Google Plus using Polymer",
                "component_id": "googleplus-timeline",
                "$$hashKey": "object:32"
              },
              {
                "version": "stable",
                "social_network": "",
                "attributes": {
                  "app_key_traffic": "AmWMG90vJ0J9Sh2XhCp-M3AFOXJWAKqlersRRNvTIS4GyFmd3MxxigC4-l0bdvz-",
                  "api_key_geocoding": "AIzaSyC3shMTM6dD10MGqty-xugLBUFSCTICeBM"
                },
                "tokenAttr": "",
                "url": "https://github.com/Mortega5/traffic-incidents",
                "img": "images/components/traffic-incidents-icon.png",
                "rate": "0",
                "description": "Web component to know the state of the traffic in a certain city",
                "component_id": "traffic-incidents",
                "$$hashKey": "object:33"
              },
              {
                "version": "stable",
                "social_network": "",
                "attributes": {},
                "tokenAttr": "",
                "url": "https://github.com/Mortega5/finance-search",
                "img": "images/components/finance-search-icon.png",
                "rate": "0",
                "description": "Web component to know the values of shares",
                "component_id": "finance-search",
                "$$hashKey": "object:34"
              },
              {
                "version": "stable",
                "social_network": "pinterest",
                "attributes": {
                  "token": "",
                  "component_base": "bower_components/pinterest-timeline-stable/"
                },
                "tokenAttr": "token",
                "url": "https://github.com/polymer-spain/DeusCoNWeT/tree/redesign/src/static/bower_components/pinterest-timeline-stable",
                "img": "images/components/pinterest.png",
                "rate": "0",
                "description": "Web component to obtain the timeline of Pinterest messages using Polymer",
                "component_id": "pinterest-timeline",
                "$$hashKey": "object:35"
              },
              {
                "version": "stable",
                "social_network": "",
                "attributes": {
                  "app-id": "655f716c02b3f0aceac9e3567cfb46a8"
                },
                "tokenAttr": "",
                "url": "https://github.com/Mortega5/open-weather",
                "img": "images/components/open-weather-icon.png",
                "rate": "0",
                "description": "Web component to know the weather in future days",
                "component_id": "open-weather",
                "$$hashKey": "object:36"
              },
              {
                "version": "stable",
                "social_network": "twitter",
                "attributes": {
                  "secret_token": "OBPFI8deR6420txM1kCJP9eW59Xnbpe5NCbPgOlSJRock",
                  "count": 200,
                  "consumer_key": "BOySBn8XHlyYDQiGiqZ1tzllx",
                  "consumer_secret": "xeSw5utUJmNOt5vdZZy8cllLegg91vqlzRitJEMt5zT7DtRcHE",
                  "access_token": "3072043347-T00ESRJtzlqHnGRNJZxrBP3IDV0S8c1uGIn1vWf",
                  "language": "{{idioma}}",
                  "endpoint": "https://centauro.ls.fi.upm.es/api/aux/twitterTimeline",
                  "component_base": "bower_components/twitter-timeline/static/"
                },
                "tokenAttr": "access_token",
                "url": "https://github.com/JuanFryS/twitter-timeline",
                "img": "images/components/twitter-logo.png",
                "rate": "0",
                "description": "Web component to obtain the timeline of Twitter using Polymer",
                "component_id": "twitter-timeline",
                "$$hashKey": "object:37"
              }
            ];
            return $q.when()
          }]
        }*/
        resolve: {
          auth: ['$q', '$cookies', '$backend', '$rootScope', '$route', function ($q, $cookies, $backend, $rootScope, $route) {
            var session = $cookies.get('session');
            var userId = $cookies.get('user');
            if ($route.current.params.user_id !== userId) {
              return $q.reject({ authorized: false });
            }
            else if (session && userId) {
              var responseUser = $backend.syncGetUser(userId);

              if (responseUser.status === 200) {
                $rootScope.user = JSON.parse(responseUser.response);
                var tokens = $backend.getTokens($rootScope.user.token_ids);
                $rootScope.user.tokens = tokens;
                $rootScope.isLogged = true;
                return $q.when(session);

              } else {
                console.error('Error ' + responseUser.status + ': al intentar coger los datos del usuario ' + userId);
                $backend.logout();
                return $q.reject({ authenticated: false });
              }
            } else {
              return $q.reject({ authenticated: false });
            }
          }]
        }
      }).when('/user/:user_id/profile', {
        templateUrl: 'views/userProfile.html',
        controller: 'UserProfileController',
        resolve: {
          auth: ['$q', '$cookies', '$backend', '$rootScope', '$route', function ($q, $cookies, $backend, $rootScope, $route) {
            var responseUser, tokens;
            var session = $cookies.get('session');
            var userId = $cookies.get('user');
            if ($route.current.params.user_id !== userId) {
              return $q.reject({ authorized: false });
            }
            else if (session && userId) {
              responseUser = $backend.syncGetUser(userId);

              if (responseUser.status === 200) {
                $rootScope.user = JSON.parse(responseUser.response);
                tokens = $backend.getTokens($rootScope.user.token_ids);
                $rootScope.user.tokens = tokens;
                $rootScope.isLogged = true;
                return $q.when(session);

              } else {
                console.error('Error ' + responseUser.status + ': al intentar coger los datos del usuario ' + userId);
                $backend.logout();
                return $q.reject({ authenticated: false });
              }
            } else {
              return $q.reject({ authenticated: false });
            }
          }]
        }
      })
      .when('/about', {
        templateUrl: 'views/about.html',
        controller: 'AboutController'
      })
      .when('/contact', {
        templateUrl: 'views/contact.html',
        controller: 'ContactController'
      })
      .when('/privacy', {
        templateUrl: 'views/privacy.html',
        controller: 'PrivacyController'
      })
      .when('/selectId', {
        templateUrl: 'views/selectId.html',
        controller: 'SelectidController',
        resolve: {
          auth: ['$q', '$rootScope', function ($q, $rootScope) {

            if ($rootScope.register) {
              return $q.when($rootScope.register);
            } else {
              return $q.reject({
                register: false
              });
            }
          }]
        }
      })
      /* Por defecto */
      .otherwise({
        redirectTo: '/'
      });
    $locationProvider.html5Mode(true);
  }]);

  app.run(['$rootScope', '$location', function ($rootScope, $location) {
    $rootScope.$on('$routeChangeError', function (event, current, previous, eventObj) {
      if (!eventObj.authorized) {
        $rootScope.unauthorized = true;
        $location.path('/');
      } else if (!eventObj.authenticated || !eventObj.register) {
        $location.path('/');
      }
    });
    $rootScope.$on('$routeChangeSuccess', function () {
      $rootScope.unauthorized = undefined;
    });

  }]);
})(wrap(document));
