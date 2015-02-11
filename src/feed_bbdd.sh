#!/bin/sh 
while read linea; do
curl --data $linea http://localhost:8080/componentes
echo "Haciendo petición POST a http://localhost:8080/componentes"
done < $1
