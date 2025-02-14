﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
from random import sample
from random import randint
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import stack as stk
from DISClib.DataStructures import mapentry as me
from datetime import datetime
from datetime import time

contextContentFeatures_file = 'context_content_features-small.csv'
usertrackhashtagtimestamp_file = 'user_track_hashtag_timestamp-small.csv'
sentimentvalues_file = 'sentiment_values.csv'
"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de datos
def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos
def loadData(catalog):
    #---------------------------------------------------------------------
    loadSentimentValues(catalog)
    total_reps = loadContextContent(catalog)
    loadUserTrackHashtag(catalog)
    #---------------------------------------------------------------------
    return total_reps


def loadSentimentValues(catalog):
    file = cf.data_dir + sentimentvalues_file
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for hashtag_leido in input_file:
        hashtag_agregar = {'hashtag': hashtag_leido['hashtag'].lower()}
        if hashtag_leido['vader_avg'] == '':
            hashtag_agregar['vader'] = -1
        else:
            hashtag_agregar['vader'] = float(hashtag_leido['vader_avg'])
        

        model.addHashtag(catalog, hashtag_agregar)
        

#-------------------------------------------------------------------------------------------
#Carga para req 5
def loadUserTrackHashtag(catalog):
    file = cf.data_dir + usertrackhashtagtimestamp_file
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    for hashtag_rep_leido in input_file:
        rep_agregar = {}
        track_id = str(hashtag_rep_leido['track_id'])
        user_id = str(hashtag_rep_leido['user_id'])
        fecha = datetime.strptime(hashtag_rep_leido['created_at'], '%Y-%m-%d %H:%M:%S')
        rep_agregar['hora'] = datetime.strptime(hashtag_rep_leido['created_at'].split(' ')[1], '%H:%M:%S')
        rep_agregar['hashtags'] = hashtag_rep_leido['hashtag'].lower()
        rep_agregar['id'] = (user_id, track_id, fecha)

        model.addHashtag_rep(catalog, rep_agregar)
    return None

#-------------------------------------------------------------------------------------------
#Carga archivo principal
def loadContextContent(catalog):
    file = cf.data_dir + contextContentFeatures_file
    input_file = csv.DictReader(open(file, encoding='utf-8'))
    contador_datos = 0
    for rep_leida in input_file:
        rep_agregar = {}
        info_numerica = ['instrumentalness','liveness', 'speechiness', 'danceability', \
             'valence', 'loudness', 'tempo', 'acousticness', 'energy']
        info_deseada_ids = ['artist_id', 'track_id', 'user_id', 'id']
        for info in info_deseada_ids:
            rep_agregar[info] = str(rep_leida[info])
        for info in info_numerica:
            rep_agregar[info] = float(rep_leida[info])
    #    rep_agregar['created_at'] = datetime.strptime(rep_leida['created_at'], '%y.%d.%m').date()
        rep_agregar['created_at'] = datetime.strptime(rep_leida['created_at'], '%Y-%m-%d %H:%M:%S')
        rep_agregar['hora'] = datetime.strptime(rep_leida['created_at'].split(' ')[1], '%H:%M:%S')
        rep_agregar['id'] = (rep_agregar['user_id'],rep_agregar['track_id'], rep_agregar['created_at'])
    #    rep_agregar['tags'] = lt.newList('ARRAY_LIST')
    #    for tag in rep_leida['tags'].split('"|"'):
    #        tag.replace('"','')
    #        lt.addLast(rep_agregar['tags'], tag)

        model.addRep(catalog, rep_agregar)
        contador_datos += 1
#        if contador_datos >= size_datos:
#            break

    return contador_datos



# Funciones de consulta sobre el catálogo
#--------------------------------------------------------------------------------------------------
#REQ1
def caracterizarReproducciones(catalog, caracteristica, valor_min, valor_max):
    #comentarios en model linea 186
    num_artistas, cantidad_reps = model.numeroReps_y_ArtistasUnicos(catalog, caracteristica, valor_min, valor_max)
    return cantidad_reps, num_artistas


#--------------------------------------------------------------------------------------------------
#REQ2
def musicaParaFestejar(catalog, minDance, maxDance, minEnergy, maxEnergy):
    #mapa ordenado : llaves= dance de la rep, valor: reproducciones con ese dance
    mapa_inicial = catalog['RepsPor_danceability']
    #lista de todas las reproducciones cuyo dance está en el rango parametro||||
    # ||||| por esto, de aqui en adelante todo está dentro del rango de Danceability
    #esto es una lista de las listas de reps por cada valor de danceability
    repsEn_Rango_danceability = model.repsPor_Rango_danceability(mapa_inicial, minDance, maxDance)
    #map/hashtable de PISTAS con id de pista/track_id como llaves, valor: artist_id, danceability, energy
    pistasEn_Rango_danceability = model.ListReps_to_HashPistasUnicas(repsEn_Rango_danceability)
    #se convierte a lista
    pistasEn_Rango_danceability = mp.valueSet(pistasEn_Rango_danceability)
    # se convierte a un mapa ordenado por Energy : llave=ValorEnergy, Valor=listadePistas con ese valor de energy
    Om_pistasEn_Rango_danceability = model.ListPistas_to_OMPistas_porEnergy(pistasEn_Rango_danceability)
    #se obtienen las que tienen el energy en el rango:
    lista_resultado = model.PistasPor_Rango_energy(Om_pistasEn_Rango_danceability, minEnergy, maxEnergy)
    cantidad = 0
    retornar = stk.newStack()

    
    for pistasConEnergy in lt.iterator(lista_resultado):
        cantidad = cantidad + lt.size(pistasConEnergy)
        '''if stk.size(retornar) < 5 and :
            for track in lt.iterator(pistasConEnergy):
                if stk.size(retornar) < 5:
                    stk.push(retornar, track)'''

    aleatorios_1 = sample(range(1,lt.size(lista_resultado)), 5)
    for pos1 in aleatorios_1:
        lista = lt.getElement(lista_resultado, pos1)
        pos2 = randint(1, lt.size(lista))
        elemento = lt.getElement(lista, pos2)
        stk.push(retornar, elemento)
    return cantidad, retornar
