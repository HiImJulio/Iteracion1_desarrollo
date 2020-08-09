
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
import os 
import seaborn as sns
import matplotlib.pyplot as plt #Dedicado a la representacion grafica 
from scipy.stats import rv_discrete
import pandas as pd

from abc import ABC, abstractmethod #util para la definicion de la clase abstracta 



#Clase que representa un edificio
'''
Lista de atributos: 
                 
                   capacidadEdificio: entero que representa la capacidad de habitantes o huespedes del edificio
                   numeroEdificio: identificador del edificio 
                   departamentos: lista de listas, que contiene los departamentos, que a su vez son listas 
                   habitantesPorDepartamento: lista que contiene el numero de habitantes por subdivision
                   numerodepartamentos: numero de departamentos 
        
'''
class Edificio(ABC):
    def __init__(self,numeroEdificio, capacidadEdificio = None,  maxCapacidad = None, estructuraFija = None, tipo):
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
                
            #Posible caso 
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
    
  
    def devolverPersonasDepartamento(self, numero):
        return self.departamentos[numero]
    
    
    @abstractmethod
    def acomodar(self, personas):
        pass
            
 #Primera clase que hereda 
class Vivienda(Edificio):
        #Primera aproximacion del metodo 
        def __init__(self,numeroEdificio,capacidadEdificio, maxCapacidad):
            super().__init__(numeroEdificio = numeroEdificio, capacidadEdificio = capacidadEdificio, maxCapacidad = maxCapacidad, tipo = "vivienda") #con esto se llama al constructor de la clase padre

        
        def acomodar(self, personas):
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado acomodar demasiadas personas en una oficina")
            aux = 0
            for num, cap in enumerate(self.habitantesPorDepartamento):
                for n in range(aux, aux + cap):
                    personas[n].idVivienda = (self.numeroEdificio, num)
        
class Oficina(Edificio):
        #Primera aproximacion del metodo 
        def __init__(self,numeroEdificio,capacidadEdificio = None, maxCapacidad = None, vestibulo = False, aforo = None, estructuraFija = None, tipo = "general"):
            super().__init__(numeroEdificio = numeroEdificio, capacidadEdificio = capacidadEdificio, maxCapacidad = maxCapacidad, tipo = tipo) #con esto se llama al constructor de la clase padre
            if vestibulo:
                if aforo is None:
                    raise TypeError("Necesario aforo para el vestibulo")
                self.vestibulo = [] #El vestibulo es un departamento a parte, una lista que contiene a personas (visitantes)
                self.aforo = aforo
            else:
                self.vestibulo = None
                
                
        def acomodar(self, personas):
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado acomodar demasiadas personas en una oficina")
            aux = 0
            for num, cap in enumerate(self.habitantesPorDepartamento):
                for n in range(aux, aux + cap):
                    personas[n].idOfcina = (self.numeroEdificio, num)
                    
        
        def lleno(self):
            return len[self.vestibulo] >= self.aforo

        
        

