'use strict';

/**
 * @ngdoc function
 * @name pruebaApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the pruebaApp
 */

angular.module('PolymerBricks')
  .controller('MainCtrl', function ($scope, $location, $timeout) {
  $scope.status = false;

  $scope.logged = function(e){
    $scope.$apply(function(){


      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
      if (e.detail.redSocial === 'twitter'){
        $location.path('/user/'+e.detail.redSocial+'_'+e.detail.userId);
      }
      else if (e.detail.redSocial === 'googleplus') { // Comprobamos si es google para buscar el id

        var xhr = new XMLHttpRequest();
        var uri = 'https://www.googleapis.com/plus/v1/people/me?access_token='+e.detail.token;
        xhr.open("GET",uri,true);
        xhr.onreadystatechange = function() {
          if (xhr.readyState == 4 && xhr.status === 200){
            $scope.$apply(function(){
              var response = JSON.parse(xhr.responseText);
              $location.path('/user/'+e.detail.redSocial+'_'+response.id);
              $scope.sendData(e.detail.token,response.id,e.detail.redSocial);
            });
          } else if (xhr.readyState == 4) {
            console.log("[INFO]: Algo fue mal en google");
          }
        }
        xhr.send();
      } else {// mandamos los datos si ya los tenemos
        $location.path('/user/'+e.detail.redSocial+'_'+e.detail.userId);
        $scope.sendData(e.detail.token,e.detail.userId,e.detail.redSocial);
      }
      // cambiamos el botton
      var button = document.querySelector('#nameId');
      // Selecionar el nombre del usuario
      button.innerHTML="Desconectar"
      // Seleccionar la imagen del perfin
      // button.src=""
      // Cambiamos a la funcion de logout
      $scope.status = true;
    });
  };


  $scope.sendData = function(token,tokenId,redSocial){
    var xhr = new XMLHttpRequest();
    var uri = 'http://example-project-13.appspot.com/api/oauth/'+redSocial;   
    var params = "token_id="+token+"&access_token="+tokenId;
    xhr.open("POST",uri,true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && !(xhr.status === 200 || xhr.status === 201))
        console.log("[INFO]: Error al introducir datos en backend");
    };
    xhr.send(params); 
  }

  $scope.changeView = function(view){
    $location.path(view); // path not hash
  };

  $scope.logout = function() {
    var button = document.querySelector('#nameId');
    // Selecionar el nombre del usuario
    button.innerHTML="Entrar"
    $location.path('/');
    $scope.status = false;
  }
  /* Escuhas de los botones*/
  document.querySelector('body').addEventListener('google-logged',$scope.logged);
  document.querySelector('body').addEventListener('linkedin-logged',$scope.logged);
  document.querySelector('body').addEventListener('github-logged',$scope.logged);
  document.querySelector('body').addEventListener('instagram-logged',$scope.logged);
  document.querySelector('body').addEventListener('twitter-logged',$scope.logged);
  document.querySelector('body').addEventListener('facebook-logged',$scope.logged);
  document.querySelector('body').addEventListener('sof-logged',$scope.logged);

  $scope.popup = false;

  $scope.showPopup = function(){
    if (!$scope.status)
      $scope.popup = true;
    else 
      $scope.logout();
  };
  $scope.hidePopup = function(){
    $scope.popup = false;
  };
  
  $scope.sendSub = function() {
    var message = document.querySelector('#message');
    var sender = document.querySelector('#sender');
    var subject = document.querySelector('#subject');
    var error = document.querySelector('#invalid');
    error.innerHTML = '';
    if (!message.value) {
      error.innerHTML="*El mensaje no debe estar vacio" 
    }

    if (!sender.value || !sender.checkValidity() ) {
      error.innerHTML+="<br>*El email debe ser válido" 
    } 
    if (message.value && sender.checkValidity() && sender.value) {
      var xhr = new XMLHttpRequest();
      var uri = 'http://example-project-13.appspot.com/api/contact';   
      var params = "action=contact&message="+message.value+"&sender="+sender.value;

      if (subject.value !== undefined) {
        params += "&subject="+subject.value; 
      }

      xhr.open("POST",uri,true);
      xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
      xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && (xhr.status === 200) ){
          console.log('[INFO]: Todo fue bien');
          message.value = '';
          sender.value = '';
          subject.value = '';
        }
        if (xhr.readyState == 4 && !(xhr.status === 200 || xhr.status === 201))
          console.log("[INFO]: Error al introducir datos en backend");
      };
      xhr.send(params); 
    }
  }

});
