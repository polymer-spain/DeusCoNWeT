'user strict'
angular.module('PolymerBricks')
.controller('ProfileCtrl', function ($scope) {
	
	$scope.calC= function()	{	 
	var nombre=document.getElementById("nombre").value;
	var apellido=document.getElementById("apellido").value;
	var mail=document.getElementById("email").value;	
	var dia=document.getElementById("day").value;
	var month=document.getElementById("month").value;
	var year=document.getElementById("year").value;
	var descr=document.getElementById("descr").value;	
	var sex=document.getElementById("sexo").value;	
		console.log(nombre);
		console.log(apellido);
		console.log(mail);
		console.log(dia);
		console.log(month);
		console.log(year);
		console.log(descr);
		
		
	if(sex==1){
	console.log("Mujer");	
		sex="Mujer";	
	}
		
	if(sex==2){
	console.log("Hombre");	
		sex="Hombre";
	}
	if(sex==3){
	console.log("Otros");	
		sex="Otros";
	}

		
    };
	
	  $scope.takeInfoLog = function(e){
		  
		  if (e.detail.redSocial === 'googleplus') {
			  var googleplus="googleplus";
   			  console.log("googleplus");
			  document.getElementById("google").status = '';
			  
		  }
		  if (e.detail.redSocial === 'facebook') {
			  var facebook="facebook";
   			  console.log("facebook");
  
		  }
		  if (e.detail.redSocial === 'github') {
				var github="github";
   				console.log("github");
  
		  }
		  if (e.detail.redSocial === 'linkedin') {
				var linkedin="linkedin";
   				console.log("linkedin");
  
		  }
		  if (e.detail.redSocial === 'instagram') {
				var instagram="instagram"
   				console.log("instagram");
  
		  }
		  if (e.detail.redSocial === 'twitter') {
				var twitter="twitter";
   				console.log("twitter");
  
		  }
	
		  };
	
	
  document.getElementById("pr").addEventListener('google-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('facebook-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('linkedin-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('github-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('instagram-logged',$scope.takeInfoLog);
  document.getElementById("pr").addEventListener('twitter-logged',$scope.takeInfoLog);

	
	 
	
})

