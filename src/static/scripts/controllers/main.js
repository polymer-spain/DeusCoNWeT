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
	$scope.status1 = true;
  $scope.logged = function(e){
    $scope.$apply(function(){
		


      $scope.hidePopup();// escondemos el popup y cambiamos la direccion del usuario
      if (e.detail.redSocial === 'twitter'){
		  	 if($location.pathname.indexOf("profile")!=0)
		 		return
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
              $scope.sendData(e.detail.token,response.id,e.detail.redSocial);
			  if($location.pathname.indexOf("profile")!=0)
		 		return
		      $location.path('/user/'+e.detail.redSocial+'_'+response.id);              

            });
          } else if (xhr.readyState == 4) {
            console.log("[INFO]: Algo fue mal en google");
          }
        }
        xhr.send();
      } else {// mandamos los datos si ya los tenemos
          $scope.sendData(e.detail.token,e.detail.userId,e.detail.redSocial);
		  	  if($location.pathname.indexOf("profile")!=0)
		 		return
          $location.path('/user/'+e.detail.redSocial+'_'+e.detail.userId);
      }
      // cambiamos el botton
      var button = document.querySelector('#nameId');
      // Selecionar el nombre del usuario
      button.innerHTML="Desconectar"
      // Seleccionar la imagen del perfin
      // button.src=""
      // Cambiamos a la funcion de logout
      $scope.status = true;
		$scope.status1 = false;
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
	  $scope.status1 = true;
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

});
