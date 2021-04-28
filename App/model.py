"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo

    Retorna el catálogo inicializado.
    """
    catalog = {'RepsPor_instrumentalness': None,
                }
    
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    #Carga:
    catalog['Artistas_Unicos'] = mp.newMap(loadfactor=4.0)
    catalog['Pistas_Unicas'] = mp.newMap(loadfactor=4.0)
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    #Req1:
    #por cada caracteristica se hace un mapa ordenado que tiene los valores de la caracteristica como llaves y a la lista de 
    # las reproducciones con el valor correspondiente a la caracteristica
    catalog['RepsPor_instrumentalness'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_liveness'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_speechiness'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_energy'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_acousticness'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_danceability'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    catalog['RepsPor_valence'] = om.newMap(omaptype='RBT',
                                      comparefunction=MAPcompareDecimals)
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    #Req 4
    #Generos: Aqui se guardaran las reproducciones partidas por generos:
    # es decir: esto es un mapa/hashTable donde una llave es un genero(para ser preciso es una tupla de nombre y limites) y su valor es la lista de reproducciones 
    #que segun su tempo/bpm corresponden a ese genero
    #OJO una MISMA EXACTA REPRODUCCION puede estar en la lista de distintos generos porque puede pertenecer a mas de un genero a la vez
    generos = mp.newMap(loadfactor=4.0)
    mp.put(generos, 'Reggae', ((60,90),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Down-Tempo', ((70,100),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Chill-Out', ((90,120),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Hip-Hop', ((85,115),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Jazz and Funk', ((120,125),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Pop', ((100,130),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'R&B', ((60,80),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Rock', ((110,140),lt.newList(datastructure='ARRAY_LIST')))
    mp.put(generos, 'Metal', ((100,160),lt.newList(datastructure='ARRAY_LIST')))
    catalog['Generos'] = generos

    #reproducciones totales:
    catalog['Reproducciones_totales'] = lt.newList(datastructure='ARRAY_LIST')
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    return catalog
    
# Funciones para agregar informacion al catalogo

def addRep(catalog, reproduccion):
    #req1(req2 tambien usa la estructura de danceability cargada aqui):
    carga_req1(catalog, reproduccion)
    #requisitos carga:
    guardar_artista_unico(catalog, reproduccion)
    guardar_pista_unica(catalog, reproduccion)
    #req4:
    lt.addLast(catalog['Reproducciones_totales'], reproduccion)


def guardar_artista_unico(catalog, rep):
    mapa = catalog['Artistas_Unicos']
    artista = rep['artist_id']
    mp.put(mapa, artista, artista)

def guardar_pista_unica(catalog, rep):
    mapa = catalog['Pistas_Unicas']
    track = rep['track_id']
    mp.put(mapa, track, track)

def carga_req1(catalog, rep):
    caracteristicas = ['instrumentalness','liveness', 'speechiness', 'danceability', \
             'valence', 'acousticness', 'energy']
    for caracteristica in caracteristicas:
        addRep_a_mapaReq1(catalog, caracteristica, rep)


def addRep_a_mapaReq1(catalog, caracteristica, rep):
    mapa = catalog['RepsPor_{}'.format(caracteristica)]
    llave = rep[caracteristica]
    if not om.contains(mapa, llave):
        nueva_lista = lt.newList(datastructure='ARRAY_LIST')
        agregar = {'id': rep['id'], 'artist_id': rep['artist_id']}
        if caracteristica=='danceability':
            agregar = {'id': rep['id'], 'artist_id': rep['artist_id'], 'danceability': rep['danceability']
            , 'energy': rep['energy'], 'track_id': rep['track_id']}
        if caracteristica=="instrumentalness":
            agregar = {'id': rep['id'], 'artist_id': rep['artist_id'], 'instrumentalness': rep['instrumentalness']
            , 'tempo': rep['tempo'], 'track_id': rep['track_id']}
        lt.addLast(nueva_lista, agregar)
        om.put(mapa, llave, nueva_lista)
    else:
        lista_existente = me.getValue(om.get(mapa, llave))
        agregar = {'id': rep['id'], 'artist_id': rep['artist_id']}
        if caracteristica=='danceability':
            agregar = {'id': rep['id'], 'artist_id': rep['artist_id'], 'danceability': rep['danceability']
            , 'energy': rep['energy'], 'track_id': rep['track_id']}
        if caracteristica=="instrumentalness":
            agregar = {'id': rep['id'], 'artist_id': rep['artist_id'], 'instrumentalness': rep['instrumentalness']
            , 'tempo': rep['tempo'], 'track_id': rep['track_id']}
        lt.addLast(lista_existente, agregar)

def carga_req4(catalog, rep, generos_a_correr):
    mapa_generos = catalog['Generos']
    tempo = rep['tempo']
    for nombre_genero in lt.iterator(generos_a_correr):
        rango_lista = me.getValue(mp.get(mapa_generos, nombre_genero))
        rango = rango_lista[0]
        inf = rango[0]
        sup = rango[1]
        #asumimos que los rangos de los generos son inclusivos
        if inf <= tempo and tempo <= sup:
            lista = rango_lista[1]
            lt.addLast(lista, rep)



# Funciones para creacion de datos



# Funciones de consulta
#-------------------------------------------------------------------------------------------
#REQ1
def caracterizarReproducciones(catalog, caracteristica, valor_min, valor_max):
    lista = om.values(catalog["RepsPor_{}".format(caracteristica)], valor_min, valor_max)
    return lt.size(lista)

def numeroArtistasUnicos(catalog, caracteristica, valor_min, valor_max):
    lista_listas = om.values(catalog["RepsPor_{}".format(caracteristica)], valor_min, valor_max)
    mapa = mp.newMap(loadfactor=4.0)
    for lista in lt.iterator(lista_listas):
        for rep in lt.iterator(lista):
            llave = rep['artist_id']
            if not mp.contains(mapa, llave):
                mp.put(mapa, llave, rep)
    num_artistas = mp.valueSet(mapa)
    return lt.size(num_artistas)

#comentarios: 
#1. seria mas eficiente juntarlos en una sola funcion porque la linea 173 y 177 son iguales, esa info se puede retornar como una tupla 
# en una sola funcion

#2. no veo necesario el uso de un ordered map, creo que con map se puede(y son mas eficientes)
        
def num_artistas(catalog, caracteristica, valor_min, valor_max):
    OM = mp.newMap(maptype='CHAINING', comparefunction=MAPcompareDecimals)
    
    
    
    

#--------------------------------------------------------------------------------------------

#REQ2
def repsPor_Rango_danceability(mapa_ordenado, minDance, maxDance):
    #esto retorna una lista de las listas de reps por cada valor de danceability
    return om.values(mapa_ordenado, minDance, maxDance)

def ListReps_to_HashPistasUnicas(lista_listas_reps):
    hashTable = mp.newMap(maptype='PROBING')
    for lista_reps in lt.iterator(lista_listas_reps):
        for reproduccion in lt.iterator(lista_reps):
            track_id = reproduccion['track_id']
            valor_agregar = {'artist_id': reproduccion['artist_id'], 'energy':reproduccion['energy']
            , 'danceability': reproduccion['danceability'], 'track_id': track_id}
            mp.put(hashTable, track_id, valor_agregar)
    return hashTable


def ListPistas_to_OMPistas_porEnergy(lista_pistas):
    #las llaves son valores de energy
    #los valores NO SON PISTAS, son listas de pistas con ese valor de energy
    OMpistasPorEnergy = om.newMap(omaptype='RBT', comparefunction=MAPcompareDecimals)
    for pista in lt.iterator(lista_pistas):
        llave = pista['energy']
        if not om.contains(OMpistasPorEnergy, llave):
            lista_pistas_con_energy = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(lista_pistas_con_energy, pista)
            om.put(OMpistasPorEnergy, llave, lista_pistas_con_energy)
        else: 
            lista_pistas_con_energy = me.getValue(om.get(OMpistasPorEnergy, llave))
            lt.addLast(lista_pistas_con_energy, pista)
    return OMpistasPorEnergy

def PistasPor_Rango_energy(mapa_ordenado, minEnergy, maxEnergy):
    return om.values(mapa_ordenado, minEnergy, maxEnergy)



#---------------------------------------------------------------------------------------------------


#REQ3
def Reproducciones_Rango_Instrumentalness(mapa, minInstrumental, maxInstrumental):
    return om.values(mapa, minInstrumental, maxInstrumental)

def Lista_unicas_Instrumentalness(Reproducciones_Rango_Instrumentalness):
    nuevo_mapa = mp.newMap(maptype='PROBING')
    for lista_reps in lt.iterator(Reproducciones_Rango_Instrumentalness):
        for rep in lt.iterator(lista_reps):
            print("ESTOY ACA")
            track_id = rep['track_id']
            track = {'artist_id': rep['artist_id'], 'tempo':rep['tempo']
            , 'instrumentalness': rep['instrumentalness'], 'track_id': track_id}
            mp.put(nuevo_mapa, track_id, track)
    return nuevo_mapa

def OM_pistas_tempo(lista_pistas):
    om_pistas_tempo = om.newMap(omaptype='RBT',comparefunction=MAPcompareDecimals)
    for pista in lt.iterator(lista_pistas):
        llave = pista['tempo']
        if not om.contains(om_pistas_tempo, llave):
            listaPistasTempo = lt.newList(type= 'ARRAY')
            lt.addLast(listaPistasTempo, pista)
            om.put(om_pistas_tempo, llave, listaPistasTempo)
        else:
            listaPistasTempo = me.getValue(mp.get(om_pistas_tempo, llave))
            lt.addLast(listaPistasTempo, pista)
    
    return om_pistas_tempo

def PistasRangoTempo(OM_pistas_tempo, minTempo, maxTempo):
    return om.values(OM_pistas_tempo, minTempo, maxTempo)



#-----------------------------------------------------------------------------------------

# Funciones utilizadas para comparar elementos dentro de una lista

def MAPcompareDecimals(keyname, category):
    keyname = float(keyname)
    cat_entry = float(category)
    if (keyname == cat_entry):
        return 0
    elif (keyname > cat_entry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
