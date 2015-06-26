angular.module('picbit').controller('ContactController', function ($scope, $backend) {
  'use strict';


  $scope.sendEmail = function () {
    var message, sender, subject, error;
    message = document.querySelector('#message');
    sender = document.querySelector('#sender');
    subject = document.querySelector('#subject');
    error = document.querySelector('#invalid');

    error.innerHTML = '';
    if (!message.value) {
      error.innerHTML = "*El mensaje no debe estar vacio";
    }

    if (!sender.value || !sender.checkValidity()) {
      error.innerHTML += "<br>*El email debe ser válido";
    }
    if (message.value && sender.checkValidity() && sender.value) {

      var callback = function () {
        message.value = '';
        sender.value = '';
        subject.value = '';
      }
      $backend.sendEmail(message.value, sender.value, subject.value, callback);
    }
  };
});