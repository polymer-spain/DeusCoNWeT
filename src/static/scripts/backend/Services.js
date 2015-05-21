angular.module('picbit').service('$backend', function ($http, $location) {
  'use strict';
  this.endpoint = 'https://' + $location.host();
  /* Envia el token y el identificador del token correspondiente a una red social */
  this.sendData = function (token, tokenId, redSocial, callback, errorCallback) {
    var request, uri, params;
    uri = this.endpoint + '/api/oauth/' + redSocial;
    params = "token_id=" + tokenId + "&access_token=" + token + "&action=login";
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };
    $http(request).success(function (data) {
      if (callback) {
        callback(data);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };

  /* Contacto: envia un email al backend */
  this.sendEmail = function (message, sender, subject, callback, errorCallback) {
    var request, uri, params;

    uri = this.endpoint + '/api/contact';
    params = "action=contact&message=" + message + "&sender=" + sender;

    if (subject) {
      params += '&subject=' + subject;
    }
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };
    $http(request).success(function (data, status) {
      if (callback) {
        callback(data);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };

  this.sendSub = function (name, sender, surname, callback, errorCallback) {
    var request, uri, params;
    uri = this.endpoint + '/api/subscriptions';
    params = "name=" + name + "&email=" + sender + "&surname=" + surname;
    request = {
      method: 'post',
      url: uri,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    };

    $http(request).success(function (data, status) {

      if (callback) {
        callback(data,status);
      }
    }).error(function (data, status) {
      if (errorCallback) {
        errorCallback(data, status);
      }
    });
  };


}).service('$anchorSmoothScroll', function () {
  'use strict';

  this.scrollTo = function (eID) {
    var startY = currentYPosition();
    var stopY = elmYPosition(eID);
    var distance = stopY > startY ? stopY - startY : startY - stopY;
    if (distance < 100) {
      scrollTo(0, stopY); return;
    }
    var speed = Math.round(distance / 100);
    speed = 25;
    var step = Math.round(distance / 25);
    var leapY = stopY > startY ? startY + step : startY - step;
    var timer = 0;
    if (stopY > startY) {
      for (var i=startY; i<stopY; i+=step) {
        setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
        leapY += step; if (leapY > stopY) leapY = stopY; timer++;
      } return;
    }
    for ( var i=startY; i>stopY; i-=step ) {
      setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
      leapY -= step; if (leapY < stopY) leapY = stopY; timer++;
    }
    function currentYPosition() {
      // Firefox, Chrome, Opera, Safari
      if (self.pageYOffset) return self.pageYOffset;
      // Internet Explorer 6 - standards mode
      if (document.documentElement && document.documentElement.scrollTop)
        return document.documentElement.scrollTop;
      // Internet Explorer 6, 7 and 8
      if (document.body.scrollTop) return document.body.scrollTop;
      return 0;
    }

    function elmYPosition(eID) {
      var elm = document.getElementById(eID);
      var y = elm.offsetTop;
      var node = elm;
      while (node.offsetParent && node.offsetParent != document.body) {
        node = node.offsetParent;
        y += node.offsetTop;
      } return y;
    }

  };

});
