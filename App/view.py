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


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________
initialStation = None
recursionLimit = 20000

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de rutas de citybike")
    print("3- Calcular componentes conectados")
    print("4- Ruta circular")
    print("5- Informacion estaciones")
    print("6- ruta resistencia")
    print("7- recomendar rutas por edad")
    print("8- ruta de interes turistico")
    print("9- publicidad")
    print("10- mantenimiento")
    
    print("0- Salir")
    print("*******************************************")

def seledad(resp):
    if resp==1:
        return '"0-10"'
    elif resp==2:
        return '"11-20"'
    elif resp==3:
        return '"21-30"'
    elif resp==4:
        return '"31-40"'
    elif resp==5:
        return '"41-50"'
    elif resp==6:
        return '"51-60"'
    if resp==7:
        return '"60+"'

def optionTwo():
    print("\nCargando información de los viajes de citibike ....")
    controller.loadTrips(cont)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion se ajusta a: ' + str(recursionLimit))

def optionThree():
    print('El número de componentes conectados es: '+ str(controller.connectedComponents(cont)))

def optionfour():
    idestacion = input("id de la estacion de inicio\n")
    tiempoin = int(input("tiempo minimo disponible\n"))
    tiempofin = int(input("tiempo maximo disponible\n"))
    controller.rutacircular(cont, idestacion,tiempoin,tiempofin)

def optionfive():
    controller.estaciones(cont)

def optionsix():
    idestacion = input("id de la estacion de inicio\n")
    tiempo = int(input("tiempo minimo disponible\n"))
    controller.rutaresistencia(cont, idestacion, tiempo)

def optionseven():
    print( "1. 0-10 \n2. 11-20 \n3. 21-30 \n4. 31-40 \n5. 41-50 \n6. 51-60 \n7. 60+")
    resp = input('seleccion edad\n')
    cual = seledad(resp)
    controller.rutasEdad(cont, cual)

def optioneight():
    latin=input("ingrese la latitud inicial\n")
    lonin=input("ingrese la longitud inicial\n")
    latfin=input("ingrese la latitud del sitio turistico a visitar\n")
    lonfin=input("ingrese la longitud del sitio turistico a visitar\n")
    controller.cercanas(cont,lonin,latin,lonfin,latfin)

def optionnine():
    print( "1. 0-10 \n2. 11-20 \n3. 21-30 \n4. 31-40 \n5. 41-50 \n6. 51-60 \n7. 60+")
    resp = input('seleccion edad\n')
    cual = seledad(resp)
    controller.publicidad(cont,cual)

def optionten():
    bikeid=input("ingrese bike id\n")
    fecha = input("ingrese fecha y-m-d\n")
    controller.mantenimiento(cont,bikeid,fecha)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs) == 1:
        print("\nInicializando....")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        executiontime = timeit.timeit(optionTwo, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 3:
        executiontime = timeit.timeit(optionThree, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 4:
        executiontime = timeit.timeit(optionfour, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 5:
        executiontime = timeit.timeit(optionfive, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 6:
        executiontime = timeit.timeit(optionsix, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs[0]) == 7:
        executiontime = timeit.timeit(optionseven, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 8:
        executiontime = timeit.timeit(optioneight, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    elif int(inputs[0]) == 9:
        executiontime = timeit.timeit(optionnine, number=1)
        print("Tiempo de ejecución: " + str(executiontime))
    
    elif int(inputs) == 10:
        executiontime = timeit.timeit(optionten, number=1)
        print("Tiempo de ejecución: " + str(executiontime))

    else:
        sys.exit(0)
sys.exit(0)
    


