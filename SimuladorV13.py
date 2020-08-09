'''
Autores:   Manuel López Amo-Ocón
           Alejangro Galván Pérez-Ilzarbe
           Santiago Cebellán
           Alejandro Meza Tudela
      
'''


#importacion de librerias
import numpy as np #agrega soporte para vectores y matrices, contituye biblioteca de funciones de alto nivel
from numpy import random #random permite la generacion de numeros aleatorios 
from random import choices #choices esta dedicado a la representacion de pesos 
import os 
import seaborn as sns
import matplotlib.pyplot as plt #Dedicado a la representacion grafica 
from scipy.stats import rv_discrete
import pandas as pd

#importacion de la clase persona 
from PersonaV12 import *
from EdificioV13 import *


#Clase Simulador: contiene lo necesario para llevar a cabo la simulacion
'''
Lista de atributos: 
                    dtrEdad: variable que contiene una distribucion de las edades 
                    ciudad: ciudad que se crea para la simulacion  
                    dia: entero que representa el paso de los dias 
                    hora: entero que representa el paso de las horas 
                    numpersonasinicial: entero que representa el numero de personas iniciales de la simulacion
                    numpersonas: entero que representa el numero de personas de la simulacion.
                    numedificios: entero que representa el numero de edificios totales. 
                    capacidades : array que contiene las capacidades de los edificios
                    CatalogoPersonas: lista que contiene a las personas de la simulacion
                    cementerio: lista que contiene las personas muertes debido a la enfermedad
                    RegistroSanos: lista que contiene a los individuos que estan sanos
                    RegistroMuertos: lista que contiene los individuos que van muriendo
                    mortalidadEdadesCovid : lista de listas, que contiene la probabilidad de muerte dependiendo de ciertos rangos
                                            de edad
'''

class Simulador:
        def __init__(self, numpersonas,personasEdificio,maxPiso,mortalidadEdadesCovid,aforoMedio):
            self.dtrEdad=self.generador_distribucion()
            self.aforoMedio=aforoMedio
            self.ciudadViviendas=self.crearViviendas(numpersonas,personasEdificio,maxPiso)
            self.ciudadOficinas=self.crearOficinas(numpersonas,personasEdificio,maxPiso,aforoMedio)
            self.dia=0 #se inicializa el dia con un valor de 0 
            self.hora=0 #se inicializa las horas con un valor de 0 
            self.numpersonasinicial=numpersonas 
            self.numViviendas=len(self.ciudadViviendas)
            self.numOficinas=len(self.ciudadOficinas)
            #self.capacidades=np.zeros(self.numedificios)
            self.CatalogoPersonas=self.crearPoblacion()
            
            self.acomodarGente()
            self.printearCatalogo()
            self.cementerio=[]
            
           
            #self.distrEdad=self.dtrEdad
            self.RegistroSanos=[numpersonas]
            self.RegistroMuertos=[]
            self.mortalidadEdadesCovid=mortalidadEdadesCovid
            
        def crearPoblacion(self):
            poblacion=[]
            for i in range(self.numpersonasinicial):
                poblacion.append(Persona(i,self.dtrEdad))         
            return poblacion
            
        def crearOficinas(self,numpersonas,personasEdificio,maxCapacidad,aforoMedio):
            Oficinas=[]
            personasColocadas=0
            edificios=0
            while (numpersonas>personasColocadas):
                personasEsteEdificio=random.randint(int(personasEdificio/2),int((personasEdificio/2)*3))
                if (numpersonas<personasEsteEdificio+personasColocadas):
                    personasEsteEdificio=numpersonas-personasColocadas
                personasColocadas+=personasEsteEdificio
                EdificioActual=Oficina(numeroEdificio=edificios,capacidadEdificio=personasEsteEdificio,maxCapacidad=maxCapacidad,
                                       aforo=aforoMedio, vestibulo=True)
                Oficinas.append(EdificioActual)
                edificios+=1
            return Oficinas
        
        
        def acomodarGente(self):
            personasAcomodadas=0
            for i in self.ciudadViviendas:
                capactual=i.capacidadEdificio
                listaActual=self.CatalogoPersonas[personasAcomodadas:personasAcomodadas+capactual]
                i.acomodar(listaActual)
                personasAcomodadas+=capactual
            CatalogoBarajado=self.CatalogoPersonas.copy()
            random.shuffle(CatalogoBarajado)
            #for i in CatalogoBarajado:
            #    print(i)
            personasAcomodadas=0
            for i in self.ciudadOficinas:
                capactual=i.capacidadEdificio
                listaActual=CatalogoBarajado[personasAcomodadas:personasAcomodadas+capactual]
                i.acomodar(listaActual)
                personasAcomodadas+=capactual
                
                
        
        def crearViviendas(self,numpersonas,personasEdificio,maxCapacidad):
            Viviendas=[]
            personasColocadas=0
            edificios=0
            while (numpersonas>personasColocadas):
                personasEsteEdificio=random.randint(int(personasEdificio/2),int((personasEdificio/2)*3))
                if (numpersonas<personasEsteEdificio+personasColocadas):
                    personasEsteEdificio=numpersonas-personasColocadas
                personasColocadas+=personasEsteEdificio
                print(edificios,personasEsteEdificio,maxCapacidad)
                EdificioActual=Vivienda(numeroEdificio=edificios,capacidadEdificio=personasEsteEdificio,maxCapacidad=maxCapacidad)
                Viviendas.append(EdificioActual)
                edificios+=1
            return Viviendas
            
        def printearCatalogo(self):
            for i in self.CatalogoPersonas:
                print(i)
    
    
    
    
        def generador_distribucion(self):
            datos_edad = pd.read_csv("distribucion_edad.csv")
            l=list(datos_edad.iloc[:,0]) # cogemos todos los datos de la primera columna, pertenecientes a todas las filas
            l2= [] #definicion de una lista auxiliar 
            for i in range(len(l)-1):
                l2.append(int(l[i])/int(l[-1]))
            #Esto es para ajustar porque parece que el numero total de personas y el numero de personas por edad no acaba de coincidir
            #creo que es que corte los mayores de 100 años.
            l2.append(1-sum(l2))

            l3=[i for i in range(len(l2))]
            #Esta es la distribución que obtenemos
            dtrEdad = rv_discrete(values=(l3,l2))

            #Se procede a eliminar, para que no queden variables sueltas
            del l
            del l2
            del l3
            return dtrEdad
