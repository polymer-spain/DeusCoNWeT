angular.module('PolymerBricks')
  .controller('contactCtrl', function ($scope,$http) {
  'use strict';

  $scope.sendEmail = function(action,message,sender,subject){
    var xhr = new XMLHttpRequest();
    var uri = 'http://example-project-13.appspot.com/api/contact;   
    var params = "action="+action+"&message="+message+"&sender="+sender;
    if (subject !== undefined) {
      params += "subject="+subject; 
    }

    xhr.open("POST",uri,true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    xhr.onreadystatechange = function() {
      if (xhr.responseText == 4 && (xhr.status === 200) ){
        console.log('[INFO]: Todo fue bien'); 
      }
      if (xhr.readyState == 4 && !(xhr.status === 200 || xhr.status === 201))
        console.log("[INFO]: Error al introducir datos en backend");
    };
    xhr.send(params); 
  }
});