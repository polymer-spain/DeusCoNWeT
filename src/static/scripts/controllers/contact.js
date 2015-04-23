angular.module('PolymerBricks').controller('contactCtrl', function ($scope, $http, $modal) {
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
      var xhr, uri, params;
      xhr = new XMLHttpRequest();
      uri = 'http://example-project-13.appspot.com/api/contacts';
      params = "message=" + message.value + "&sender=" + sender.value;

      if (subject.value !== undefined) {
        params += "&subject=" + subject.value;
      }

      xhr.open("POST", uri, true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
      xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && (xhr.status === 201)) {
          console.log('[INFO]: Todo fue bien');
          message.value = '';
          sender.value = '';
          subject.value = '';
        }
        if (xhr.readyState === 4 && !(xhr.status === 200 || xhr.status === 201)) {
          console.log("[INFO]: Error al introducir datos en backend");
        }
      };
      xhr.send(params);
    }
  };
});