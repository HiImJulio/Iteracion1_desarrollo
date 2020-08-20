
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
from random import sample 
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
            if maxCapacidad>1:
                aux = random.randint(1,maxCapacidad)
            else:
                aux=1
            
            while(aux + contadorEdificio <= self.capacidadEdificio): 
                self.habitantesPorDepartamento.append(aux) 
                contadorEdificio += aux
                if maxCapacidad>1:
                    aux = random.randint(1,maxCapacidad)
                else:
                    aux=1
                self.departamentos.append([])
                
            #Posible caso que sobre un poco de la capacidad del edificio
            if(contadorEdificio < self.capacidadEdificio):
                aux = self.capacidadEdificio - contadorEdificio
                self.habitantesPorDepartamento.append(aux) 
                self.departamentos.append([])
                
        self.numerodepartamentos = len(self.departamentos)
        self.tipo = tipo
            
    
    #Metodo que imprime los atributos de la clase
    def __str__(self):
            return str(self.numeroEdificio) + ", " + str(self.capacidadEdificio) + ", " + str(self.numerodepartamentos) + ", " + self.tipo
    
    #Metodo que devuelve personas de un departamento, dado el numero de esto 
    def devolverPersonasDepartamento(self, numero):
        return self.departamentos[numero]
    
    #Metodo que imprime a las personas de los departamentos 
    def printearpersonas(self):
        print("ID :"+str(self.numeroEdificio))
        for i in range(len(self.departamentos)):
            print("Piso "+str(i)+" :")
            for j in self.departamentos[i]:
                print(j)
    
    #Metodo dedicado a la acomodacion de personas en los edificios
    @abstractmethod
    def acomodar(self, personas):
        pass
    
    #Metodo que se encarga del contagio en el edificio
    def contagiarEdificio(self,posibilidadContagio,mediaincubacion,desvincubacion,dia):
        for i in self.departamentos:
            pesoContagio=self.conteoContagiosos(i,posibilidadContagio)
            if pesoContagio<1:
                for j in i:
                    contagia=random.uniform(0, 1)
                    if (1-pesoContagio>contagia): #Podriamos hacerlo con distribucion de poisson
                        j.contagiarse(mediaincubacion,desvincubacion,dia)
                        print(contagia)
    
    #Metodo que devuelve una probabilidad
    def conteoContagiosos(self,piso,posibilidadContagio): #la probabilidad de que no te contagie nadie del piso
        peso=1
        for j in piso:
            if j.puede_propagar():
                peso*=j.infectar(posibilidadContagio)
        return peso
    
     #Metodo que realiza la transicion de estados de los individuos del edificio
    def transicionEdificio(self,dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid,simulador):
        for i in self.departamentos:
            for j in i:
                j.transicionEstados(dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid,simulador)
                
     #Metodo que hace que las personas realizen su comportamiento programado      
    def edificioIAS (self, hora, simulador):
         for i in self.departamentos:
            for j in i:
                j.simular_ia(hora, simulador)
    
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
         
         #Metodo que se encarga de meter personas en un edificio 
        def meterInicio(self,personas):
            #En caso de que se traten de meter mas personas que la capacidad del edificio 
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado meter personas en una casa")
            aux = 0 
            for num, cap in enumerate(self.habitantesPorDepartamento): #se itera en la lista con los habitantes por departamento  
                for n in range(aux, aux + cap):  #Se itera por cada vivienda 
                    personas[n].lugarActual=(self.numeroEdificio,num,0)
                    self.departamentos[num].append(personas[n])
                aux += cap

