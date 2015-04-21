
/* Llamadas a las api*/
var base = "http://hydra.ls.fi.upm.es:8080/";

// Peticion de todos los componentes ordenados //
var getAllComponents = function (orderBy, sortBy, callback) {
	xhr = new XMLHttpRequest();
	var url = base + "componentes";
	xhr.open("GET", url, true);

	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			if (callback != undefined) {
				eval(callback(JSON.parse(xhr.responseText)));
			}
		}
	}
	xhr.send();
}


// Peticion de un componentes

var getComponent = function(id_componente,usuario,callback) {
	xhr = new XMLHttpRequest();
	
	if (usuario != undefined) {
		var params = "?user="+usuario;
	}
	var url = base + "componentes/"+id_componente+params;

	xhr.open("GET",url,true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState ==  4) {
			if (callback != undefined) {
				eval(callback(JSON.parse(xhr.responseText)));	
			};
		}
	};
	xhr.send();
}

// Valorar un componente 

var rateComponent = function(id_componente,valoracion,usuario,callback) {
	var xhr = new XMLHttpRequest();

	var params="?rate="+valoracion+"\&user="+usuario;
	var url = base + "componentes/"+id_componente+params;

	xhr.open("POST",url,true);
	xhr.onreadystatechange = function() {
		if (xhr.readyState == 4) {
			if (callback != undefined) {
				eval(callback);		
			};
		}
	};
	xhr.send();
}

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
