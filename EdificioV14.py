
'''
Autores:   Manuel López-Amo Ocón
           Alejandro Galván Pérez-Ilzarbe
           Santiago Cebellán
           Alejandro Meza Tudela
'''

#Importacion de librerias
import numpy as np #agrega soporte para vectores y matrices, contituye biblioteca de funciones de alto nivel
from numpy import random #random permite la generacion de numeros aleatorios 
from random import choices #choices esta dedicado a la representacion de pesos 
import pandas as pd

from abc import ABC, abstractmethod #util para la definicion de la clase abstracta 



#Clase que representa un edificio
'''
Lista de atributos de la clase edificio: 
                 
                   capacidadEdificio: entero que representa la capacidad de habitantes o huespedes del edificio
                   numeroEdificio: identificador del edificio 
                   departamentos: lista de listas, que contiene los departamentos, que a su vez son listas 
                   habitantesPorDepartamento: lista que contiene el numero de habitantes por subdivision
                   tipo: atributo que representa el tipo de edificio del que se trata
                  
'''
class Edificio(ABC):
    def __init__(self,numeroEdificio, tipo, capacidadEdificio = None,  maxCapacidad = None, estructuraFija = None):
        if estructuraFija is not None: #Comprueba si ha recibido un argumento para determinar concretamente la estructura del edificio (los departamentos)
            self.capacidadEdificio = sum(estructuraFija)
            self.numeroEdificio = numeroEdificio
            self.habitantesPorDepartamento = estructuraFija
            self.departamentos = []
            for i in len(self.habitantesPorDepartamento):
                self.departamentos.append([])
        else:
            if capacidadEdificio is None or maxCapacidad is None:
                raise AttributeError('Faltan parametros')
            self.capacidadEdificio = capacidadEdificio #entero que representa la capacidad de este edificio 
            self.numeroEdificio = numeroEdificio #entero que representa un identificador del edificio
            self.departamentos = []  #lista de listas, que contiene los departamentos, que a su vez son listas 
            self.habitantesPorDepartamento = [] #lista que contiene el numero de habitantes por subdivision
        
            contadorEdificio = 0
            
            #Se procede a la creacion de edificios
            aux = random.randint(1,maxCapacidad)
             
            while(aux + contadorEdificio <= self.capacidadEdificio): 
                self.habitantesPorDepartamento.append(aux) 
                contadorEdificio += aux
                aux = random.randint(1,maxCapacidad)
                self.departamentos.append([])
                
            #Posible caso que sobre un poco de la capacidad del edificio
            if(contadorEdificio < self.capacidadEdificio):
                aux = self.capacidadEdificio - contadorEdificio
                self.habitantesPorDepartamento.append(aux) 
                self.departamentos.append([])
                
        self.numerodepartamentos = len(self.departamentos)
        self.tipo = tipo
            
    
    #Metodo que imprime los atributos de la clase
    @abstractmethod
    def __str__(self):
            return str(self.numeroEdificio) + ", " + str(self.capacidadEdificio) + ", " + str(self.numerodepartamentos) + ", " + self.tipo
    
    #Metodo que devuelve personas de un departamento, dado el numero de esto 
    def devolverPersonasDepartamento(self, numero):
        return self.departamentos[numero]
    
    #Metodo dedicado a la acomodacion de personas en los edificios
    @abstractmethod
    def acomodar(self, personas):
        pass
    
    
'''
 Clase Vivienda (herencia de la clase edificio)
''' 
class Vivienda(Edificio):
        def __init__(self,numeroEdificio,capacidadEdificio, maxCapacidad):
            super().__init__(numeroEdificio = numeroEdificio, capacidadEdificio = capacidadEdificio, maxCapacidad = maxCapacidad, tipo = "vivienda") #se llama al constructor de la clase padre

        #Metodo encargado de acomodar a un conjunto de personas en el edificio
        def acomodar(self, personas):
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado acomodar demasiadas personas en una oficina")
            aux = 0 
            for num, cap in enumerate(self.habitantesPorDepartamento): #se itera en la lista con los habitantes por departamento  
                for n in range(aux, aux + cap):  #Se itera por cada vivienda
                    personas[n].idVivienda = (self.numeroEdificio, num)  #se asigna a cada persona el id de su vivienda: numeroEdificio + numero
                aux += cap

                    
'''
 Clase oficina (herencia de la clase edificio)
'''
class Oficina(Edificio):
        def __init__(self,numeroEdificio,capacidadEdificio = None, maxCapacidad = None, vestibulo = False, aforo = None, estructuraFija = None, tipo = "general"):
            super().__init__(numeroEdificio = numeroEdificio, capacidadEdificio = capacidadEdificio, maxCapacidad = maxCapacidad, tipo = tipo) #con esto se llama al constructor de la clase padre
            #Se procede a comprobar si hay vestibulo o no 
            if vestibulo:  
                if aforo is None: #Si el aforo es nulo se levanta un error
                    raise TypeError("Necesario aforo para el vestibulo")
                #En caso de que no lo sea, se crea el vestibulo y se coge el aforo
                self.vestibulo = [] #El vestibulo es un departamento aparte, una lista que contiene a personas (visitantes)
                self.aforo = aforo
            else:
                self.vestibulo = None
                
        #Metodo encargado de acomodar a un conjunto de personas en el edificio      
        def acomodar(self, personas):
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado acomodar demasiadas personas en una oficina")
            aux = 0
            for num, cap in enumerate(self.habitantesPorDepartamento):#se itera en la lista con los habitantes por departamento  
                for n in range(aux, aux + cap): #Se itera por cada vivienda
                    personas[n].idOficina = (self.numeroEdificio, num) #se asigna a cada persona el id de su vivienda: numeroEdificio + numero
                aux += cap
                    
        #Metodo que devuelve verdadero si el aforo del vestibulo esta completo
        def lleno(self):
            return len[self.vestibulo] >= self.aforo

        
        

