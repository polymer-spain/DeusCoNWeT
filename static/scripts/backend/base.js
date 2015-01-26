'use strict';
/**
	 * @fileoverview
	 * Provides methods for the polymerBricks Endpoints sample UI and interaction with the
	 * polymerBricks Endpoints API.
	 */

/** google global namespace for Google projects. */
var google = google || [];
var apisToLoad = 1;// must match number of calls to gapi.client.load()
/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for App Engine sample code. */
google.appengine.api = google.appengine.api || {};

/** polymerBricks namespace for this sample. */
google.appengine.api.polymerBricks = google.appengine.api.polymerBricks || {};
/**
	 * Client ID of the application (from the APIs Console).
	 * @type {string}
	 */
google.appengine.api.polymerBricks.CLIENT_ID =
	'example-project-13';

/**
	 * Scopes used by the application.
	 * @type {string}
	 */
google.appengine.api.polymerBricks.SCOPES =
	'https://www.googleapis.com/auth/userinfo.email';
/**
	 * Whether or not the user is signed in.
	 * @type {boolean}
	 */
google.appengine.api.polymerBricks.signedIn = false;

/**
	 * Initializes the application.
	 * @param {string} apiRoot Root of the API's path.
	 */
google.appengine.api.polymerBricks.init = function (apiRoot) {
	// Loads the OAuth and helloworld APIs asynchronously, and triggers 
	// when they have completed.

	var callback = function () {
		if (--apisToLoad === 0) {

			var scope = angular.element(document.getElementById('views')).scope();
			scope.init();
		}
	};

	gapi.client.load('polymerbricks', 'v1.1', callback, apiRoot);
};

google.appengine.api.polymerBricks.getAllComponentsLimit = function (orderBy,sortBy,limit) {
	document.getElementById('tabs').style.cursor = 'wait';
	gapi.client.polymerbricks.components.getAllComponents({'orderBy' : orderBy,'sortBy': sortBy,'limit':limit}).execute(
		function(resp) {

			var scope = angular.element(document.getElementById('lista')).scope();
			scope.$apply(function () {
				scope.webComponents = resp.items;
				localStorage.setItem('components',JSON.stringify(resp.items));
			});
			document.getElementById('tabs').style.cursor = 'default';
		});
};

google.appengine.api.polymerBricks.getAllComponents = function (orderBy,sortBy) {
	document.getElementById('tabs').style.cursor = 'wait';
	gapi.client.polymerbricks.components.getAllComponents({'orderBy' : orderBy,'sortBy': sortBy}).execute(
		function(resp) {

			var scope = angular.element(document.getElementById('views')).scope();
			scope.$apply(function () {
				scope.webComponents = resp.items;
				localStorage.setItem('components',JSON.stringify(resp.items));
			});
			document.getElementById('tabs').style.cursor = 'default';
		});
};

google.appengine.api.polymerBricks.uploadComponent = function (URL) {
	gapi.client.polymerbricks.components.uploadComponent({'url' : URL}).execute (
		function(resp) {
			var scope = angular.element(document.getElementById('inputC')).scope();
			if (resp.status_code === undefined){
				if (resp.code === 404) {
					scope.loadModal(404);
				} else {
					scope.loadModal(403);
				}
			} else  {
				scope.loadModal(201);
			}
		});
};

google.appengine.api.polymerBricks.getComponent = function (component) {
	gapi.client.polymerbricks.components.getComponent({'idComponent' : component}).execute(
		function (resp) {
			var scope = angular.element(document.getElementById('views')).scope();
			console.log("Llamada a get component");
			scope.$apply(function () {
				scope.component = resp;
				localStorage.setItem('component',JSON.stringify(resp));
				console.log(resp);
			});
			return resp;
		});
}
google.appengine.api.polymerBricks.rateComponent = function (idComponent, rate) {
	gapi.client.polymerbricks.components.rateComponent({'idComponent': idComponent,'rate': rate}).execute(function () {
	})
	google.appengine.api.polymerBricks.getComponent = function (component,userId) {
		gapi.client.polymerbricks.components.getComponent({'idComponent' : component,'user': userId}).execute(
			function (resp) {
				var scope = angular.element(document.getElementById('views')).scope();
				scope.$apply(function () {
					scope.component = resp;
					document.querySelector('#rate').value = resp.userRating;

					localStorage.setItem('component',JSON.stringify(resp));
				});
				return resp;
			});
	};
	google.appengine.api.polymerBricks.rateComponent = function (idComponent, rate, UserId) {
		gapi.client.polymerbricks.components.rateComponent({'idComponent': idComponent,'rate': rate,'user': UserId}).execute(function () {
		});

	};
};

var onSignInCallback = function(authResult) {
	gapi.client.load('plus','v1').then(function() {
		var scope= [];
		var rate = [];
		if (authResult.access_token) {
			scope = angular.element(document.querySelector('#login')).scope();
			document.querySelector('#g-signout').addEventListener('click',disconnect);
			gapi.client.plus.people.get( {'userId' : 'me'} ).execute(function(resp) {
				rate = document.querySelector('#rate');
				if (rate  != undefined ) {
					angular.element(document.querySelector('#rate')).scope().init();
				}
				scope.$apply(function () {
					scope.logueado = true;
					scope.user = resp;
					document.querySelector('#g-signout').setAttribute('src',resp.image.url);
					document.querySelector('#userName').innerHTML = scope.user.name.givenName;

				});

			});

		} else if (authResult.error) {
			scope = angular.element(document.querySelector('#login')).scope();
			rate = document.querySelector('#rate');
			if (rate != undefined) {
				rate.setAttribute('readOnly',true);
			}
			scope.$apply(function () {
				scope.logueado = false;
			});
		}
	});
};

var disconnect =  function() {
	// Revoke the access token.

	var callback = function() {
		var scope = angular.element(document.querySelector('#login')).scope();
		scope.$apply(function(){
			scope.logueado = false;
			document.querySelector('#userName').innerHTML = "";
			if ((rate = document.querySelector('#rate')) !== undefined) {
				rate.setAttribute('readOnly',true);
			}
			scope.user = [];
		});
	};

	var url = 'https://accounts.google.com/o/oauth2/revoke?token=' +
			gapi.auth.getToken().access_token;
	jsonp(url,callback);
};

var jsonp = function (url, callback) {
	var callbackName = 'jsonp_callback_' + Math.round(100000 * Math.random());

	window[callbackName] = function() {
		delete window[callbackName];
		document.body.removeChild(script);
		callback();
	};

	var script = document.createElement('script');
	script.src = url + (url.indexOf('?') >= 0 ? '&' : '?') + 'callback=' + callbackName;
	document.body.appendChild(script);
};
