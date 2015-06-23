# -*- coding: utf8 -*-

# Script para hacer pruebas a la API de Componentes de PicBit (api/componentes)
# Uso: ./api_componentes_tester

# PRE-TEST 1: Hacer login en el sistema mediante googleplus


# TEST 1: Obtener la lista de componentes. Debe retornar una lista vacia de componentes
# Status esperado: 204 

# TEST 2: Subir un componente al sistema, proporcionando una uri incorrecta.
# Status esperado: 404

# TEST 3: Subir un componente al sistema, proporcionando un parametro erroneo.
# Status esperado: 400

# Subimos dos componentes al sistema
# TEST 4: Subir un componente al sistema (componente 1).
# Status esperado: 200

# TEST 5: Subir un componente al sistema (componente 2).
# Status esperado: 200

# TEST 6: Obtener la lista de componentes, sin proporcionar una cookie de sesion
# Status esperado: 401

# TEST 7 : Obtener la lista de componentes, proporcionando una cookie de sesion
# Status esperado: 200


# POST-TEST 1: Hacer logout en el sistema mediante googleplus