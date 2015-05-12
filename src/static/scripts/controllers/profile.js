'user strict'
angular.module('picbit')

.controller('ProfileCtrl', function ($scope) {
	
	$scope.calC= function()	{
    
	var nombre=document.getElementById("nombre").value;
	var apellido=document.getElementById("apellido").value;
	var mail=document.getElementById("sender").value;	
    var dia=document.getElementById("dia").selectedItemLabel;
    var mes=document.getElementById("mes").selectedItemLabel;
    var ano=document.getElementById("ano").selectedItemLabel;
    var sex=document.getElementById("sex").selectedItemLabel;
		console.log(nombre);
		console.log(apellido);
		console.log(mail);
        console.log(sex);
        console.log(dia);
        console.log(mes);
        console.log(ano);
		
    };
	
	  $scope.takeInfoLog = function(e){
		  
		  if (e.detail.redSocial === 'googleplus') {
			  var googleplus="googleplus";
		  }
		  if (e.detail.redSocial === 'facebook') {
			  var facebook="facebook";
              var acToken=e.detail.token;
              var userId=e.detail.userId;
		  }
		  if (e.detail.redSocial === 'github') {
				var github="github";
   				console.log("github");
//            document.getElementById("google").status = '';
//            document.getElementById("googleitem").style.display="none";
  
		  }
		  if (e.detail.redSocial === 'linkedin') {
				var linkedin="linkedin";
   				console.log("linkedin");
//            document.getElementById("linkedin").status = '';
//            document.getElementById("linkedinitem").style.display="none";
  
		  }
		  if (e.detail.redSocial === 'instagram') {
				var instagram="instagram"
   				console.log("instagram");
//            document.getElementById("instagram").status = '';
//            document.getElementById("instagramitem").style.display="none";
  
		  }
		  if (e.detail.redSocial === 'twitter') {
				var twitter="twitter";
   				console.log("twitter")
//document.getElementById("twitter").status = '';
//document.getElementById("twitteritem").style.display="none";   
 
		  }
	
		  };

  document.getElementById("pr").addEventListener('google-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('facebook-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('linkedin-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('github-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('instagram-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('twitter-logged',$scope.takeInfoLog);




})

