#!/bin/sh


if $1 == "componente"
	then
		while read linea; do
		curl --data $linea http://localhost:8080/componentes
		echo "Haciendo petición POST a http://localhost:8080/componentes"
		done < $1
elif $1 == "usuario" 
	then	
		while read linea; do
		curl --data $linea http://localhost:8080/usuarios
		echo "Haciendo petición POST a http://localhost:8080/usuarios"
		done < $1
fi
