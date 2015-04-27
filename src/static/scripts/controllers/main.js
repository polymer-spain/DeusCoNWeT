angular.module('PolymerBricks').controller('MainCtrl', function ($scope, $location, $timeout, $http) {
  'use strict';



  $scope.status = false;
  $scope.domain = 'http://' + $location.host();
  $scope.logged = function (e) {
    $scope.$apply(function () {

      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
      if (e.detail.redSocial === 'twitter') {
        $scope.changeView('/user/' + e.detail.redSocial + '_' + e.detail.userId);
      } else if (e.detail.redSocial === 'googleplus') { // Comprobamos si es google para buscar el id
        var uri, button;
        uri = 'https://www.googleapis.com/plus/v1/people/me?access_token=' + e.detail.token;
        $http.get(uri).success(function (data) {
            $scope.changeView('/user/' + e.detail.redSocial + '_' + data.id);
            $scope.sendData(e.detail.token, data.id, e.detail.redSocial);
        }).error(function () {
          console.error("Error al contactar con google");               
        });
      } else {
        $scope.changeView('/user/' + e.detail.redSocial + '_' + e.detail.userId);
        $scope.sendData(e.detail.token, e.detail.userId, e.detail.redSocial);
      }
      // cambiamos el botton
      $scope.logOutButton();

    });
  };
  $scope.logOutButton = function() {
    var button = document.querySelector('#nameId');
    button.innerHTML = "Desconectar";
    // Seleccionar la imagen del perfin
    // button.src=""
    // Cambiamos a la funcion de logout
    $scope.status = true;

  };

  $scope.sendData = function (token, tokenId, redSocial) {
    var request, uri, params;
    uri = $scope.domain + '/api/oauth/' + redSocial;    
    params = "token_id=" + tokenId + "&access_token=" + token + "&action=login";
    request = {
      method:"post",
      url: uri, 
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      data: params
    }
    $http(request).error(function (data,status) {
      console.error('Error:' + status ': no se enviaron datos al backend'); 
    });

  };

  $scope.changeView = function (view) {
    $location.hash('');
    $location.path(view); // path not hash
  };

  $scope.logout = function () {
    var button = document.querySelector('#nameId');
    // Selecionar el nombre del usuario
    button.innerHTML = "Entrar";
    $scope.changeView('/');
    $scope.status = false;
  };
  /* Escuhas de los botones*/
  document.querySelector('body').addEventListener('google-logged', $scope.logged);
  document.querySelector('body').addEventListener('linkedin-logged', $scope.logged);
  document.querySelector('body').addEventListener('github-logged', $scope.logged);
  document.querySelector('body').addEventListener('instagram-logged', $scope.logged);
  document.querySelector('body').addEventListener('twitter-logged', $scope.logged);
  document.querySelector('body').addEventListener('facebook-logged', $scope.logged);
  document.querySelector('body').addEventListener('sof-logged', $scope.logged);

  $scope.popup = false;

  $scope.showPopup = function () {
    if (!$scope.status) {
      $scope.popup = true;
    } else {
      $scope.logout();
    }
  };
  $scope.hidePopup = function () {
    $scope.popup = false;
  };

  $scope.sendSub = function () {
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
      var uri, request;
      uri = $scope.domain+'/api/contact';
      request = {
        method:"post",
        url: uri, 
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        data: params
      };

      $http(request).succes(function () {
        console.info('Todo fue bien');
        message.value = '';
        sender.value = '';
        subject.value = '';
      }).error( function () {
        console.error("Error al introducir datos en backend");
      });
    };
  };
});
