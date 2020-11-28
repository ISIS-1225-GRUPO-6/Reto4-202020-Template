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
from math import radians, cos, sin, asin, sqrt
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
import datetime
from datetime import date
from DISClib.ADT import stack
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
                'bikes':None,
                'components': None,
                'paths': None
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




# Funciones para agregar informacion al grafo

def addNewTrip(analyzer, service):
    try:
        origen = service["start station id"]
        destino = service["end station id"]
        duracion = int(service["tripduration"])

        addStop(analyzer, origen)
        addStop(analyzer, destino)

        addEdge(analyzer, origen, destino, duracion)

        addTripEnd(analyzer, service)
        addTripStart(analyzer, service)

        addBike(analyzer,service)

        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

def addBike(analyzer, service):
    entry = m.get(analyzer['bikes'], service["bikeid"])
    if entry is None:
        infoBike={"cuantosViajes":1, "id":service["bikeid"], "tiempoUso": int(service["tripduration"]) , "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips), "fecha": m.newMap(numelements=2000, maptype='PROBING', comparefunction=compareDates) }
        uptadeDate(infoBike["fecha"],service)
        lt.addLast(infoBike["viajes"], service)
        m.put(analyzer['bikes'], service["bikeid"], infoBike)
    else:
        infoBike = entry['value']
        if infoBike["id"]==service["bikeid"]:
            infoBike["cuantosViajes"]+=1
            infoBike["tiempoUso"]+= int(service["tripduration"])
            lt.addLast(infoBike["viajes"],service)
            uptadeDate(infoBike["fecha"],service)

def uptadeDate(map,service):
    date = service["starttime"]
    serviceDate = datetime.datetime.strptime( date, '%Y-%m-%d %H:%M:%S.%f')
    entry = m.get(map, serviceDate.date())
    if entry is None:
        dia = {"tiempouso":0 , "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips)}
        m.put(map ,serviceDate.date(), dia)  
    else:
        dia = entry['value']
    
    lt.addLast(dia["viajes"], service)
    dia["tiempouso"]+=int(service["tripduration"])
    return map

def addStop(analyzer, estacion):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['graph'], estacion):
            gr.insertVertex(analyzer['graph'], estacion)
        return analyzer

    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addTripStart(analyzer, service):
    entry = m.get(analyzer['stationsStart'], service["start station id"])
    if entry is None:
        edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
        infoViaje={"id": service["start station id"] ,"cuantosViajes":1, "nombre":service["start station name"], "latitud":service["start station latitude"], 
            "longitud":service["start station longitude"],"edades": edades, "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips) ,"subs":0}
        lt.addLast(infoViaje["viajes"],service)
        if(service["usertype"]=="Subscriber"):
            infoViaje["subs"]+=1
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
        elif 2020-int(service["birth year"]) >60:
            infoViaje["edades"]["60+"] += 1
        m.put(analyzer['stationsStart'], service["start station id"], infoViaje)
    else:
        infoViaje = entry['value']
        if entry['key']==service['start station id']:
            infoViaje["cuantosViajes"]+=1
            lt.addLast(infoViaje["viajes"],service)
            if(service["usertype"]=="Subscriber"):
                infoViaje["subs"]+=1
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
            elif 2020-int(service["birth year"]) >60:
                infoViaje["edades"]["60+"] += 1

    return analyzer

def addTripEnd(analyzer, service):
    entry = m.get(analyzer['stationsEnd'], service["end station id"])
    if entry is None:
        edades = {"0-10":0, "11-20":0, "21-30":0, "31-40":0, "41-50":0, "51-60":0, "60+":0}
        infoViaje={"id": service["end station id"], "cuantosViajes":1, "nombre":service["end station name"], "latitud":service["end station latitude"], 
            "longitud":service["end station longitude"],"edades": edades, "viajes": lt.newList("ARRAY_LIST", cmpfunction=compareTrips),"subs":0 }
        lt.addLast(infoViaje["viajes"],service)
        if(service["usertype"]=="Subscriber"):
            infoViaje["subs"]+=1
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
        elif 2020-int(service["birth year"]) >60:
            infoViaje["edades"]["60+"] += 1
        m.put(analyzer['stationsEnd'], service["end station id"], infoViaje)
    else:
        infoViaje = entry['value']
        if entry['key']==service["end station id"]:
            infoViaje["cuantosViajes"]+=1
            lt.addLast(infoViaje["viajes"],service)
            if(service["usertype"]=="Subscriber"):
                infoViaje["subs"]+=1
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
            elif 2020-int(service["birth year"]) >60:
                infoViaje["edades"]["60+"] += 1

    return analyzer

def addEdge(analyzer, origen, destino, duracion):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer["graph"], origen, destino)
    if edge is None:
        gr.addEdge(analyzer["graph"], origen, destino, duracion)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================

def connectedComponents(analyzer):
    """
    req 1
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
    return scc.connectedComponents(analyzer['components'])

def sameCC(analyzer, station1, station2):
    vert1 = gr.containsVertex(analyzer["graph"], station1)
    vert2 = gr.containsVertex(analyzer["graph"], station2)
    if vert1 is False and vert2 is False:
        return "0"
    elif vert1 is False:
        return "1"
    elif vert2 is False:
        return "2"
    else:
        return scc.stronglyConnected(analyzer['components'], station1, station2)

def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['graph'])

def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['graph'])

def rutaCircular(analyzer, estacion, tiempoin, tiempofin):
    
    if m.get(analyzer['stationsStart'],estacion) is not None:
        lista1 = lt.newList("ARRAY_LIST")
        adyacentes = gr.adjacents(analyzer['graph'], estacion)
        connectedComponents(analyzer)
        for h in range (adyacentes['size']):
            adyacente= lt.getElement(adyacentes,h)
            fcc = sameCC(analyzer, estacion, adyacente)
            if fcc:
                tiempo=0
                analyzer['paths'] = dfs.DepthFirstSearch(analyzer["graph"], adyacente)
                caminos = dfs.pathTo(analyzer["paths"], estacion)
                primero= caminos['first']
                siguiente = primero['next']
                for i in range(caminos['size']-1):
                    infoin = primero['info']
                    if siguiente is not None:
                        infoul = siguiente['info']
                        arco = gr.getEdge(analyzer["graph"], infoin, infoul)
                        if arco is not None:
                            tiempo += float(arco["weight"])
                    primero = primero['next']
                    siguiente = siguiente['next']
                suma = float(caminos['size'])*1200
                tiempo+=suma
                lt.addLast(caminos,tiempo)
                lt.addLast(lista1, caminos)

        listafinal= lt.newList("ARRAY_LIST")
        if lista1 is not None:
            tmi = int(tiempoin)*60
            tmf = int(tiempofin)*60
            while (not stack.isEmpty(lista1)):
                parada = stack.pop(lista1)
                if float(parada['last']['info']) >= tmi and float(parada['last']['info']) <= tmf: 
                    lt.addLast(listafinal, parada)     
        print("la cantidad de rutas es : "+ str(listafinal['size']))
        for i in range( listafinal['size'] ):
            actual = lt.getElement(listafinal,i)
            print("ruta no: "+ str(i+1))
            for j in range(actual['size']-1):
                info= m.get(analyzer['stationsStart'], lt.getElement(actual,j))
                print(str(j+1)+". " + info["nombre"])
            print("con una duracion estimada de: "+str(int(actual['last']['info'])/60)+" minutos")   

def rutaresistencia(analyzer, estacion, tiempo):
    
    if m.get(analyzer['stationsStart'],estacion) is not None:
        lista1 = lt.newList("ARRAY_LIST")
        adyacentes = gr.adjacents(analyzer['graph'], estacion)
        connectedComponents(analyzer)
        for h in range (adyacentes['size']):
            adyacente= lt.getElement(adyacentes,h)
            fcc = sameCC(analyzer, estacion, adyacente)
            if fcc:
                tiempo=0
                analyzer['paths'] = bfs.BreadhtFisrtSearch(analyzer["graph"], adyacente)
                caminos = bfs.pathTo(analyzer["paths"], estacion)
                primero= caminos['first']
                siguiente = primero['next']
                for i in range(caminos['size']-1):
                    infoin = primero['info']
                    if siguiente is not None:
                        infoul = siguiente['info']
                        arco = gr.getEdge(analyzer["graph"], infoin, infoul)
                        if arco is not None:
                            tiempo += float(arco["weight"])
                    primero = primero['next']
                    siguiente = siguiente['next']
                lt.addLast(caminos,tiempo)
                lt.addLast(lista1, caminos)

        listafinal= lt.newList("ARRAY_LIST")
        if lista1 is not None:
            tmi = int(tiempo)*60
            while (not stack.isEmpty(lista1)):
                parada = stack.pop(lista1)
                if parada['last']['info'] <= tmi : 
                    lt.addLast(listafinal, parada)     
        print("la cantidad de rutas es : "+ str(listafinal['size']))
        for i in range( listafinal['size'] ):
            actual = lt.getElement(listafinal,i)
            print("ruta no: "+ str(i+1))
            for j in range(actual['size']-1):
                info= m.get(analyzer['stationsStart'], lt.getElement(actual,j))
                print(str(j+1)+". " + info["nombre"])
            print("con una duracion estimada de: "+str(int(actual['last']['info'])/60)+" minutos")   

def estaciones(analyzer):
    "requerimiento 3"
    llaves = m.keySet(analyzer['stationsStart'])
    ite = it.newIterator(llaves)
    mayors1=0
    names1=""
    mayors2=0
    names2=""
    mayors3=0
    names3=""
    
    menos1=50000
    namem1=""
    menos2=0
    namem2=""
    menos3=0
    namem3=""
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual=m.get(analyzer['stationsStart'],info)['value']
        noviaje = int(actual["cuantosViajes"])
        nombre=actual["nombre"]
        ubicado=False
        if noviaje >= mayors1 and ubicado==False:
            mayors3=mayors2
            names3=names2
            mayors2=mayors1
            names2=names1
            mayors1=noviaje
            names1=nombre
            ubicado=True
        elif noviaje >= mayors2 and ubicado==False:
            mayors3=mayors2
            names3=names2
            mayors2=noviaje
            names2=nombre
            ubicado=True
        elif noviaje >= mayors3 and ubicado==False:
            mayors3=noviaje
            names3=nombre
            ubicado=True

        act = m.get(analyzer['stationsEnd'],actual["id"])['value']
        cuantos=noviaje+int(act["cuantosViajes"])
        ubicado1=False
        if cuantos <= menos1 and ubicado1==False:
            menoss3=menos2
            namem3=namem2
            menos2=menos1
            namem2=namem1
            menos1=cuantos
            namem1=nombre
            ubicado1=True
        elif cuantos <= menos2 and ubicado1==False:
            menoss3=menos2
            namem3=namem2
            menos2=cuantos
            namem2=nombre
            ubicado1=True
        elif cuantos <= menos3 and ubicado1==False:
            menos3=cuantos
            namem3=nombre
            ubicado1=True
            

    llaves1 = m.keySet(analyzer['stationsEnd'])
    ite1 = it.newIterator(llaves1)
    mayore1=0
    namee1=""
    mayore2=0
    namee2=""
    mayore3=0 
    namee3=""
    while(it.hasNext(ite1)):
        info=it.next(ite1)
        actual=m.get(analyzer['stationsEnd'],info)['value']
        noviaje = int(actual["cuantosViajes"])
        nombre=actual["nombre"]
        ubicado=False
        if noviaje >= mayore1 and ubicado==False:
            mayore3=mayore2
            namee3=namee2
            mayore2=mayore1
            namee2=namee1
            mayore1=noviaje
            namee1=nombre
            ubicado=True
        elif noviaje >= mayore2 and ubicado==False:
            mayore3=mayore2
            namee3=namee2
            mayore2=noviaje
            namee2=nombre
            ubicado=True
        elif noviaje >= mayors3 and ubicado==False:
            mayore3=noviaje
            namee3=nombre
            ubicado=True

    print(" la estaciones mas populares para salir son : \n1."+names1+"con : "+str(mayors1)+" viajes. \n2."+names2+"con : "+str(mayors2)+" viajes. \n3."
        +names3+"con : "+str(mayors3)+" viajes. \n")
    print(" la estaciones mas populares para llegar son : \n1."+namee1+"con : "+str(mayore1)+" viajes. \n2."+namee2+"con : "+str(mayore2)+" viajes. \n3."
        +namee3+"con : "+str(mayore3)+" viajes. \n")
    print(" la estaciones menos visitadas son : \n1."+namem1+"con : "+str(menos1)+" viajes. \n2."+namem2+"con : "+str(menos2)+" viajes. \n3."
        +namem3+"con : "+str(menos3)+" viajes. \n")

def rutasPorEdad(analyzer, edad):
    cuantosinicio=0
    ninicio=''
    cuantosfinal=0
    nfinal=''

    llaves = m.keySet(analyzer['stationsStart'])
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual=m.get(analyzer['stationsStart'],info)['value']
        nocuantos=0
        if edad=="0-10":
            nocuantos = actual["edades"]["0-10"]
        elif edad=="11-20":
            nocuantos = actual["edades"]["11-20"]
        elif edad=="21-30":
            nocuantos = actual["edades"]["21-30"]
        elif edad=="31-40":
            nocuantos = actual["edades"]["31-40"]
        elif edad=="41-50":
            nocuantos = actual["edades"]["41-50"]
        elif edad=="51-60":
            nocuantos = actual["edades"]["51-60"]
        elif edad=="60+":
            nocuantos = actual["edades"]["60+"]

        if nocuantos >= cuantosinicio :
           cuantosinicio = nocuantos
           ninicio = info

    llaves1 = m.keySet(analyzer['stationsEnd'])
    ite1 = it.newIterator(llaves1)
    while(it.hasNext(ite1)):
        info=it.next(ite1)
        actual=m.get(analyzer['stationsEnd'],info)['value']
        nocuantos=0
        if edad=="0-10":
            nocuantos = actual["edades"]["0-10"]
        elif edad=="11-20":
            nocuantos = actual["edades"]["11-20"]
        elif edad=="21-30":
            nocuantos = actual["edades"]["21-30"]
        elif edad=="31-40":
            nocuantos = actual["edades"]["31-40"]
        elif edad=="41-50":
            nocuantos = actual["edades"]["41-50"]
        elif edad=="51-60":
            nocuantos = actual["edades"]["51-60"]
        elif edad=="60+":
            nocuantos = actual["edades"]["60+"]
        if nocuantos >= cuantosfinal :
           cuantosfinal = nocuantos
           nfinal = info
    
    analyzer['paths'] = bfs.BreadhtFisrtSearch(analyzer['graph'], ninicio)
    caminos = bfs.pathTo(analyzer['paths'], nfinal)
    pasos=1
    tiempo=0
    print(caminos['size'])
    primero= caminos['first']
    siguiente = primero['next']
    ultimo=caminos['last']
    for i in range(caminos['size']-1):
        infoin = primero['info']
        if siguiente is not None:
            infoul = siguiente['info']
            arco = gr.getEdge(analyzer["graph"], infoin, infoul)
            if arco is not None:
                tiempo += float(arco["weight"])
        info=m.get(analyzer['stationsStart'],infoin)['value']
        print(str(pasos)+". "+ info["nombre"])
        pasos+=1
        primero = primero['next']
        siguiente = siguiente['next']
    if ultimo is not None:
        info = m.get(analyzer['stationsEnd'],ultimo['info'])['value']
        print(str(pasos)+". "+ info["nombre"])
    print("el tiempo estimado es: "+ str(tiempo/60))

def cercanas(analyzer, lon1,lat1,lon2,lat2):
    llaves = m.keySet(analyzer['stationsStart'])
    ite = it.newIterator(llaves)
    menor=1000
    inicio=''
    ninicio=""
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual = m.get(analyzer['stationsStart'],info)['value']
        latitud = float(actual["latitud"])
        longitud= float(actual["longitud"])
        distancia= haversine(float(lon1),float(lat1),longitud,latitud)
        if distancia < menor:
            menor=distancia
            inicio=info
            ninicio = actual["nombre"]
    print("la estacion mas cercana al punto inicial es : "+ninicio)


    llaves1 = m.keySet(analyzer['stationsEnd'])
    ite1 = it.newIterator(llaves1)
    menor1=1000000000
    final=''
    nfinal=""
    while(it.hasNext(ite1)):
        info=it.next(ite1)
        actual=m.get(analyzer['stationsEnd'],info)['value']
        latitud = float(actual["latitud"])
        longitud = float(actual["longitud"])
        distancia = haversine(float(lon2),float(lat2),longitud,latitud)
        if distancia < menor1:
            menor1=distancia
            final=info
            nfinal = actual["nombre"]
    print("la estacion mas cercana al punto final es : "+nfinal)

    analyzer['paths'] = bfs.BreadhtFisrtSearch(analyzer['graph'], inicio)
    caminos = bfs.pathTo(analyzer['paths'], final)
    pasos=1
    print(caminos['size'])

    tiempo=0
    if caminos is not None:
        primero= caminos['first']
        siguiente = primero['next']
        ultimo=caminos['last']
        for i in range(caminos['size']-1):
            infoin = primero['info']
            if siguiente is not None:
                infoul = siguiente['info']
                arco = gr.getEdge(analyzer["graph"], infoin, infoul)
                if arco is not None:
                    tiempo += float(arco["weight"])
            info=m.get(analyzer['stationsStart'],infoin)['value']
            print(str(pasos)+". "+ info["nombre"])
            pasos+=1
            primero = primero['next']
            siguiente = siguiente['next']
        if ultimo is not None:
            info=m.get(analyzer['stationsEnd'],ultimo['info'])['value']
            print(str(pasos)+". "+ info["nombre"])
        print("el tiempo estimado es: "+ str(tiempo/60))

def publicidad(analyzer, edad):
    cuantosinicio=0
    ninicio=""
    cuantosviin=0

    cuantosopc=0
    opcional=""
    cuantosviinop=0

    cuantosfinal=0
    nfinal=""
    cuantosvifin=0

    cuantosopc1=0
    opcional1=""
    cuantosvifinop=0


    llaves = m.keySet(analyzer['stationsStart'])
    ite = it.newIterator(llaves)
    while(it.hasNext(ite)):
        info=it.next(ite)
        actual=m.get(analyzer['stationsStart'],info)['value']
        nocuantos=0
        cuantossub= int(actual["subs"])
        if edad=="0-10":
            nocuantos = actual["edades"]["0-10"]
        elif edad=="11-20":
            nocuantos = actual["edades"]["11-20"]
        elif edad=="21-30":
            nocuantos = actual["edades"]["21-30"]
        elif edad=="31-40":
            nocuantos = actual["edades"]["31-40"]
        elif edad=="41-50":
            nocuantos = actual["edades"]["41-50"]
        elif edad=="51-60":
            nocuantos = actual["edades"]["51-60"]
        elif edad=="60+":
            nocuantos = actual["edades"]["60+"]

        if (nocuantos+cuantossub) > cuantosinicio :
            cuantosopc= cuantosinicio
            opcional=ninicio
            cuantosviinop = cuantosviin
            cuantosinicio = (nocuantos+cuantossub)
            ninicio = actual["nombre"]
            cuantosviin = actual["cuantosViajes"]

    llaves1 = m.keySet(analyzer['stationsEnd'])
    ite1 = it.newIterator(llaves1)
    while(it.hasNext(ite1)):
        info=it.next(ite1)
        actual=m.get(analyzer['stationsEnd'],info)['value']
        nocuantos=0
        cuantossub= int(actual["subs"])
        if edad=="0-10":
            nocuantos = actual["edades"]["0-10"]
        elif edad=="11-20":
            nocuantos = actual["edades"]["11-20"]
        elif edad=="21-30":
            nocuantos = actual["edades"]["21-30"]
        elif edad=="31-40":
            nocuantos = actual["edades"]["31-40"]
        elif edad=="41-50":
            nocuantos = actual["edades"]["41-50"]
        elif edad=="51-60":
            nocuantos = actual["edades"]["51-60"]
        elif edad=="60+":
            nocuantos = actual["edades"]["60+"]
        if (nocuantos+cuantossub) > cuantosfinal :
            cuantosopc1= cuantosfinal
            opcional1=nfinal
            cuantosvifinop = cuantosvifin
            cuantosfinal = (nocuantos+cuantossub)
            nfinal = actual["nombre"]
            cuantosvifin = actual["cuantosViajes"]

    pareja1 = ("la estacion identificada es:\n inicio en:" + ninicio + "con : "+ str(cuantosviin)+" viajes registrados\n, y con su estacion de llegada : "+nfinal+" con : "+str(cuantosvifin)+" viajes registrados" )
    pareja2 = ("\nopcional la estacion identificada es:\n inicio en:" + opcional + "con : "+ str(cuantosviinop)+" viajes registrados\n, y con su estacion de llegada : "+opcional1+" con : "+str(cuantosvifinop)+" viajes registrados" )
    print(pareja1+pareja2)

def mantenimiento(analyzer, idbike, fecha):
    info= m.get(analyzer['bikes'],idbike)['value']
    if info is not None:
        dia = datetime.datetime.strptime(fecha, '%Y-%m-%d')
        info2= m.get(info["fecha"], dia.date())['value']
        tiempototaluso= int(info2["tiempouso"])/60
        tiempoestacionada = ((60*24)-tiempototaluso)
        viajes=[info2["viajes"]]
        print("el tiempo de uso es : "+ str(tiempototaluso)+", y el tiempo estacionada es: "+ str(tiempoestacionada)+", minutos")
        cual=0
        for i in range(info2["viajes"]['size']):
            print(str(cual)+". "+ lt.getElement(info2["viajes"],i)["start station name"] )
            cual+=1

# ==============================
# Funciones Helper
# ==============================
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    formula tomada de https://stackoverflow.com/questions/42686300/how-to-check-if-coordinate-inside-certain-area-python
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 3956 # Radius of earth in miles. Use 3956 for miles
    return c * r

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

def compareBikes(bike1, bike2):
    trip1=int(bike1)
    trip2= int(bike2['key'])
    if (trip1 == trip2):
        return 0
    elif (trip1 > trip2):
        return 1
    else:
        return -1

def compareDates(date1, date2):

    if (date1 == date2['key']):
        return 0
    elif (date1 > date2['key']):
        return 1
    else: 
        return -1