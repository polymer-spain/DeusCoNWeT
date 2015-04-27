angular.module('picbit').controller('contactCtrl', function ($scope, $backend) {
  'use strict';

  $scope.sendEmail = function () {
    var message = document.querySelector('#message');
    var sender = document.querySelector('#sender');
    var subject = document.querySelector('#subject');
    var error = document.querySelector('#invalid');
    error.innerHTML = '';
    if (!message.value) {
      error.innerHTML = "*El mensaje no debe estar vacio";
    }

    if (!sender.value || !sender.checkValidity()) {
      error.innerHTML += "<br>*El email debe ser válido";
    }
    if (message.value && sender.checkValidity() && sender.value) {

      var callback = function () {
        document.querySelector('#message').value = '';
        document.querySelector('#sender').value = '';
        document.querySelector('#subject').value = '';
      }
      $backend.sendEmail(message.value, sender.value, subject.value, callback);
    }
  };
});