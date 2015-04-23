

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */
angular.module('PolymerBricks')
  .service('anchorSmoothScroll', function () {
  this.scrollTo = function(eID) {
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
      for ( var i=startY; i<stopY; i+=step ) {
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

}).controller('landingCtrl', function ($scope,$timeout,$location,anchorSmoothScroll) {
  'use strict';
  if ($location.hash() === 'section1') {
    $scope.selected = 1;
  } else if ($location.hash() === 'section2') {
    $scope.selected = 2;
  }
  else if ($location.hash() === 'section3') {
    $scope.selected = 3;
  } else if ($location.hash() === 'section4') {
    $scope.selected = 4;
  }
  else {
    $scope.selected = 1;
  }

  $scope.cambiarAnchor = function(section){
    $location.hash(section);
    anchorSmoothScroll.scrollTo(section);   
  };
  $scope.setStyle = function (el, el2){
    document.querySelector(el).removeAttribute('selected')
    document.querySelector(el2).setAttribute('selected',true);

  };

  $scope.sub = function () {
    var name, sender, surname, error;
    name = document.querySelector('#namesus');
    sender = document.querySelector('#sendersus');
    surname = document.querySelector('#surnamesus');
    error = document.querySelector('#invalid');

    error.innerHTML = '';
    if (!name.value) {
      error.innerHTML = "* El nombre es obligatorio";
    }

    if (!surname.value) {
      if (error.innerHTML) {
        error.innerHTML +='<br>';
      }
      error.innerHTML += "* El apellido es obligatorio";
    }

    if (!sender.value || !sender.checkValidity()) {
      if (error.innerHTML) {
        error.innerHTML +='<br>';
      }
      error.innerHTML += "* El correo debe ser valido"
    }

    if (name.value && sender.checkValidity() && surname.value) {
      var peticion, uri, params;
      peticion = new XMLHttpRequest();
      uri = 'http://test-frontend.example-project-13.appspot.com' + '/api/subscriptions';
      params = "name=" + name.value + "&email=" + sender.value + "&surname=" + surname.value;

      peticion.open("POST", uri, true);
      peticion.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      peticion.onreadystatechange = function () {
        if (peticion.readyState === 4 && (peticion.status === 201)) {
          console.log('[INFO]: Todo fue bien');
          name.value='';
          sender.value='';
          surname.value='';
          $scope.$apply(function () { 
            $scope.$parent.shadow = true;
            $scope.$parent.sended = true;
          });

        } else if (peticion.readyState === 4 && (peticion.status === 200)) {
          error.innerHTML="* Ya esta registrado para la beta";
          name.value='';
          sender.value='';
          surname.value='';
        } else if (peticion.readyState === 4 && !(peticion.status === 200 || peticion.status === 201)) {
          console.log("[INFO]: Error al introducir datos en backend",peticion);
        }
      };
      peticion.send(params);
    }
  };


  $scope.wheel = function(e) {
    $scope.$apply(function () {
      e.preventDefault();
      document.onmousewheel = '';
      var scrolled;
      e.wheelDelta<0 ? scrolled=1 : scrolled=-1;
      /* Section 1*/
      if ($scope.selected===1 && e.wheelDelta<0) {
        $scope.selected +=scrolled;
        $scope.cambiarAnchor('section2'); 
        /* Section 2*/
      } else if ($scope.selected === 2) {
        $scope.selected +=scrolled

        $scope.cambiarAnchor('section'+$scope.selected); 

        /* Section 3*/
      } else if ($scope.selected === 3) {
        $scope.selected += scrolled;
        $scope.cambiarAnchor('section'+$scope.selected);
      } else if ($scope.selected === 4 && e.wheelDelta > 0) {
        $scope.selected +=scrolled;
        $scope.cambiarAnchor('section3');
      };
      document.onmousewheel = $scope.wheel;
    });
  };

  document.onmousewheel = $scope.wheel;

  $scope.closeSended = function() {
      $scope.$parent.shadow = false;
      $scope.$parent.sended = false;
      $scope.setSelected(1);
  };
  $scope.setSelected = function(sel){
    $scope.selected = sel;
    $scope.cambiarAnchor("section"+sel);
  };

  $scope.isSelected = function(sel) {
    return $scope.selected === sel; 
  }
});