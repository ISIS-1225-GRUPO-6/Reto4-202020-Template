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

import config as cf
from App import model
import csv
import os

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadTrips (analyzer):
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            print('Cargando archivo: ' + filename)
            loadServices(analyzer, filename)
    return analyzer


def loadServices(analyzer, servicesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.
    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """
    servicesfile = cf.data_dir + servicesfile
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=",")
    for lastservice in input_file:
        model.addNewTrip(analyzer, lastservice)
        
    return analyzer

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def totalStops(analyzer):
    """
    Total de paradas de autobus
    """
    return model.totalStops(analyzer)

def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)

def connectedComponents(analyzer):
    """
    Numero de componentes fuertemente conectados
    """
    return model.connectedComponents(analyzer)

def estaciones(analyzer):
    model.estaciones(analyzer)

def rutasEdad(analyzer, edad):
    model.rutasPorEdad(analyzer,edad)

def cercanas(analyzer, lonin,latin,lonfin,latfin):
    model.cercanas(analyzer,lonin,latin,lonfin,latfin)

def publicidad(analyzer,edad):
    model.publicidad(analyzer,edad)

def mantenimiento(analyzer, idbike, fecha):
    model.mantenimiento(analyzer,idbike,fecha)

def rutacircular( analyzer, idestacion, tiempoin, tiempofin):
    model.rutaCircular(analyzer, idestacion, tiempoin,tiempofin)

def rutaresistencia(analyzer, idestacion, tiempo):
    model.rutaresistencia(analyzer, idestacion, tiempo)