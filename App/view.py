﻿"""
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
from DISClib.DataStructures import mapentry as me
from datetime import datetime
from datetime import time
import time
import tracemalloc
assert cf

#----------------------------------------------------------------------------------
#FUNCIONES PARA CALCULAR EL TIEMPO DE EJECUCIÓN Y MEMORIA
def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
#---------------------------------------------------------------------------------------------------
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

def printR4(info_generos, total_reproducciones):
    print('-----------------------------------------------------------------------')
    print('El total reproducciones entre los generos consultados es: {}'.format(total_reproducciones))
    print('-----------------------------------------------------------------------')
    for genero in lt.iterator(mp.keySet(info_generos)):

        info_del_genero = me.getValue(mp.get(info_generos, genero))
        tamaño_genero = info_del_genero[0]
        artistas_genero = info_del_genero[1]
        cantidad_artistas = lt.size(artistas_genero)
        print('-----------------------------------------------------------------------')
        print('El genero {} tiene {} distintas reproducciones y {} distintos artistas.'.format(genero, tamaño_genero, cantidad_artistas))
        
        print('Diez artistas del genero {} son:'.format(genero))
        contador = 0
        for artista in lt.iterator(artistas_genero):
            print('Artista {} : {}'.format(contador + 1,artista))
            contador = contador + 1
            if contador == 10:
                break
        print('-----------------------------------------------------------------------')
    print('-----------------------------------------------------------------------')
        


def printMenu():
    print("-----------------------------------------------------------------------")
    print("Bienvenido")
    print("1- Inicializar catálogo")
    print("2- Cargar información en el catálogo")
    print("3- Consultar reproducciones en el sistema de recomendación para una característica y rango")
    print("4- Encontrar música para festejar")
    print("5- Encontrar música para estudiar")
    print("6- Estudiar los géneros musicales")
    print("7- Indicar el género musical más escuchado en un rango de horas")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    #Inicializa el catálogo
    if int(inputs[0]) == 1:
        print("Inicializando catálogo ....")
        catalog = initCatalog()

    #CARGA
    elif int(inputs[0]) == 2:
        print("")
        print("Cargando información del catálogo ....")
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
        controller.loadData(catalog)
        cantidad_total_reps = controller.loadData(catalog)
        cantidad_artistas_unicos = lt.size(mp.keySet(catalog['Artistas_Unicos']))
        cantidad_pistas_unicas = lt.size((mp.keySet(catalog['Pistas_Unicas'])))
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        print("------------------------------------------------------------")
        print("Registros de eventos de escucha cargados: "+ str(cantidad_total_reps))
        print("Artistas únicos cargados: " + str(cantidad_artistas_unicos))
        print("Pistas de audio únicas cargadas: "+ str(cantidad_pistas_unicas))
        print("------------------------------------------------------------")
        

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        print('Tiempo [ms]: {}'.format(delta_time))
        print('Memoria [kB]: {}'.format(delta_memory))
        #PRUEBAS:----
        #primer_hashtag = lt.firstElement(mp.keySet(catalog['Hashtags']))
        #print(primer_hashtag)
        #print(me.getValue(mp.get(catalog['Hashtags'], primer_hashtag)))
        #primera_hora = datetime.strptime('3:40:00', '%H:%M:%S')
        #segunda_hora = datetime.strptime('13:40:00', '%H:%M:%S')
        #print(lt.firstElement(om.values(catalog['RepsPor_hora'], primera_hora, segunda_hora)))

        #PRUEBAS HASTA AQUI ----
    


    #---------------------------------------------------------------------------------------------
    #REQ 1
    elif int(inputs[0]) == 3:
        print("")
        caracteristica = input('¿Para cuál característica de contenido desea obtener información?\n')
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
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
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        print("------------------------------------------------------------")
        print('Cantidad de reproducciones: {}'.format(cantidad_reps))
        print('Número de artistas únicos: {}'.format(num_artistas))
        print("------------------------------------------------------------")
        print('Tiempo [ms]: {}'.format(delta_time))
        print('Memoria [kB]: {}'.format(delta_memory))
        print("------------------------------------------------------------")



    #----------------------------------------------------------------------------------------
    #REQ 2
    elif int(inputs[0])==4:
        print("")
        minE = float(input('Ingresa el mínimo valor de Energy:\n'))
        minD = float(input('Ingresa el mínimo valor de Danceability:\n'))
        maxE = float(input('Ingresa el máximo valor de Energy:\n'))
        maxD = float(input('Ingresa el máximo valor de Danceability:\n'))
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
        resultado = controller.musicaParaFestejar(catalog, minD, maxD, minE, maxE)
        cantidad = resultado[0]
        stack_cinco_tracks = resultado[1]
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        print('-------------------------------------------------------------')
        print('Buscando pistas con Energy entre {} y {}, y Danceability entre {} y {}:'.format(minE,maxE,minD,maxD))
        print('Se encontraron {} pistas.'.format(cantidad))
        print('5 pistas :')
        if not stk.isEmpty(stack_cinco_tracks):
            for i in range(5):
                pista = stk.pop(stack_cinco_tracks)
                tid = pista['track_id']
                aid = pista['artist_id']
                d = pista['danceability']
                e = pista['energy']
                print('Track ID: {}, Artist ID: {}, Danceability: {}, Energy: {}'.format(tid, aid, d, e))
            print('-------------------------------------------------------------')
            print('Tiempo [ms]: {}'.format(delta_time))
            print('Memoria [kB]: {}'.format(delta_memory))
        else:
            print('No hay pistas.')
        print("------------------------------------------------------------")

    


    #----------------------------------------------------------------------------------
    #REQ3
    elif int(inputs[0])==5:
        print("")
        minI = float(input('Ingresa el mínimo valor de Instrumentalness:\n'))
        minT = float(input('Ingresa el mínimo valor de Tempo:\n'))
        maxI = float(input('Ingresa el máximo valor de Instrumentallness:\n'))
        maxT = float(input('Ingresa el máximo valor de Tempo:\n'))
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
        resultado = controller.musicaParaEstudiar(catalog, minI, maxI, minT, maxT)
        cantidad_pistas = resultado[0]
        cinco_pistas_supuestamente_aleatorias = resultado[1]
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        print('-------------------------------------------------------------')
        print('Buscando pistas con Instrumentalness entre {} y {}, y Tempo entre {} y {}...'.format(minI,maxI,minT,maxT))
        print('Se encontraron {} pistas.'.format(cantidad_pistas))
        print('5 pistas :')
        if not stk.isEmpty(cinco_pistas_supuestamente_aleatorias):
            for i in range(5):
                pista = stk.pop(cinco_pistas_supuestamente_aleatorias)
                tid = pista['track_id']
                aid = pista['artist_id']
                I = pista['instrumentalness']
                t = pista['tempo']
                print('Track ID: {}, Artist ID: {}, Instrumentalness: {}, Tempo: {}'.format(tid, aid, I, t))
                print('-------------------------------------------------------------')
        else:
            print('No hay pistas.')
        #-------------------------------
        print('Tiempo [ms]: {}'.format(delta_time))
        print('Memoria [kB]: {}'.format(delta_memory))
        print("------------------------------------------------------------")



    #---------------------------------------------------------------------------------------
    #REQ4
    elif int(inputs[0])==6:
        print("")
        #agregar genero se hace con la funcion en controller llamada nuevo_genero
        print('Antes de escoger los generos a consultar, ¿Deseas definir un genero nuevo?')
        print('Presiona: 1 para agregar genero o 0 para continuar.')
        decision = input('')
        while decision == '1':
            
            nombre_genero_nuevo = str(input('Introduce el nombre del genero nuevo: \n'))
            lim_inf = float(input('Introduce el limite inferior de bpm del genero nuevo: \n'))
            lim_sup = float(input('Introduce el limite superior de bpm del genero nuevo: \n'))
            controller.nuevo_genero(catalog, nombre_genero_nuevo, lim_inf, lim_sup)
            print('Presiona: 1 para agregar genero o 0 para continuar.')
            decision = input('')
        generos_a_correr = lt.newList('ARRAY_LIST')
        for genero_preguntar in lt.iterator(mp.keySet(catalog['Generos'])):
            print('¿Deseas incluir el genero {}?'.format(genero_preguntar))
            incluido = input('Presiona: 1 para consultar este genero o 0 para continuar.\n')
            if incluido == '1':
                lt.addLast(generos_a_correr, genero_preguntar)
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
        respuesta_cruda = controller.req4(catalog, generos_a_correr)
        total_reproducciones = respuesta_cruda[1]
        info_generos = respuesta_cruda[0]
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        printR4(info_generos, total_reproducciones)
        #--------------------------------
        print('Tiempo [ms]: {}'.format(delta_time))
        print('Memoria [kB]: {}'.format(delta_memory))
        print("------------------------------------------------------------")


    #REQ5
    elif int(inputs[0])==7:
        print("")
        print('Indique la hora mínima que quiera consultar: \n')
        hora_min = input('PORFAVOR USA EL FORMATO h:m:s\n')
        print('Indique la hora máxima que quiera consultar: \n')
        hora_max = input('PORFAVOR USA EL FORMATO h:m:s\n')
        #--------------------------------
        delta_time = -1.0
        delta_memory = -1.0

        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        #--------------------------------
        generos_ordenPorReps, tracks, num_tracks_maxGenero = controller.generoMasEscuchadoEnTiempo(catalog, hora_min, hora_max)
        #--------------------------------
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()

        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        #--------------------------------
        print('---------------------Generos ordenados por reproducciones------------------------')
        contador = 0
        for tupla in lt.iterator(generos_ordenPorReps):
            genero = tupla[0]
            num_reps_genero = tupla[1]
            print('Top {} genero: {} , {} reproducciones.'.format(contador+1, genero, num_reps_genero))
            contador = contador + 1
            if contador == 10:
                break
        print("------------------------------------------------------------ \n")
        maxgenero, max_reps = lt.firstElement(generos_ordenPorReps)
        print("El género más escuchado entre las {} y las {} fue: {} con {} reproducciones.".format(hora_min, hora_max, maxgenero, max_reps))

        print('--------------------{} Análisis Sentimental-----------------------'.format(maxgenero))
        print('{} tiene {} tracks distintos.'.format(maxgenero, num_tracks_maxGenero))
        print('Las top 10 tracks del genero son:')
        contador = 0
        for tupla in lt.iterator(tracks):
            numero_ht_track, vader_track, track = tupla
            print('Top {} track: {}, {} hashtags, vader promedio = {} '.format(contador+1, track, numero_ht_track, vader_track))
            contador = contador + 1
            if contador == 10:
                break

        #--------------------------------
        print('Tiempo [ms]: {}'.format(delta_time))
        print('Memoria [kB]: {}'.format(delta_memory))
        print("------------------------------------------------------------")


        
#continuar
        # correr un for sobre los generos (llaves de el mapa catalog['Generos'])
        # para cada uno preguntar si lo quiere incluir o no , el print se puede hacer con format



    else:
        sys.exit(0)
sys.exit(0)
