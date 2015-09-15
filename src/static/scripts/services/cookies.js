/*global angular, document*/
angular.module("picbit").service("$cookie", function () {
  "use strict";
  this.get = function (name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) {
      return parts.pop().split(";").shift();
    }
  };

  this.put  = function (key, value, expires, path, domain, secure) {
    var cookie;
    cookie = key + "=" + value;
    if (expires) {
      cookie += "; expires=" + expires;
    }
    if (path) {
      cookie += "; path=" + path;
    }
    if (domain) {
      cookie += "; domain=" + domain;
    }
    if (secure) {
      cookie += "; secure";
    }
    document.cookie = cookie;
  };

  this.delete = function (name) {
    document.cookie = name + "=; expires= Thu, 01 jan 1970 00:00:00 UTC";
  };
  this.set = function (key, value, expires, path, domain, secure) {
    this.put(key, value, expires, path, domain, secure);
  };
  this.getAll = function () {
    return document.cookie;
  };
});
