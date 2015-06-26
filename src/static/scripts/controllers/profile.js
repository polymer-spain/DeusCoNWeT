'user strict'
angular.module('picbit')

  .controller('ProfileController', function ($scope) {
  $scope.calC= function()	{
    var nombre=document.getElementById("nombre").value;
    var apellido=document.getElementById("apellido").value;
    var mail=document.getElementById("sender").value;	
  };

  $scope.takeInfoLog = function(e){

    if (e.detail.redSocial === 'googleplus') {
      var googleplus="googleplus";
      var acToken=e.detail.token;
    }

    if (e.detail.redSocial === 'facebook') {
      var facebook="facebook";
      var acToken=e.detail.token;
      var userId=e.detail.userId;
    }

    if (e.detail.redSocial === 'github') {
      var github="github";
      var acToken=e.detail.token;
    }

    if (e.detail.redSocial === 'linkedin') {
      var linkedin="linkedin";
      var acToken=e.detail.token;
      var userId=e.detail.userId;
    }

    if (e.detail.redSocial === 'instagram') {
      var instagram="instagram"
      var acToken=e.detail.token;
      var userId=e.detail.userId;
    }

    if (e.detail.redSocial === 'twitter') {
      var twitter="twitter";
      var acToken=e.detail.token;
    }

  };

	$scope.sort = true

  /*  document.getElementById("pr").addEventListener('facebook-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('linkedin-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('github-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('instagram-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('twitter-logged',$scope.takeInfoLog);
  */
})
