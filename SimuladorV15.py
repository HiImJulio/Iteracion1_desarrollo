'''
Autores:   Manuel López Amo-Ocón
           Alejangro Galván Pérez-Ilzarbe
           Santiago Cebellán
           Alejandro Meza Tudela
      
'''


#importacion de librerias
import numpy as np #agrega soporte para vectores y matrices, contituye biblioteca de funciones de alto nivel
import random as rand
from numpy import random #random permite la generacion de numeros aleatorios 

from random import choices #choices esta dedicado a la representacion de pesos 
import os 
import seaborn as sns
import matplotlib.pyplot as plt #Dedicado a la representacion grafica 
from scipy.stats import rv_discrete
import pandas as pd



from PersonaV14 import * #importacion de la clase persona
from EdificioV16 import * #importacio de la clase edificio


#Clase Simulador: contiene lo necesario para llevar a cabo la simulacion
'''
Lista de atributos: 
                    dtrEdad: variable que contiene una distribucion de las edades 
                    ciudad: ciudad que se crea para la simulacion  
                    dia: entero que representa el paso de los dias 
                    hora: entero que representa el paso de las horas 
                    numpersonasinicial: entero que representa el numero de personas iniciales de la simulacion
                    numpersonas: entero que representa el numero de personas de la simulacion.
                    numViviendas: entero que representa el numero de viviendas totales. 
                    numOficinas: entero que representa el numero de oficinas totales.
                    serviciosDisponibles: lista que representa un conjunto de servicios disponibles: oficinas con vestibulo.
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
            self.serviciosDisponibles=[] #lista de servicios
            self.rellenarServicios() #metodo que se procedera a describir a continuacion
            self.CatalogoPersonas=self.crearPoblacion()
            print(self.serviciosDisponibles)
            print(self.ciudadOficinas)
            self.acomodarGente()

            self.cementerio=[]
            
           
            #self.distrEdad=self.dtrEdad
            self.RegistroSanos=[]
            self.RegistroMuertos=[]
            self.mortalidadEdadesCovid=mortalidadEdadesCovid
            
        #Metodo que recorre las oficinas de la ciudad y en caso de estas tener vestibulo
        #se agregan a la lista de servicios disponibles
        def rellenarServicios(self):
            for i in self.ciudadOficinas:
                if i.vestibulo!=None:
                    self.serviciosDisponibles.append(i)
        
        #Metodo que elimina servicio de la lista de servicios disponibles
        def bloquearservicio(self,edificio):
            """
            print("_____")
            print("    ")
            print("Edificio "+str(edificio.numeroEdificio) +" bloqueado")
            print("Capacidad :"+ str(len(edificio.vestibulo))+ " / "+str(edificio.aforo) )
            print("    ") 
            print("_____")
            """
            self.serviciosDisponibles.remove(edificio)
        
        #Metodo que agrega servicio a la lista de servicios     
        def desbloquearservicio(self,edificio):
            """
            print("_____")
            print("    ")
            print("Edificio "+str(edificio.numeroEdificio) +" desbloqueado")
            print("Capacidad :"+ str(len(edificio.vestibulo))+ " / "+str(edificio.aforo) )
            print("    ") 
            print("_____")
            self.serviciosDisponibles.append(edificio)
            """
            self.serviciosDisponibles.append(edificio)
            
        #Metodo que devuelve una lista de personas: una poblacion para nuestro caso particular    
        def crearPoblacion(self):
            poblacion=[]
            for i in range(self.numpersonasinicial):
                poblacion.append(Persona(i,self.dtrEdad))         
            return poblacion
         
        #Metodo que crea una lista de listas, que son las oficinas    
        def crearOficinas(self,numpersonas,personasEdificio,maxCapacidad,aforoMedio):
            print(numpersonas,personasEdificio,maxCapacidad,aforoMedio)
            Oficinas=[]
            personasColocadas=0
            edificios=0
            while (numpersonas>personasColocadas):
                personasEsteEdificio=random.randint(int(personasEdificio/2),int((personasEdificio/2)*3))
                if (numpersonas<personasEsteEdificio+personasColocadas):
                    personasEsteEdificio=numpersonas-personasColocadas
                personasColocadas+=personasEsteEdificio

                aforoActual=random.randint(int(aforoMedio/1.5),int(aforoMedio*2))
                EdificioActual=Oficina(numeroEdificio=edificios,capacidadEdificio=personasEsteEdificio,maxCapacidad=maxCapacidad,
                                       aforo=aforoActual, vestibulo=True)
                Oficinas.append(EdificioActual)
                edificios+=1
            return Oficinas
        
        
        def acomodarGente(self):
            personasAcomodadas=0
            for i in self.ciudadViviendas:
                capactual=i.capacidadEdificio
                listaActual=self.CatalogoPersonas[personasAcomodadas:personasAcomodadas+capactual]
                i.acomodar(listaActual)  
                i.meterInicio(listaActual)
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
                
                
                
         #Metodo que simula el paso del tiempo de la simulacion         
        def pasar_tiempo(self,mediaincubacion,desvincubacion,mediaduracion,desvduracion,posibilidadContagio):
            #self.RegistroSanos.append(self.personas_sanas())
            for i in self.ciudadViviendas:
                i.edificioIAS ( self.hora,self)
                i.contagiarEdificio(posibilidadContagio,mediaincubacion,desvincubacion,self.dia)
            for i in self.ciudadOficinas:
                i.edificioIAS ( self.hora,self)
                i.contagiarEdificio(posibilidadContagio,mediaincubacion,desvincubacion,self.dia)   
            if (self.hora<23):
                self.hora+=1
            else:#comienza un nuevo dia
                self.hora=0
                self.dia+=1
                for i in self.ciudadViviendas:
                    #Llamar a las transiciones de estados
                    i.transicionEdificio(self.dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,self.mortalidadEdadesCovid,self)
                for i in self.ciudadOficinas:
                    #Llamar a las transiciones de estados
                #transicionEstados(self.dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,self.mortalidadEdadesCovid)
                     i.transicionEdificio(self.dia, mediaincubacion,desvincubacion,mediaduracion,desvduracion,self.mortalidadEdadesCovid,self)
       
        #Metodo que permite a una persona irse de su lugar actual
        def irse(self,persona):
            if persona.lugarActual[2]==0:
                self.ciudadViviendas[persona.lugarActual[0]].departamentos[persona.lugarActual[1]].remove(persona)
            elif persona.lugarActual[2]==1: 
                
                self.ciudadOficinas[persona.lugarActual[0]].departamentos[persona.lugarActual[1]].remove(persona)
            elif persona.lugarActual[2]==2: 
                self.ciudadOficinas[persona.lugarActual[0]].vestibulo.remove(persona)
                
                if len(self.ciudadOficinas[persona.lugarActual[0]].vestibulo)==self.ciudadOficinas[persona.lugarActual[0]].aforo-1:
                    self.desbloquearservicio(self.ciudadOficinas[persona.lugarActual[0]])
                    #print(self.ciudadOficinas[persona.lugarActual[0]])
        
         #Metodo que permite a una persona ir a un lugar que es diferente del que estaba 
        def meterse(self,persona,lugar,tipolugar):
            if tipolugar==0:
                self.ciudadViviendas[lugar[0]].departamentos[lugar[1]].append(persona)
            elif tipolugar==1: 
                self.ciudadOficinas[lugar[0]].departamentos[lugar[1]].append(persona)
            elif tipolugar==2: 

                self.ciudadOficinas[lugar].vestibulo.append(persona)
                if len(self.ciudadOficinas[lugar].vestibulo)==self.ciudadOficinas[lugar].aforo:
                    self.bloquearservicio(self.ciudadOficinas[lugar])
            elif tipolugar==3:#cementerio
                self.cementerio.append(persona)
        
         #Metodo que crea una lista de listas, que son las viviendas
        def crearViviendas(self,numpersonas,personasEdificio,maxCapacidad):
            Viviendas=[]
            personasColocadas=0
            edificios=0
            while (numpersonas>personasColocadas):
                personasEsteEdificio=random.randint(int(personasEdificio/2),int((personasEdificio/2)*3))
                if (numpersonas<personasEsteEdificio+personasColocadas):
                    personasEsteEdificio=numpersonas-personasColocadas
                personasColocadas+=personasEsteEdificio
                print(f"Num.Edificio: {edificios} , PersonasEdificio: {personasEsteEdificio}, MaxCapacidad: {maxCapacidad}")
                EdificioActual=Vivienda(numeroEdificio=edificios,capacidadEdificio=personasEsteEdificio,maxCapacidad=maxCapacidad)
                Viviendas.append(EdificioActual)
                edificios+=1
            return Viviendas
        
        #Metodo que permite la impresion de los individuos del catalago de personas 
        def printearCatalogo(self):
            for i in self.CatalogoPersonas:
                print(i)
    
         #Metodo que crea a los 'pacientes cero' 
        def contagio_fijo(self, cambioEstadoInicial,numpacientescero):
            personas=rand.sample(self.CatalogoPersonas,k=numpacientescero)
            for i in personas:
                i.estado="asintomatico"
                i.cambioEstado= cambioEstadoInicial
    
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
        
        
         #Funcion que se encarga de mostrar el cementerio 
        def mostrarcementerio(self):
            print()
            if(len(self.cementerio) == 0):
                print("No ha habido ningun fallecido")
            else:
                print("El cementerio es: ") 
                for i in self.cementerio:
                    print(i)
            print()

         #Mostrar los individuos con sus edades pertenecientes a la simulacion              
        def graficoPersonasEdades(self):
            edades=[self.CatalogoPersonas[i].edad for i in range(len(self.CatalogoPersonas))] #obtener en un array las edades de los individuos 
            arr=np.reshape(edades, (len(self.CatalogoPersonas), 1)).T[0]
            plt.hist(arr, bins=50)
            plt.title('Grafico de las edades de los individuos') 
            plt.show()
            print()
        
        #Mostrar un grafico con las personas sanas
        def  graficoPersonasSanas(self): 
           
            for i in range (len(self.CatalogoPersonas)):
                if self.CatalogoPersonas[i].esta_sano() == True:
                    aux = self.CatalogoPersonas[i]
                    self.RegistroSanos.append(aux)
            
            if(len(self.RegistroSanos)) == 0:
                print("No hay ningun sano")
            else:
                edades=[self.RegistroSanos[i].edad for i in range(len(self.RegistroSanos))]
                arr=np.reshape(edades, (len(self.RegistroSanos), 1)).T[0]
                plt.hist(arr, bins=50)
                plt.title('Grafico de las personas sanas por edades ') 
                plt.show()
                print()
        
        #Metodo que se encarga de imprimir las muertes por edades
        #CORREGIIIIRRRR
        def defuncionesPorEdades(self):
            if(len(self.cementerio) == 0):
                print("Nada que imprimir")
            else:
                edades=["0-20", "20-40", "40-60" , "60+"]
                PrimerPorcentaje = 0
                SegundoPorcentaje = 0
                TercerPorcentaje = 0
                CuartoPorcentaje = 0

                for i in range (len(self.cementerio)):
                    if self.cementerio[i].edad <= 20:
                        PrimerPorcentaje += 1
                    elif  20 < self.cementerio[i].edad  <= 40:
                        SegundoPorcentaje += 1
                    elif  40 < self.cementerio[i].edad  <= 60:
                        TercerPorcentaje += 1
                    elif  60 < self.cementerio[i].edad:
                        CuartoPorcentaje += 1
                
                total = len(self.cementerio)
                PrimerPorcentaje = PrimerPorcentaje/total
                SegundoPorcentaje = SegundoPorcentaje/total
                TercerPorcentaje = TercerPorcentaje/total
                CuartoPorcentaje = CuartoPorcentaje/total
                porcentajes= [ PrimerPorcentaje,SegundoPorcentaje,TercerPorcentaje,CuartoPorcentaje ]

                plt.pie(porcentajes, labels=edades)
                plt.axis("equal")
                plt.show()
