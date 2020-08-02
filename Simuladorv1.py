'''
Autores:   Manuel López Amo-Ocón
           Alejangro Galván Pérez-Ilzarbe
           Santiago Cebellán
           Alejandro Meza Tudela
           
Fecha de versión final: 01-08-2020 
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
from PersonaV0 import *

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
        def __init__(self, numpersonas,personasedificio,mortalidadEdadesCovid):
            self.dtrEdad=self.generador_distribucion()
            self.ciudad=self.crearciudadv0(numpersonas,personasedificio)

            self.dia=0 #se inicializa el dia con un valor de 0 
            self.hora=0 #se inicializa las horas con un valor de 0 
            self.numpersonasinicial=numpersonas 
            self.numpersonas=numpersonas
            self.numedificios=len(self.ciudad)
            self.capacidades=np.zeros(self.numedificios)
            self.CatalogoPersonas=[]
            self.cementerio=[]
            for i in range(self.numedificios-1,-1,-1):
                self.capacidades[i]=int(len(self.ciudad[i])) #establecemos las capacidades de los edificios
                for j in range (len(self.ciudad[i])):
                    self.CatalogoPersonas.append(self.ciudad[i][j])
                    
            self.capacidades=self.capacidades.astype(int)
            #self.distrEdad=self.dtrEdad
            self.RegistroSanos=[numpersonas]
            self.RegistroMuertos=[]
            self.mortalidadEdadesCovid=mortalidadEdadesCovid
                
         #Devuelve un string con la informacion util del simulador   
        def __str__(self):
            return str(self.dia) + "," + str(self.hora) + "," + str(self.numpersonas) + "," +str(self.numedificios)  
        
        #Metodo que se encarga de actualizar los datos de las personas ordenadas por id 
        def actualizar_catalogo(self):
            nuevoCatalogo=[]
            for i in range(self.numedificios):
                for j in range (len(self.ciudad[i])):
                    nuevoCatalogo.append(self.ciudad[i][j]) #primero cogemos todas las personas sin ordenar
                    self.CatalogoPersonas = sorted(nuevoCatalogo, key=lambda x: x.idpersona, reverse=False) #ordenamos de acuerdo al id
            
        #Metodo que hace que el simulador avance una hora , con sus consecuencias en las personas
        def pasar_tiempo(self,mediaincubacion,desvincubacion,mediaduracion,desvduracion,posibilidadContagio ):
            self.RegistroSanos.append(self.personas_sanas())
            if ((self.hora % 8)==0): #barajar a las personas cada 8 horas( hacen shuffle)
                self.moverpersonas2()
                #print("owo")
            for j in range(len(self.ciudad)): #recorre los edificios 
                for i in range(len(self.ciudad[j])): #recorre las personas 
                    self.ciudad[j][i].infectar(posibilidadContagio,self.ciudad,mediaincubacion,desvincubacion,self.dia) #pasa a infectar 
            if (self.hora<23):
                self.hora+=1
            else:#comienza un nuevo dia
                self.hora=0
                self.dia+=1
                for j in range(len(self.ciudad)):
                    for i in range(len(self.ciudad[j])):                     
                        self.ciudad[j][i].transicionEstados(self.dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,self.mortalidadEdadesCovid)
                        
                for j in range(len(self.ciudad)):
                    for i in range(len(self.ciudad[j])-1,-1,-1):   
                        if (self.ciudad[j][i].estado=="muerto"):
                            
                            self.cementerio.append(self.ciudad[j].pop(i))
                            self.numpersonas-=1
                self.cementerio=sorted(self.cementerio, key=lambda x: x.idpersona, reverse=False)
                self.RegistroMuertos.append(len(self.cementerio))
                            
        
        #Función que devuelve el total de personas sanas o que ya pasaron la enfermedad de la ciudad
        def personas_sanas(self):
            contador_sanos=0
            for j in range(len(self.ciudad)): #se recorre los edificios de la ciudad
                    for i in range(len(self.ciudad[j])): #se va recorriendo las personas de los edificios 
                        if self.ciudad[j][i].esta_sano():
                            contador_sanos+=1
            return contador_sanos
        
        #Funcion que actualiza el catalago de personas, para luego devolver un individuo
        def cogerpersona(self, idpersona):
            self.actualizar_catalogo()
            return self.CatalogoPersonas[idpersona]
        
        #Baraja a todas las personas de la ciudad indiscriminadamente
       #Vamos a crear una nueva ciudad utilizando las personas actuales  
        def moverpersonas(self):
            print(f"Total de vivos:{self.numpersonas}")
            personasColocadas=0
            edificiosSinVaciar=self.numedificios
            ciudadnueva=[] #la nueva ciudad
            for i in range(self.numedificios-1,-1,-1):
                if (len(self.ciudad[i])==0):
                    del self.ciudad[i]
                    edificiosSinVaciar-=1
            
            for i in range(self.numedificios):
                edificionuevo = [] #El edificio actual de la ciudad nueva.
                
                for j in range(self.capacidades[i]):
                    if personasColocadas==self.numpersonas:
                        break
                    
                    if edificiosSinVaciar>1:
                        edificioescogido=random.randint(0,edificiosSinVaciar)
                    else:
                        edificioescogido=0
                    edificionuevo.append(self.ciudad[edificioescogido].pop(0))
                    edificionuevo[j].lugar=i
                    personasColocadas+=1
                    if (personasColocadas==self.numpersonas):
                        break
                    if (len(self.ciudad[edificioescogido])==0):
                        del  self.ciudad[edificioescogido]
                        edificiosSinVaciar-=1
            
                ciudadnueva.append(edificionuevo)
                
            self.ciudad=ciudadnueva
        
        #Metodo que se encarga del movimiento de las personas en la ciudad
        def moverpersonas2(self):
            print(f"Total de vivos:{self.numpersonas}")
            personasColocadas=0
            edificiosAntiguos=self.numedificios
            ciudadnueva=[] #la nueva ciudad
            opciones=[]
            for i in range(self.numedificios):
                edificionuevo=[]
                ciudadnueva.append(edificionuevo)
                opciones.append(i)
            
            personasColocadas=0
            edificiosLlenos=self.numedificios
            
            for i in range(self.numedificios):
                for j in range(len(self.ciudad[i])):
                    if (len(self.ciudad[i])==0):
                        break
                    edificioALlenar=random.choice(opciones)
                    ciudadnueva[edificioALlenar].append(self.ciudad[i].pop(0))
                    if (len(ciudadnueva[edificioALlenar])==self.capacidades[edificioALlenar]):
                        opciones.remove(edificioALlenar)
            self.ciudad=ciudadnueva
            
            
        #Función que contagia a la primera persona (la deja sintomática), se usa para crear pacientes 0
        def contagio_fijo(self, cambioEstadoInicial):
            self.ciudad[0][0].estado=self.ciudad[0][0].estadosposibles[3]
            self.ciudad[0][0].cambioEstado= cambioEstadoInicial
            
        #Funcion que se encarga de mostrar el cementerio 
        def mostrarcementerio(self):
            print(f"Total de muertos:{len(self.cementerio)}")
            for j in range(len(self.cementerio)):
                print(self.cementerio[j])
        
        #Metodo que se encarga de la representacion grafica de las personas sanas
        def  graficoPersonasSanas(self):   
            arr=np.reshape(self.RegistroSanos, (len(self.RegistroSanos), 1)).T[0]
            data=pd.DataFrame({'horas':range(0,len(self.RegistroSanos)),'personas_sanas':arr})
            sns.relplot(x="horas",y="personas_sanas", kind="line", data=data)
            
        def  graficoPersonasEdades(self):   
            edades=[self.CatalogoPersonas[i].edad for i in range(len(self.CatalogoPersonas))]      
            arr=np.reshape(edades, (len(self.CatalogoPersonas), 1)).T[0]
            plt.hist(arr, bins=50)
            plt.show()
            
         #Metodo que se encarga de la representacion grafica de las personas muertas
        def  graficoPersonasMuertas(self):   
            arr=np.reshape(self.RegistroMuertos, (len(self.RegistroMuertos), 1)).T[0]
            data=pd.DataFrame({'horas':range(0,len(self.RegistroMuertos)),'personas_muertas':arr})
            sns.relplot(x="horas",y="personas_muertas", kind="line", data=data)
            
            
            
            
        #Esta función crea la ciudad en la versión 0 de la simulacion.
        #La ciudad es una lista de edificios y cada edificio es una lista de personas de tamaño variable.
        #Input: personas de la ciudad, media de personas por edificio.
        #Output: la ciudad.
        def crearciudadv0(self,numpersonas,personasedificio):
            edificios = [] #La ciudad.
            capacidadusada=0 #Numero de personas metidas en la ciudad.
            edificioactual=0 #indice del numero del edificio
            while (capacidadusada < numpersonas):
                column = [] #El edificio.
                esteedificio=random.randint(1,personasedificio*3) #entero que representa la capacidad de este edificio 
                '''
                Maximo de personas en el edificio. 
                Si usamos desviación tipica de capacidad de edificio, iria aqui
                '''
                contadoredificio=0 #numero de personas colocadas en este edificio
                #print(f"edificio actual:{edificioactual}")

                #Bucle en el que se llena el edificio de personas.
                while (capacidadusada < numpersonas) and (contadoredificio < esteedificio):

                    #print(f"contador del edificio:{contadoredificio}")
                    #print(f"capacidad:{esteedificio}")

                    #Insercion de persona.
                    column.append(Persona(capacidadusada,edificioactual,self.dtrEdad))
                    capacidadusada+=1
                    contadoredificio+=1


                #Insercion de edificio en la ciudad
                edificios.append(column)
                edificioactual+=1

            return edificios
        
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
