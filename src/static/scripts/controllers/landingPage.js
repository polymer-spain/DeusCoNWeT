/*global angular, document */
angular.module("picbit").controller("LandingController", ["$scope", "$timeout", "$location", "$anchorSmoothScroll", "$anchorScroll", "$backend", function ($scope, $timeout, $location, $anchorSmoothScroll, $anchorScroll, $backend) {
  "use strict";
  if ($location.hash() === "section1") {
    $scope.selected = 1;
  } else if ($location.hash() === "section2") {
    $scope.selected = 2;
  } else if ($location.hash() === "section3") {
    $scope.selected = 3;
  } else if ($location.hash() === "section4") {
    $scope.selected = 4;
  } else {
    $scope.selected = 1;
  }

  $scope.cambiarAnchor = function (section) {
    $location.hash(section);
    $anchorSmoothScroll.scrollTo(section);
  };
  $scope.goto = function (section) {
    $scope.selected = section;
    $location.hash("section" + section);
    $anchorScroll();
  };
  $scope.setStyle = function (el, el2) {
    document.querySelector(el).removeAttribute("selected");
    document.querySelector(el2).setAttribute("selected", true);

  };

  $scope.sub = function () {
    var name, sender, surname, error;
    name = document.querySelector("#namesus");
    sender = document.querySelector("#sendersus");
    surname = document.querySelector("#surnamesus");
    error = document.querySelector("#invalid");

    error.innerHTML = "";
    if (!name.value) {
      error.innerHTML = "* El nombre es obligatorio";
    }

    if (!surname.value) {
      if (error.innerHTML) {
        error.innerHTML += "<br>";
      }
      error.innerHTML += "* El apellido es obligatorio";
    }

    if (!sender.value || !sender.checkValidity()) {
      if (error.innerHTML) {
        error.innerHTML += "<br>";
      }
      error.innerHTML += "* El correo debe ser valido";
    }

    if (name.value && sender.checkValidity() && surname.value) {
      var callback, callbackError;

      callback = function (data, status) {
        if (status === 201) {
          name.value = "";
          sender.value = "";
          surname.value = "";

          $scope.$parent.shadow = true;
          $scope.$parent.sended = true;

        } else if (status === 200) {
          error.innerHTML = "* Ya esta registrado para la beta";
          name.value = "";
          sender.value = "";
          surname.value = "";
        }
      };
      callbackError = function () {
        error.innerHTML = "* Ahora mismo no podemos tratar su petición, intentelo mas tarde";
      };
      $backend.sendSub(name.value, sender.value, surname.value, callback, callbackError);

    }
  };


  $scope.wheel = function (e) {
    document.onmousewheel = "";
    $scope.$apply(function () {
      e.preventDefault();
      var scrolled;
      scrolled = e.wheelDelta < 0 ? 1 : -1;
      /* Section 1*/
      if ($scope.selected === 1 && e.wheelDelta < 0) {
        $scope.selected += scrolled;
        $scope.cambiarAnchor("section2");
        /* Section 2*/
      } else if ($scope.selected === 2) {
        $scope.selected += scrolled;

        $scope.cambiarAnchor("section" + $scope.selected);

        /* Section 3*/
      } else if ($scope.selected === 3) {
        $scope.selected += scrolled;
        $scope.cambiarAnchor("section" + $scope.selected);
      } else if ($scope.selected === 4 && e.wheelDelta > 0) {
        $scope.selected += scrolled;
        $scope.cambiarAnchor("section3");
      }

      document.onmousewheel = $scope.wheel;

    });
  };
  /*document.onmousewheel = $scope.wheel;*/

  $scope.closeSended = function () {
    $scope.$parent.shadow = false;
    $scope.$parent.sended = false;
    $scope.goto(1);
  };
  $scope.setSelected = function (sel) {
    $scope.selected = sel;
    $scope.cambiarAnchor("section" + sel);
  };

  $scope.isSelected = function (sel) {
    return $scope.selected === sel;
  };
}]);
