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
			controller: 'MainController',
			resolve: {
				auth: ['$cookies', '$backend', '$rootScope', '$q', '$location', function ($cookies, $backend, $rootScope, $q, $location) {
					var cookieSession = $cookies.get('session');
					var userId = $cookies.get('user');
					var socialnetwork = $cookies.get('social_network');
					//Si tiene credenciales, pedimos los datos y le llamos a su pagina principal
					if (cookieSession && userId && socialnetwork ) {
						var requestUser = $backend.syncGetUser(userId);
						if (requestUser.status === 200) {
							$rootScope.user = JSON.parse(requestUser.response);
							var tokens = $backend.getTokens($rootScope.user.token_ids);
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
			controller: 'UserHomeController'/*,
			resolve: {
				auth: ['$q', '$cookies', '$backend', '$rootScope', '$route', function ($q, $cookies, $backend, $rootScope, $route) {

					var session = $cookies.get('session');
					var userId = $cookies.get('user');
					if ($route.current.params.user_id !== userId) {
						return $q.reject({authorized: false});
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
							return $q.reject({authenticated: false});
						}
					} else {
						return $q.reject({authenticated: false});
					}
				}]
			}*/
		}).when('/user/:user_id/profile', {
			templateUrl: 'views/userProfile.html',
			controller: 'UserProfileController'/*,
			resolve: {
				auth: ['$q', '$cookies', '$backend', '$rootScope', '$route', function ($q, $cookies, $backend, $rootScope, $route) {

					var session = $cookies.get('session');
					var userId = $cookies.get('user');
					if ($route.current.params.user_id !== userId) {
						return $q.reject({authorized: false});
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
							return $q.reject({authenticated: false});
						}
					} else {
						return $q.reject({authenticated: false});
					}
				}]
			}*/
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

	}]);
})(wrap(document));
