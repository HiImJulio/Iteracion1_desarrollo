'''
Autores:   Manuel López Amo-Ocón
           Alejangro Galván Pérez-Ilzarbe
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


#Clase Persona: se encarga de representar obviamente a una persona. 
'''
Lista de atributos: 
                    idpersona : identificador numerico
                    edad: entero que reprenta la edad del individuo 
                    estados_posibles: array que contiene los posibles cambios de estado durante una enfermedad
                    estado : estado actual de la persona
                    lugar: lugar actual del individuo. Se inicializa con el lugar original.
                    lugar original : entero que representa el lugar de origen. Es el id del edificio.
                    cambioEstado: entero que indica que dia cambiara de estado la persona
                    contadorInfecciones
                    dni: representacion del DNI                  
'''
class Persona:
        def __init__(self, idpersona,dtrEdad):           
            self.idpersona=idpersona
            self.edad=self.generador_edad(dtrEdad)
            self.estadosposibles=["sano","incubando","incubandoContagioso","sintomatico","asintomatico","muerto","inmune"]
            self.estado=self.estadosposibles[0]
            self.cambioEstado=np.inf  #Atributo que indica que dia cambiara la persona de estado.
            self.contadorInfecciones=0
            self.dni = self.creaDni()
            self.edificiomuerte=-1
            self.idVivienda = (-1, -1)
            self.idOficina = (-1, -1)  
             # piso - edificio - que estoy haciendo : 0.vivienda   1.oficina    2.ocio 
            self.lugarActual=(-1,-1,-1)
            self.horario=None
     
            
             
        #Metodo que devuelve un string con la informacion util del sujeto
        def __str__(self):
            return "ID: "+str(self.idpersona) + ", Estado: " + str(self.estado) + ", DNI: "+str(self.dni)+", edad:"+str(self.edad)+", Vivienda y piso:" +str(self.idVivienda[0])+ ","  +str(self.idVivienda[1]) +", Oficina y piso:" +str(self.idOficina[0]) + "," + str(self.idOficina[1]) +"Lugar actual: "+str(self.lugarActual[0])+ " " +str(self.lugarActual[1])+ " " +str(self.lugarActual[2])+ " "
        
        #Metodo que determina si el individuo puede propagar o no la enfermedad
        def puede_propagar(self):
            return ((self.estado == "sintomatico") or (self.estado == "asintomatico") or (self.estado == "incubandoContagioso"))
        
        #Metodo que determina si un individuo es susceptible de contraer la enfermedad o no
        def susceptible(self):
            return (self.estado == "sano")
        
        #Metodo que determina si un individuo se encuentra  sano o no
        def esta_sano(self):
            return (self.estado == "sano") or (self.estado == "inmune")
        

        def infectar(self,posibilidadContagio): #probabilidad de que no te contagie este man
            base=posibilidadContagio #es raro que contagie por defecto
            if self.lugarActual[2]==0:
                base**1.6  # Si está en casa, hay más posibilidad de contagio
            if self.lugarActual[2]==1:
                base**0.4 # Si está en el trabajo, hay menos posibilidad de contagio
            if (self.estado == "sintomatico"):
                base**0.5 # Si es sintomático, hay menos posibilidad de contagio
                
            
            
            return base
                            
        #Metodo que basado en unas probabilidades dadas, determina si un individuo es asintomatico o no 
        def asintomatico_o_no(self):
            estado = ["asintomatico", "sintomatico"]
            peso_de_decision = [0.4, 0.6] #array de pesos  
            n = choices(estado, peso_de_decision) #choices devolvera un vector con el resultado de interes
            return n[0]
        
        #Metodo que determina la probabilidad de muerte de un individuo basada en su edad 
        def probabilidad_de_muerte(self,mortalidadEdadesCovid,mediaduracion):
            franja_edad=0

            valoracion = [0,1] #retornara 1 en caso de muerte, y 0 en caso contrario 
            while (mortalidadEdadesCovid[0][franja_edad]<self.edad):
                franja_edad+=1
            aux=mortalidadEdadesCovid[1][franja_edad]
            pesoraw=1-((aux/100)/(mediaduracion))
            peso=[pesoraw,1-pesoraw]
            print(peso,self.edad)
            n = choices(valoracion, peso) #n es un vector cuyo primer elemento es la valoracion 
            return n[0]
               
        #Funcion que simula el hecho de contagiarse. El individuo pasa a estar incubando el virus 
        def contagiarse(self,mediaincubacion,desvincubacion,diaactual):
            if(self.susceptible()==True):
                self.estado=self.estadosposibles[1]
                self.cambioEstado=diaactual+(random.randint(int(mediaincubacion-desvincubacion),int(mediaincubacion+desvincubacion))/2)
                if self.lugarActual[2]==0:
                    print("contagio en la casa "+str(self.idVivienda[0])+"!")
                elif self.lugarActual[2]==1:
                    print("contagio en la oficina "+str(self.idOficina[0])+"!")
        #Metodo que simula la transicion de estados en los individuos a lo largo de la simulacion               
        def transicionEstados(self, dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,mortalidadEdadesCovid):
            '''
            A partir de aqui se comprueba que estado posee la persona
            Y se mira dos casos:
            1.Si el individuo posee sintomas --> en ese caso, se ve su probabilidad de muerte
            2.En caso de que el cambio de estado sea menor o igual que el dia actual
            '''
            if(self.estado == "sintomatico"):
                me_voy_a_morir = self.probabilidad_de_muerte(mortalidadEdadesCovid,mediaduracion)
                if(me_voy_a_morir == 1):
                    self.cambioEstado=np.inf
                    self.estado = "muerto"
                    if self.lugarActual[2]==0:
                        print("muerte en la casa "+str(self.idVivienda[0])+"!")
                    elif self.lugarActual[2]==1:
                        print("muerte en la oficina "+str(self.idOficina[0])+"!")
            if(self.cambioEstado <= dia):
                if(self.estado == "incubando"):
                    self.estado = "incubandoContagioso" #se le asigna el siguiente estado  
                    self.cambioEstado = dia + random.randint(int(mediaincubacion-desvincubacion),int(mediaincubacion+desvincubacion))/2    #tiempo que pasa a inmune o muerto xD

                elif(self.estado == "incubandoContagioso"):
                    self.estado = self.asintomatico_o_no() #se le asigna el siguiente estado 
                    self.cambioEstado =dia+ random.randint(int(mediaduracion-desvduracion),int(mediaduracion+desvduracion)) #tiempo que pasa a inmune o muerto xD

                elif(self.estado == "sintomatico"):
                    self.cambioEstado = np.inf 
                    self.estado = "inmune"
                    '''
                      Y ahora una vez que pasa a ser asintomatico o no, se debe ver la probabilidad de que la persona se vaya 
                       a morir o no, y dependiendo de eso, se asignan unos dias...
                    '''

                elif(self.estado == "asintomatico"):
                    self.estado = "inmune"
                    self.cambioEstado = np.inf 
                                     
            #Funcion que se encarga de crear una secuencia valida de DNI
            #Para ello, se ha utilizado el algoritmo que se usa en la vida real -en cuanto a la relacion numero y letra- 
        def creaDni(self):
            letras = "TRWAGMYFPDXBNJZSQVHLCKEO" #conjunto de letras del dni
            numero=0
            for i in range(0,8): 
                n = random.randint(0,9)
                numero=10*numero+n
            input=numero
            #Se consigue que toda la secuencia de numeros sea 1 solo

            #Se calcula la letra que ha de ser adicionada
            valor =int(input / 23)
            #print(f"El valor en este caso es: {valor}")
            valor *= 23
            valor = input - valor;
            #Ahora, ha de pasarse el numero de la secuencia
            #a una lista donde cada elemento es un numero de la secuencia 
            DNI=str(input)+letras[valor]

            return DNI
        
        
        
          #Metodo que simula el comportamiento de la persona 
        #Para mover del sitio actual: hacer pop del sitio actual, y append en el lugar 
        def simular_ia(self, hora, simulador):
            #La variable hora hace checkear el valor de la columna correspondiente a su posicion 
            #Se necesita una variable que haga referencia al dataframe
            #Se comprueba si el individuo esta en casa o en ocio
            if(self.estado == "sintomatico"):
                 if(self.lugarActual[2] != 0):
                    simulador.irse(self)
                    simulador.meterse(self, self.idVivienda,0)
                    self.lugarActual = (self.idVivienda[0],self.idVivienda[1],0) 
       
            else:
                if(self.lugarActual[2] == 0 or self.lugarActual[2] == 2):
                     if(self.horario.iloc[hora] == True): #en caso de que tenga que ir al trabajo...                   
                       
                        
                        simulador.irse(self)
                        simulador.meterse(self, self.idOficina,1)
                        self.lugarActual = (self.idOficina[0],self.idOficina[1],1)  #se actualiza el valor
           
                #Se comprueba    
                elif(self.lugarActual[2] == 1):
                     if(self.horario.iloc[hora] == False): 
                        
                        simulador.irse(self)
                        simulador.meterse(self, self.idVivienda,0)
                        self.lugarActual = (self.idVivienda[0],self.idVivienda[1],0)  #se actualiza el valor
                        
                        
                        
                
        #Funcion que genera la edad de la persona en en base a una distribución discreta
        def generador_edad(self,dtrEdad):
            n = dtrEdad.rvs(size=1)[0] #el rango de edad, sera desde los 0 años hasta los 110
            return n
       
