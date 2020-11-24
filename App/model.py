"""
 * Copyright 2020, Departamento de sistemas y Computación
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
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newAnalyzer():
    """ Inicializa el analizador

   stations: Tabla de hash para guardar los vertices del grafo
   graph: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {'stationsStart': None,
                'stationsEnd': None,
                'graph': None,
                'bikes':None
                    }

    analyzer['stationsEnd'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)

    analyzer['stationsStart'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareStations)
                                
    analyzer['bikes'] = m.newMap(numelements=2000,
                                     maptype='PROBING',
                                     comparefunction=compareBikes)

    analyzer['graph'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=10000,
                                              comparefunction=compareStations)
    return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')



# Funciones para agregar informacion al grafo

def addNewTrip(analyzer, service):
    
    
    try:
        origen = service["start station id"]
        destino = service["end station id"]
        duracion = int(service["tripduration"])

        addStop(analyzer, origen)
        addStop(analyzer, destino)

        addConnection(analyzer, origen, destino, duracion)

        addTripEnd(analyzer, service)
        addTripStart(analyzer, service)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addBike(analyzer, service):
    entry = m.get(analyzer['bikes'], service["bikeid"])
    if entry is None:
        infoBike={"cuantosViajes":1, "id":service["bikeid"],"tiempoUso": int(service["tripduration"]) , "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips) }
        lt.addLast(infoBike["viajes"], service)
        m.put(analyzer['bikes'], service["bikeid"], infoBike)
    else:
        infoBike = entry['value']
        if infoBike["id"]==service["bikeid"]:
            infoBike["cuantosViajes"]+=1
            infoBike["tiempoUso"]+= int(service["tripduration"])
            lt.addLast(infoBike["viajes"],service)

def addStop(analyzer, estacion):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], estacion):
            gr.insertVertex(analyzer['graph'], estacion)
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addTripStart(analyzer, service):
    entry = m.get(analyzer['stationsStart'], service["start station id"])
    if entry is None:
        edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
        infoViaje={"cuantosViajes":1, "nombre":service["start station name"], "latitud":service["start station latitude"], 
            "longitud":service["start station longitude"],"edades": edades, "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips) }
        lt.addLast(infoViaje["viajes"],service)
        if 2020-int(service["birth year"]) >=0 and 2020-int(service["birth year"]) <= 10:
            infoViaje["edades"]["0-10"] += 1
        elif 2020-int(service["birth year"]) >=11 and 2020-int(service["birth year"]) <= 20:
            infoViaje["edades"]["11-20"] += 1
        elif 2020-int(service["birth year"]) >=21 and 2020-int(service["birth year"]) <= 30:
            infoViaje["edades"]["21-30"] += 1
        elif 2020-int(service["birth year"]) >=31 and 2020-int(service["birth year"]) <= 40:
            infoViaje["edades"]["31-40"] += 1
        elif 2020-int(service["birth year"]) >=41 and 2020-int(service["birth year"]) <= 50:
            infoViaje["edades"]["41-50"] += 1
        elif 2020-int(service["birth year"]) >=51 and 2020-int(service["birth year"]) <= 60:
            infoViaje["edades"]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            infoViaje["edades"]["60+"] += 1
        m.put(analyzer['stationsStart'], service["start station id"], infoViaje)
    else:
        infoViaje = entry['value']
        if entry['key']==service['start station id']:
            infoViaje["cuantosViajes"]+=1
            lt.addLast(infoViaje["viajes"],service)
            if 2020-int(service["birth year"]) >=0 and 2020-int(service["birth year"]) <= 10:
                infoViaje["edades"]["0-10"] += 1
            elif 2020-int(service["birth year"]) >=11 and 2020-int(service["birth year"]) <= 20:
                infoViaje["edades"]["11-20"] += 1
            elif 2020-int(service["birth year"]) >=21 and 2020-int(service["birth year"]) <= 30:
                infoViaje["edades"]["21-30"] += 1
            elif 2020-int(service["birth year"]) >=31 and 2020-int(service["birth year"]) <= 40:
                infoViaje["edades"]["31-40"] += 1
            elif 2020-int(service["birth year"]) >=41 and 2020-int(service["birth year"]) <= 50:
                infoViaje["edades"]["41-50"] += 1
            elif 2020-int(service["birth year"]) >=51 and 2020-int(service["birth year"]) <= 60:
                infoViaje["edades"]["51-60"] += 1
            elif 2020-int(route["birth year"]) >60:
                infoViaje["edades"]["60+"] += 1

    return analyzer

def addTripEnd(analyzer, service):
    entry = m.get(analyzer['stationsEnd'], service["end station id"])
    if entry is None:
        edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
        infoViaje={"cuantosViajes":1, "nombre":service["end station name"], "latitud":service["end station latitude"], 
            "longitud":service["end station longitude"],"edades": edades, "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips) }
        lt.addLast(infoViaje["viajes"],service)
        if 2020-int(service["birth year"]) >=0 and 2020-int(service["birth year"]) <= 10:
            infoViaje["edades"]["0-10"] += 1
        elif 2020-int(service["birth year"]) >=11 and 2020-int(service["birth year"]) <= 20:
            infoViaje["edades"]["11-20"] += 1
        elif 2020-int(service["birth year"]) >=21 and 2020-int(service["birth year"]) <= 30:
            infoViaje["edades"]["21-30"] += 1
        elif 2020-int(service["birth year"]) >=31 and 2020-int(service["birth year"]) <= 40:
            infoViaje["edades"]["31-40"] += 1
        elif 2020-int(service["birth year"]) >=41 and 2020-int(service["birth year"]) <= 50:
            infoViaje["edades"]["41-50"] += 1
        elif 2020-int(service["birth year"]) >=51 and 2020-int(service["birth year"]) <= 60:
            infoViaje["edades"]["51-60"] += 1
        elif 2020-int(route["birth year"]) >60:
            infoViaje["edades"]["60+"] += 1
        m.put(analyzer['stationsEnd'], service["end station id"], infoViaje)
    else:
        infoViaje = entry['value']
        if entry['key']==service["end station id"]:
            infoViaje["cuantosViajes"]+=1
            lt.addLast(infoViaje["viajes"],service)
            if 2020-int(service["birth year"]) >=0 and 2020-int(service["birth year"]) <= 10:
                infoViaje["edades"]["0-10"] += 1
            elif 2020-int(service["birth year"]) >=11 and 2020-int(service["birth year"]) <= 20:
                infoViaje["edades"]["11-20"] += 1
            elif 2020-int(service["birth year"]) >=21 and 2020-int(service["birth year"]) <= 30:
                infoViaje["edades"]["21-30"] += 1
            elif 2020-int(service["birth year"]) >=31 and 2020-int(service["birth year"]) <= 40:
                infoViaje["edades"]["31-40"] += 1
            elif 2020-int(service["birth year"]) >=41 and 2020-int(service["birth year"]) <= 50:
                infoViaje["edades"]["41-50"] += 1
            elif 2020-int(service["birth year"]) >=51 and 2020-int(service["birth year"]) <= 60:
                infoViaje["edades"]["51-60"] += 1
            elif 2020-int(route["birth year"]) >60:
                infoViaje["edades"]["60+"] += 1

    return analyzer

def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer["graph"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["graph"], origin, destination, duration)
    else:
        ed.updateAverageWeight(edge, duration) 
    return analyzer

# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(sc, station1, station2):
    return scc.stronglyConnected(sc, station1, station2)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])

# ==============================
# Funciones Helper
# ==============================


# ==============================
# Funciones de Comparacion
# ==============================

def compareStations(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

def compareTrips(trip1, trip2):
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1