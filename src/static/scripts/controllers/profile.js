'user strict'
angular.module('PolymerBricks')
.controller('ProfileCtrl', function ($scope) {
	
	$scope.redes=[
			{nombre:"F"},
			{nombre:"L"},
			{nombre:"I"} ]
	
	$scope.calC= function()	{	 
	var nombre=document.getElementById("nombre").value;
	var apellido=document.getElementById("apellido").value;
	var mail=document.getElementById("email").value;	
	var dia=document.getElementById("day").value;
	var month=document.getElementById("month").value;
	var year=document.getElementById("year").value;
	var descr=document.getElementById("descr").value;	
		console.log(nombre);
		console.log(apellido);
		console.log(mail);
		console.log(dia);
		console.log(month);
		console.log(year)
		console.log(descr)
		
		var resultado="ninguno";
        
        var porNombre=document.getElementsByName("sex");
        for(var i=0;i<porNombre.length;i++)
        {
            if(porNombre[i].checked)
                resultado=porNombre[i].value;
        }
        
       console.log(resultado);
    }
		

		

	
	 
	
})

