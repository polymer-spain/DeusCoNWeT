/*global angular, document, setTimeout, self*/
angular.module("picbit").service("$anchorSmoothScroll", function () {
  "use strict";

  function currentYPosition() {
    // Firefox, Chrome, Opera, Safari
    if (self.pageYOffset) {
      return self.pageYOffset;
    }
    // Internet Explorer 6 - standards mode
    if (document.documentElement && document.documentElement.scrollTop) {
      return document.documentElement.scrollTop;
    }
    // Internet Explorer 6, 7 and 8
    if (document.body.scrollTop) {
      return document.body.scrollTop;
    }
    return 0;
  }

  function elmYPosition(eID) {
    var elm = document.getElementById(eID);
    var y = elm.offsetTop;
    var node = elm;
    while (node.offsetParent && node.offsetParent !== document.body) {
      node = node.offsetParent;
      y += node.offsetTop;
    } return y;
  }
  this.scrollTo = function (eID) {
    var startY = currentYPosition();
    var stopY = elmYPosition(eID);
    var distance = stopY > startY ? stopY - startY : startY - stopY;
    if (distance < 100) {
      this.scrollTo(0, stopY);
      return;
    }
    var speed = Math.round(distance / 100);
    speed = 25;
    var step = Math.round(distance / 25);
    var leapY = stopY > startY ? startY + step : startY - step;
    var timer = 0;
    var i;
    if (stopY > startY) {
      for (i = startY; i < stopY; i += step) {
        setTimeout("window.scrollTo(0, " + leapY + ")", timer * speed);
        leapY += step;
        if (leapY > stopY) {
          leapY = stopY;
        }
        timer++;
      } return;
    }
    for (i = startY; i > stopY; i -= step ) {
      setTimeout("window.scrollTo(0, " + leapY + ")", timer * speed);
      leapY -= step;
      if (leapY < stopY) {
        leapY = stopY;
      }
      timer++;
    }
  };

});
