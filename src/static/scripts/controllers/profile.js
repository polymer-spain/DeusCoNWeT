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

		
    }
	
	
	 
	
})

