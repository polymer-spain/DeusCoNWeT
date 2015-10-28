#!/bin/sh

# Script para añadir usuarios a la datastore en local
# Uso: ./feed_usuarios.sh prueba_usuarios.txt

while read linea; do
curl --data $linea http://localhost:8080/usuarios
echo "Haciendo petición POST a http://localhost:8080/usuarios"
done < $1
