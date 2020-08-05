
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
    def __init__(self,capacidadEdificio = None, numeroEdificio, maxCapacidad = None, estructuraFija = None):
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
            numeroPiso = 0 #variable iterativa
            
            #Se procede a la creacion de edificios
            aux = random.randint(1,maxCapacidad)
             
            while(aux + contadorEdifico <= self.capacidadEdificio): 
                self.habitantesPorDepartamento[self.numeroPiso].append(aux) 
                self.contadorEdificio += aux
                numeroPiso += 1
                aux = random.randint(1,maxCapacidad)
                self.departamentos.append([])
                
            #Posible caso 
            if(contadorEdificio < self.capacidadEdificio):
                aux = self.capacidadEdificio - contadorEdificio
                self.habitantesPorDepartamento[self.numeroPiso].append(aux) 
                self.departamentos.append([])
                
        self.numerodepartamentos = len(self.departamentos)
            
    
    #Metodo que imprime los atributos de la clase
    @abstractmethod
    def __str__(self):
            return str(self.numeroEdificio) + ", " + str(self.capacidadEdificio) + ", " + str(self.numerodepartamentos)
    
  
    def devolverPersonasDepartamento(self, numero):
        return self.departamentos[numero]
    
 #Primera clase que hereda 
 class Vivienda(Edificio):
        #Primera aproximacion del metodo 
        def __init__(self,capacidadEdificio,numeroEdificio, maxCapacidad):
            super().__init__(capacidadEdificio, numeroEdificio, maxCapacidad) #con esto se llama al constructor de la clase padre
         
        def __str__(self):
            return super().__str__() + ", vivienda" 
 
 class Oficina(Edificio):
        #Primera aproximacion del metodo 
        def __init__(self,capacidadEdificio = None,numeroEdificio, maxCapacidad = None, vestibulo = False, estructuraFija = None):
            super().__init__(capacidadEdificio, numeroEdificio, maxCapacidad, estructuraFija) #con esto se llama al constructor de la clase padre
            if vestibulo:
                self.vestibulo = [] #El vestibulo es un departamento a parte, una lista que contiene a personas (visitantes)
            else:
                self.vestibulo = None
         
        def __str__(self):
            return super().__str__() + ", oficina"
        
        

