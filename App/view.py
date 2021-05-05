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
from DISClib.ADT import stack as stk
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
    print("3- Consultar reproducciones en el sistema de recomendación para una característica y rango")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical más escuchado en el tiempo")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando catálogo ....")
        catalog = initCatalog()

    elif int(inputs[0]) == 2:
        print("")
        print("Cargando información del catálogo ....")
        controller.loadData(catalog)
        cantidad_total_reps = controller.loadData(catalog)
        cantidad_artistas_unicos = lt.size(mp.keySet(catalog['Artistas_Unicos']))
        cantidad_pistas_unicas = lt.size((mp.keySet(catalog['Pistas_Unicas'])))
        print("------------------------------------------------------------")
        print("Registros de eventos de escucha cargados: "+ str(cantidad_total_reps))
        print("Artistas únicos cargados: " + str(cantidad_artistas_unicos))
        print("Pistas de audio únicas cargadas: "+ str(cantidad_pistas_unicas))
        print("------------------------------------------------------------")

    elif int(inputs[0]) == 3:
        print("")
        caracteristica = input('¿Para cuál característica de contenido desea obtener información?\n')
        altura = om.height(catalog['RepsPor_{}'.format(caracteristica)])
        elementos = om.size(catalog['RepsPor_{}'.format(caracteristica)])
        print("------------------------------------------------------------")
        print("Cantidad de elementos en el árbol: "+str(elementos))
        print("Altura del arbol: " + str(altura))
        print("------------------------------------------------------------")
        valor_min = float(input("Escoja valor mínimo para la característica seleccionada: "))
        valor_max = float(input("Escoja valor máximo para la característica seleccionada: "))
        resultado = controller.caracterizarReproducciones(catalog, caracteristica, valor_min, valor_max)
        cantidad_reps = resultado[0]
        num_artistas = resultado[1]
        print('REPS:{}'.format(cantidad_reps))
        print('ARTISTAS:{}'.format(num_artistas))


    elif int(inputs[0])==4:
        print("")
        minE = float(input('Ingresa el mínimo valor de Energy:\n'))
        minD = float(input('Ingresa el mínimo valor de Danceability:\n'))
        maxE = float(input('Ingresa el máximo valor de Energy:\n'))
        maxD = float(input('Ingresa el máximo valor de Danceability:\n'))
        resultado = controller.musicaParaFestejar(catalog, minD, maxD, minE, maxE)
        cantidad = resultado[0]
        stack_cinco_tracks = resultado[1]
        print('-------------------------------------------------------------')
        print('Buscando pistas con Energy entre {} y {}, y Danceability entre {} y {}:'.format(minE,maxE,minD,maxD))
        print('Se encontraron {} pistas.'.format(cantidad))
        print('5 pistas :')
        for i in range(5):
            pista = stk.pop(stack_cinco_tracks)
            tid = pista['track_id']
            aid = pista['artist_id']
            d = pista['danceability']
            e = pista['energy']
            print('Track ID: {}, Artist ID: {}, Danceability: {}, Energy: {}'.format(tid, aid, d, e))

    elif int(inputs[0])==5:
        print("")
        minI = float(input('Ingresa el mínimo valor de Instrumentalness:\n'))
        minT = float(input('Ingresa el mínimo valor de Tempo:\n'))
        maxI = float(input('Ingresa el máximo valor de Instrumentallness:\n'))
        maxT = float(input('Ingresa el máximo valor de Tempo:\n'))
        resultado = controller.musicaParaEstudiar(catalog, minI, maxI, minT, maxT)
        cantidad_pistas = resultado[0]
        cinco_pistas_supuestamente_aleatorias = resultado[1]

    

    elif int(inputs[0])==6:
        print("")
        #agregar genero se hace con la funcion en controller llamada nuevo_genero
        # correr un for sobre los generos (llaves de el mapa catalog['Generos'])
        # para cada uno preguntar si lo quiere incluir o no , el print se puede hacer con format

    elif int(inputs[0])==7:
        print("")



    else:
        sys.exit(0)
sys.exit(0)
