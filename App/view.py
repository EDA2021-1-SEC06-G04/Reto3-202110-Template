"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as mp
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

contextContentFeatures_file = 'context_content_features-small.csv'
usertrackhashtagtimestamp_file = 'user_track_hashtag_timestamp-small.csv'
sentimentvalues_file = 'sentiment_values.csv'

def initCatalog():
    """
    Inicializa el Catálogo
    """
    return controller.initCatalog()



def printMenu():
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Consultar cuántas reproducciones están en el sistema de recomendación basado en una característica de contenido y un rango determinado")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")

cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando catálogo ....")
        cont = initCatalog()

    elif int(inputs[0]) == 2:
        print("Cargando información del catálogo ....")
        controller.loadData(cont)
        
        cantidad_total_reps = controller.loadData(cont)
        cantidad_artistas_unicos = lt.size(mp.keySet(cont['Artistas_Unicos']))
        cantidad_pistas_unicas = lt.size((mp.keySet(cont['Pistas_Unicas'])))
        print("El total de registros de eventos de escucha cargados fue de: "+ str(cantidad_total_reps))
        print("El total de artistas únicos cargados fue de: " + str(cantidad_artistas_unicos))
        print("El total de pistas de audio únicas cargadas fue de: "+ str(cantidad_pistas_unicas))

    elif int(inputs[0]) == 3:
        print("OPCIÓN 3:")
        caracteristica = input('¿Para cuál característica de contenido desea obtener información?\n')
        altura = om.height(cont['RepsPor_{}'.format(caracteristica)])
        elementos = om.size(cont['RepsPor_{}'.format(caracteristica)])
        print("Cantidad de elementos en el árbol: "+str(elementos))
        print("Altura del arbol: " + str(altura))


    else:
        sys.exit(0)
sys.exit(0)
