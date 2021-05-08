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
    # es decir: esto es un mapa/hashTable donde una llave es un genero(nombre del genero) y su valor es una tupla:
    # 1: una tupla de los limites del rango 2. la lista de reproducciones que segun su tempo/bpm corresponden a ese genero
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
    catalog['Reproducciones_totales'] = mp.newMap(loadfactor=4.0)
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    # REQ 5:
    catalog['RepsPor_hora'] = om.newMap(omaptype='RBT', comparefunction=MAPCompararHoras)
    return catalog
    
# Funciones para agregar informacion al catalogo

def addRep(catalog, reproduccion):
    #req1(req2 tambien usa la estructura de danceability cargada aqui):
    carga_req1(catalog, reproduccion)
    #requisitos carga:
    guardar_artista_unico(catalog, reproduccion)
    guardar_pista_unica(catalog, reproduccion)
    #req4:
    mp.put(catalog['Reproducciones_totales'], reproduccion['id'], reproduccion)

def addHashtag_rep(catalog, reproduccion):
    rbt = catalog['RepsPor_hora']
    archivo_1 = catalog['Reproducciones_totales']
    hora = reproduccion['hora']
    #estoe atributo de la rep en realidad es un solo hashtag por ahora
    hashtag = reproduccion['hashtags']
    r_id = reproduccion['id']
    if not om.contains(rbt, hora):
        mapa_reps = mp.newMap(loadfactor=4.0)
        lista_hashtags = lt.newList('ARRAY_LIST')
        lt.addLast(lista_hashtags, hashtag)
        #ahora si lo volvemos una lista de hashtags
        reproduccion['hashtags'] = lista_hashtags
        if mp.contains(archivo_1, r_id):
            reproduccion['tempo'] = me.getValue(mp.get(archivo_1, r_id))['tempo']
            mp.put(mapa_reps, r_id, reproduccion)
# IMPORTANTE:
# ESTE ELSE SE PUEDE BORRAR
# todo depende de como interpretamos el archivo 2 y lo que son las reproducciones
# hacer el else es decir que esto es una rep que no tiene valor tempo porque no aparece en el archivo 1
# NO hacer el else (no hacer nada(no agregar la 'rep') en else) es decir que esto NO es una rep valida existente porque no aparece en el archivo 1
        else:
            reproduccion['tempo'] = -1
            mp.put(mapa_reps, r_id, reproduccion)

        om.put(rbt, hora, mapa_reps)
    else:
        mapa_reps = me.getValue(om.get(rbt, hora))
        if not mp.contains(mapa_reps, r_id):
            lista_hashtags = lt.newList('ARRAY_LIST')
            lt.addLast(lista_hashtags, hashtag)
            #ahora si lo volvemos una lista de hashtags
            reproduccion['hashtags'] = lista_hashtags

            if mp.contains(archivo_1, r_id):
                reproduccion['tempo'] = me.getValue(mp.get(archivo_1, r_id))['tempo']
                mp.put(mapa_reps, r_id, reproduccion)
# IMPORTANTE:
# ESTE ELSE SE PUEDE BORRAR
# todo depende de como interpretamos el archivo 2 y lo que son las reproducciones
# hacer el else es decir que esto es una rep que no tiene valor tempo porque no aparece en el archivo 1
# NO hacer el else (no hacer nada(no agregar la 'rep') en else) es decir que esto NO es una rep valida existente porque no aparece en el archivo 1            
            else:
                reproduccion['tempo'] = -1
                mp.put(mapa_reps, r_id, reproduccion)
        else:
            rep = me.getValue(mp.get(mapa_reps, r_id))
            lt.addLast(rep['hashtags'], reproduccion['hashtags'])




        




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
        # esto se hace por req2
        if caracteristica=='danceability':
            agregar = {'id': rep['id'], 'artist_id': rep['artist_id'], 'danceability': rep['danceability']
            , 'energy': rep['energy'], 'track_id': rep['track_id']}
        #esto se hace por req3
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
    agregado = False
    for nombre_genero in lt.iterator(generos_a_correr):
        rango_lista = me.getValue(mp.get(mapa_generos, nombre_genero))
        rango = rango_lista[0]
        inf = rango[0]
        sup = rango[1]
        #asumimos que los rangos de los generos son inclusivos
        if inf <= tempo and tempo <= sup:
            lista = rango_lista[1]
            lt.addLast(lista, rep)
            agregado = True
    
    return agregado



# Funciones para creacion de datos



# Funciones de consulta
#-------------------------------------------------------------------------------------------
#REQ1


def numeroReps_y_ArtistasUnicos(catalog, caracteristica, valor_min, valor_max):
    lista_listas = om.values(catalog["RepsPor_{}".format(caracteristica)], valor_min, valor_max)
    mapa = mp.newMap(loadfactor=4.0)
#    numeroReps = 0
    mapa2 = mp.newMap(loadfactor=4.0)
    for lista in lt.iterator(lista_listas):
#        numeroReps = numeroReps + lt.size(lista)
        for rep in lt.iterator(lista):
            llave = rep['artist_id']
            llave2 = rep['id']
#            if not mp.contains(mapa, llave):
            mp.put(mapa, llave, rep)
#            if not mp.contains(mapa2, llave2):
            mp.put(mapa2, llave2, rep)
    num_artistas = mp.size(mapa)
    return num_artistas, mp.size(mapa2)

 

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
#            print(rep)
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
            listaPistasTempo = lt.newList(datastructure='ARRAY_LIST')
            lt.addLast(listaPistasTempo, pista)
            om.put(om_pistas_tempo, llave, listaPistasTempo)
        else:
            listaPistasTempo = me.getValue(om.get(om_pistas_tempo, llave))
            lt.addLast(listaPistasTempo, pista)
    
    return om_pistas_tempo

def PistasRangoTempo(oM_pistas_tempo, minTempo, maxTempo):
    return om.values(oM_pistas_tempo, minTempo, maxTempo)



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

def MAPCompararHoras(keyname, category):
    keyname = (keyname)
    cat_entry = (category)
    if (keyname == cat_entry):
        return 0
    elif (keyname > cat_entry):
        return 1
    else:
        return -1

# Funciones de ordenamiento