#---------------------------------------------------------------------------------------------
#REQ3
def musicaParaEstudiar(catalog, minInstrumental, maxInstrumental, minTempo, maxTempo):
    mapa = catalog['RepsPor_instrumentalness']
    Reproducciones_Rango_Instrumentalness = model.Reproducciones_Rango_Instrumentalness(mapa, minInstrumental, maxInstrumental)
    lista_pistas = model.Lista_unicas_Instrumentalness(Reproducciones_Rango_Instrumentalness)
    #Obtenemos la lista
    lista_pistas = mp.valueSet(lista_pistas)
    #Organizamos por tempo con mapa
    om_pistas_tempo = model.OM_pistas_tempo(lista_pistas)
    lista_resultado = model.PistasRangoTempo(om_pistas_tempo, minTempo, maxTempo)
    cantidad = 0
    retornar = stk.newStack()
    
    for lista in lt.iterator(lista_resultado):
        cantidad = cantidad + lt.size(lista)
        

    aleatorios_1 = sample(range(1,lt.size(lista_resultado)), 5)
    for pos1 in aleatorios_1:
        lista = lt.getElement(lista_resultado, pos1)
        pos2 = randint(1, lt.size(lista))
        elemento = lt.getElement(lista, pos2)
        stk.push(retornar, elemento)
    return cantidad, retornar
#-------------------------------------------------------------------------------------------------
#REQ4 
#a:
def nuevo_genero(catalog, nombre:str, lim_inf:float, lim_sup:float):
    generos = catalog['Generos']
    valor_de_genero_nuevo = ((lim_inf,lim_sup), lt.newList(datastructure='ARRAY_LIST'))
    mp.put(generos, nombre, valor_de_genero_nuevo)

#b:
def req4(catalog, lista_generos):
    #la lista que entra como parametro puede ser de ceros y unos viniendo del view para minimizar implementacion
    # en el view y pasar la informacion binaria a una lista real de generos aqui
    Reproducciones_totales = mp.valueSet(catalog['Reproducciones_totales'])
    
    total_reproducciones_generos = 0
    for reproduccion in lt.iterator(Reproducciones_totales):
        agregado = model.carga_req4(catalog, reproduccion, lista_generos)
        if agregado:
            total_reproducciones_generos = total_reproducciones_generos + 1
    
    mapa_respuesta = mp.newMap(loadfactor=4.0)
    for genero in lt.iterator(lista_generos):
        reps_del_genero= me.getValue(mp.get(catalog['Generos'], genero))[1]
        tamaño_genero = lt.size(reps_del_genero)
        
        artistas_genero = mp.newMap(loadfactor=4.0)
        for rep in lt.iterator(reps_del_genero):
            mp.put(artistas_genero, rep['artist_id'], rep['artist_id'])
        
        mp.put(mapa_respuesta, genero, (tamaño_genero, mp.valueSet(artistas_genero)))
    return mapa_respuesta, total_reproducciones_generos
        
#----------------------------------------------------------------------------------------------
#REQ5
def generoMasEscuchadoEnTiempo(catalog, hora_min, hora_max):

    hora_min = datetime.strptime(hora_min, '%H:%M:%S')
    hora_max = datetime.strptime(hora_max, '%H:%M:%S')

    #hay que ver en que formato entran las horas para ver si es necesario transformarlas antes de empezar a ejecutar
    lista_mapas_reps = om.values(catalog['RepsPor_hora'], hora_min, hora_max)

    #esto es una lista de tuplas (genero, cantidad_reps_genero) ORDENADA por cantidad_reps_genero
    generos_ordenados_por_reps = model.Reps_genero_en_horario(catalog, lista_mapas_reps)

    max_genero = lt.firstElement(generos_ordenados_por_reps)[0]
    
    unique_tracks = model.unique_tracks(catalog, max_genero, lista_mapas_reps)
    model.calculo_vaders_tracks(unique_tracks)
    unique_tracks = mp.valueSet(unique_tracks)
    #aqui quedan ordenados los tracks por numero de hashtags
    model.Ordenar_tracks_por_hashtags(unique_tracks)

    '''for track in lt.iterator(unique_tracks):
        if track[0]>4:
            print(track[0])'''

    #esto puede borrarse y pasar la informacion de otra forma
    cantidad_track_max_genero = lt.size(unique_tracks)

    return generos_ordenados_por_reps, unique_tracks, cantidad_track_max_genero

    



    