'''
 Clase oficina (herencia de la clase edificio)
'''
class Oficina(Edificio):
        horarios = pd.read_csv('horarios.csv') #Se almacena los horarios que contiene el csv
        
        def __init__(self, numeroEdificio, capacidadEdificio = None, maxCapacidad = None, vestibulo = False, aforo = None, estructuraFija = None, tipo = "general"):
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
            self.horarios = Oficina.elegirhorarios()
                
        #Metodo encargado de acomodar a un conjunto de personas en el edificio      
        def acomodar(self, personas):
            if len(personas) > self.capacidadEdificio:
                raise ValueError("Se han intentado acomodar demasiadas personas en una oficina")
            aux = 0
            hors = set()
            for num, cap in enumerate(self.habitantesPorDepartamento):#se itera en la lista con los habitantes por departamento  
                for n in range(aux, aux + cap): #Se itera por cada vivienda
                    personas[n].idOficina = (self.numeroEdificio, num) #se asigna a cada persona el id de su vivienda: numeroEdificio + numero
                    hor = random.randint(0, len(self.horarios))#Decide que horario va a tener esa persona
                    if num == 0 and self.vestibulo is not None:#Si esa persona va a trabajar en el vestibulo lo recuerda para despues hacer el horario del vestibulo
                        hors.add(hor)
                    personas[n].horario = self.horarios[hor]
                aux += cap
            if self.vestibulo is None:
                self.edificioAbierto = None
            else:
                iterador = iter(hors)
                i = next(iterador)
                self.edificioAbierto = self.horarios[i]
                for i in iterador:
                    self.edificioAbierto = self.edificioAbierto | self.horarios[i]
                    
        #Metodo que devuelve verdadero si el aforo del vestibulo esta completo
        def lleno(self):
            return len[self.vestibulo] >= self.aforo
        
        #Este metodo elige dos horarios para el edificio
        @staticmethod
        def elegirhorarios():
            aux = sample([i for i in range(0, len(Oficina.horarios.columns))], 2)
            return (Oficina.horarios.iloc[:, aux[0]], Oficina.horarios.iloc[:, aux[1]])
        
        #Metodo que se encarga de imprimir a las personas de los departamentos y a los idividuos
        #que se encuentren en el vestibulo
        def printearpersonas(self):
            super().printearpersonas() #Se llama al metodo de la clase padre
            print()
            print("Vestíbulo :"+ str(len(self.vestibulo))+ " / aforo:  "+str(self.aforo))
            for j in self.vestibulo:
                print(j)
        
         #Metodo que se encarga del contagio en el edificio
        def contagiarEdificio(self,posibilidadContagio,mediaincubacion,desvincubacion,dia):
            for i in range(len(self.departamentos)):
                pesoContagio=self.conteoContagiosos(i,posibilidadContagio)
                if pesoContagio<1:                
                    for j in self.departamentos[i]:
                        contagia=random.uniform(0, 1)
                        if (1-pesoContagio>contagia): #Podriamos hacerlo con distribucion de poisson
                            j.contagiarse(mediaincubacion,desvincubacion,dia)
                            print(contagia)
                    if i==0: ##Eficiencia lamentable pero francamente me da pereza arreglarlo ahora
                        for j in self.vestibulo:
                            contagia=random.uniform(0, 1)
                            if (1-pesoContagio>contagia): #Podriamos hacerlo con distribucion de poisson
                                j.contagiarse(mediaincubacion,desvincubacion,dia)
                                print(contagia)
        
         #Metodo que devuelve una probabilidad
        def conteoContagiosos(self,piso,posibilidadContagio): #la probabilidad de que no te contagie nadie del piso
            peso=1
            for j in self.departamentos[piso]:
                    if j.puede_propagar():
                        peso*=j.infectar(posibilidadContagio)
            if piso==0: #si se trata del vestibulo
                for u in self.vestibulo:
                    if u.puede_propagar():
                        peso*=u.infectar(posibilidadContagio)
            return peso
        
         #Metodo que realiza la transicion de estados de los individuos del edificio
        def transicionEdificio(self,dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid,simulador):
            for i in self.departamentos:
                for j in i:
                    j.transicionEstados(dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid,simulador)
            for u in self.vestibulo:
                u.transicionEstados(dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid,simulador)
        
        
        #Metodo que hace que las personas realizen su comportamiento programado     
        def edificioIAS (self, hora, simulador):
            for i in self.departamentos:
                for j in i:
                    j.simular_ia(hora, simulador)
            for u in self.vestibulo:
                u.simular_ia(hora, simulador)
        
        
        
        

