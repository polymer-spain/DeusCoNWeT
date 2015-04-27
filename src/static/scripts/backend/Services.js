angular.module('picbit').service('$backend', function () {
  'use strict';
  this.endpoint = 'http://example-project-13.appspot.com';

  /* Envia el token y el identificador del token correspondiente a una red social */
  this.sendData = function (token, tokenId, redSocial, callback, errorCallback) {
    var xhr, uri, params;
    xhr = new XMLHttpRequest();
    uri = this.endpoint + '/api/oauth/' + redSocial;
    params = "token_id=" + tokenId + "&access_token=" + token;

    xhr.open("POST", uri, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && (xhr.status === 200 || xhr.status === 201) && callback) {
        callback(xhr.responseText);
      } else if (xhr.readyState === 4 && errorCallback) {
        errorCallback(xhr.responseText, xhr.status);
      }
    };
    xhr.send(params);
  };

  /* Contacto: envia un email al backend */
  this.sendEmail = function (message, sender, subject, callback, errorCallback) {
    var xhr, uri, params;
    xhr = new XMLHttpRequest();
    uri = this.endpoint + '/api/contact';
    params = "action=contact&message=" + message.value + "&sender=" + sender.value;

    if (subject) {
      params += '&subject=' + subject;
    }

    xhr.open("POST", uri, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && (xhr.status === 200) && callback) {
        callback(xhr.responseText);
      } else if (xhr.readyState === 4 && !(xhr.status === 201 && errorCallback)) {
        errorCallback(xhr.responseText, xhr.status);
      }
    };
    xhr.send(params);
  };

  this.sendSub = function (name, sender, surname, callback, errorCallback) {
    var xhr, uri, params;
    xhr = new XMLHttpRequest();
    uri = this.endpoint + '/api/subscriptions';
    params = "name=" + name.value + "&email=" + sender.value + "&surname=" + surname.value;

    xhr.open("POST", uri, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 201 && callback) {
        callback(xhr.responseText);
      } else if (xhr.readyState === 4 && errorCallback) {
        errorCallback(xhr.responseText, xhr.status);
      }

    };
    xhr.send(params);
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