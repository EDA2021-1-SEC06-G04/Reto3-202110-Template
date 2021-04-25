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
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo

    Retorna el catálogo inicializado.
    """
    catalog = {'RepsPorInstrumentalness': None,
                }
    
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    #Carga:
    catalog['Artistas_Unicos'] = mp.newMap(loadfactor=4.0)
    catalog['Pistas_Unicas'] = mp.newMap(loadfactor=4.0)
    #-----------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------
    #Req1:
    
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
    return catalog
    
# Funciones para agregar informacion al catalogo

def addRep(catalog, reproduccion):
    carga_req1(catalog, reproduccion)
    guardar_artista_unico(catalog, reproduccion)
    guardar_pista_unica(catalog, reproduccion)

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
        lt.addLast(nueva_lista, {'id': rep['id'], 'artist_id': rep['artist_id']})
        om.put(mapa, llave, nueva_lista)
    else:
        lista_existente = me.getValue(om.get(mapa, llave))
        lt.addLast(lista_existente, {'id': rep['id'], 'artist_id': rep['artist_id']})



# Funciones para creacion de datos



# Funciones de consulta
def caracterizarReproducciones(catalog, caracteristica, valor_min, valor_max):
    mapa = catalog["RepsPor_{}".format(caracteristica)]
    contador = 0
    lista_caracteristica_rango = lt.newList(datastructure='ARRAY_LIST')


def repsPor_Rango_danceability(mapa_ordenado, minDance, maxDance):
    return om.values(mapa_ordenado, minDance, maxDance)

def ListReps_to_HashPistasUnicas(lista_reps):
    hashTable = mp.newMap(maptype='PROBING')
    for reproduccion in lt.iterator(lista_reps):
        valor_agregar = {'artist_id': reproduccion['artist_id'], 'energy':reproduccion['energy']
        , 'danceability': reproduccion['danceability']}
        mp.put(hashTable, reproduccion['track_id'], valor_agregar)
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
