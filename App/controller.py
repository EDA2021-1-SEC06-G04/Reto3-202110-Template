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
 """

import config as cf
import model
import csv


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
    loadContextContent(catalog)
    loadUserTrackHashtag(catalog)
    #---------------------------------------------------------------------
def loadSentimentValues(catalog):
    return None

def loadContextContent(catalog):
    file = cf.data_dir + 'videos-large.csv'
    input_file = csv.DictReader(open(file, encoding='utf-8'))
#    contador_datos = 0
    for rep_leida in input_file:
        rep_agregar = {}
        info_numerica = ['instrumentalness','liveness', 'speechiness', 'danceability', \
             'valence', 'loudness', 'tempo', 'acousticness', 'energy']
        info_deseada_ids = ['artist_id', 'track_id', 'artist_id', 'id']
        for info in info_deseada_ids:
            rep_agregar[info] = int(rep_leida[info])
        for info in info_numerica:
            rep_agregar[info] = float(rep_leido[info])
        
        

    #    rep_agregar['created_at'] = datetime.strptime(rep_leida['created_at'], '%y.%d.%m').date()
        
    #    rep_agregar['tags'] = lt.newList('ARRAY_LIST')
    #    for tag in rep_leida['tags'].split('"|"'):
    #        tag.replace('"','')
    #        lt.addLast(rep_agregar['tags'], tag)

        model.addRep(catalog, rep_agregar)
#        contador_datos += 1
#        if contador_datos >= size_datos:
#            break

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
