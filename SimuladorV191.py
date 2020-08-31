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
import time
from IPython.display import clear_output

from random import choices #choices esta dedicado a la representacion de pesos 
import os 
import seaborn as sns
import matplotlib.pyplot as plt #Dedicado a la representacion grafica 
from scipy.stats import rv_discrete
import pandas as pd



from PersonaV19 import * #importacion de la clase persona
from EdificioV19 import * #importacio de la clase edificio


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
            self.tInicial = time.time()
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
             #metodo que se procedera a describir a continuacion
            self.CatalogoPersonas=self.crearPoblacion()
            self.acomodarGente()
            self.rellenarServicios()
            self.cementerio=[]
            
           
            #self.distrEdad=self.dtrEdad
            self.RegistroSanos=[]
            self.RegistroInfectados = []
            self.RegistroMuertos=[]
            self.mortalidadEdadesCovid=mortalidadEdadesCovid
            
            
            self.tiempoCreacion=time.time()- self.tInicial
            self.tiemposPorDias=[]
            self.tiemposPorHoras=[]
            
        def mostrarTiempo(self): 
            print("El simulador ha tardado "+ str(self.tiempoCreacion) +" en crearse." )
            
            if len(self.tiemposPorDias)>0:
                print("El simulador ha tardado "+ str(sum(self.tiemposPorDias)/len(self.tiemposPorDias)) +" de media en simular un dia." )
                print("El simulador ha tardado "+ str(sum(self.tiemposPorDias)/(len(self.tiemposPorDias)*24)) +" de media en simular una hora." )
                print("El simulador ha tardado "+ str(sum(self.tiemposPorDias)) +" en simular "+str(len(self.tiemposPorDias)) +" dias." )

        #Metodo que recorre las oficinas de la ciudad y en caso de estas tener vestibulo
        #se agregan a la lista de servicios disponibles
        def rellenarServicios(self):
            for i in self.ciudadOficinas:
                if i.vestibulo!=None and i.edificioAbierto[0]==True:
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
            #print(numpersonas,personasEdificio,maxCapacidad,aforoMedio)
            Oficinas=[]
            personasColocadas=0
            edificios=0
            while (numpersonas>personasColocadas):
                personasEsteEdificio=random.randint(int(personasEdificio/2),int((personasEdificio/2)*3))
                if (numpersonas<personasEsteEdificio+personasColocadas):
                    personasEsteEdificio=numpersonas-personasColocadas
                personasColocadas+=personasEsteEdificio

                aforoActual=random.randint(int(aforoMedio/2),int(aforoMedio*1.5))
                EdificioActual=Oficina(numeroEdificio=edificios,capacidadEdificio=personasEsteEdificio,maxCapacidad=maxCapacidad,
                                       aforo=aforoActual, vestibulo=True)
                #print(f"Num.Edificio: {edificios} , PersonasEdificio: {personasEsteEdificio}, MaxCapacidad: {maxCapacidad}, aforo: {aforoActual}")
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
            t_inicio=time.time()
            self.RegistroSanos.append(self.personas_sanas())
            self.RegistroInfectados.append(self.personas_infectadas())
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
                    
            for i in self.ciudadOficinas:                
                i.abrirCerrar(self.hora, self)        
                         
            for i in self.CatalogoPersonas:
                if i.estado!="muerto":
                    i.simular_ia( self.hora,self) 
            
            for i in self.ciudadViviendas:               
                i.contagiarEdificio(posibilidadContagio,mediaincubacion,desvincubacion,self.dia)
            for i in self.ciudadOficinas:                
                i.contagiarEdificio(posibilidadContagio,mediaincubacion,desvincubacion,self.dia)   
            
            
            t_final=time.time()-t_inicio
            self.tiemposPorHoras.append(t_final)
            if len(self.tiemposPorHoras)==24:
                self.tiemposPorDias.append(sum(self.tiemposPorHoras))
                self.tiemposPorHoras=[]
                
                
                
                
       
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
                i.estado="incubandoContagioso"
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
        def graficoPersonasSanasActuales(self): 
            RegistroSanosActuales=[]
            for i in range (len(self.CatalogoPersonas)):
                if self.CatalogoPersonas[i].esta_sano() == True:
                    aux = self.CatalogoPersonas[i]
                    RegistroSanosActuales.append(aux)
            
            if(len(self.RegistroSanos)) == 0:
                print("No hay ningun sano")
            else:
                edades=[RegistroSanosActuales[i].edad for i in range(len(RegistroSanosActuales))]
                arr=np.reshape(edades, (len(RegistroSanosActuales), 1)).T[0]
                plt.subplot()
                plt.hist(arr, bins=50)
                plt.title('Grafico de las personas sanas por edades ') 
                plt.show()
                print()
        
        
        #Metodo que se encarga de imprimir las personas por horas
        def  graficoPersonasSanas(self):         
            arr=np.reshape(self.RegistroSanos, (len(self.RegistroSanos), 1)).T[0]
            data=pd.DataFrame({'horas':range(0,len(self.RegistroSanos)),'personas_sanas':arr})
            
            plt.figure()
            sns.relplot(x="horas",y="personas_sanas", kind="line", data=data)
            plt.show()
            
        #Metodo que se encarga de imprimir las personas infectadas por horas
        def  graficoPersonasInfectadas(self):   
            arr=np.reshape(self.RegistroInfectados, (len(self.RegistroInfectados), 1)).T[0]
            data=pd.DataFrame({'horas':range(0,len(self.RegistroInfectados)),'personas_infectadas':arr})
            sns.set()
            sns.relplot(x="horas",y="personas_infectadas", kind="line", data=data)
     
            
        #Función que devuelve el total de personas sanas o que ya pasaron la enfermedad de la ciudad
        def personas_sanas(self):
            contador_sanos=0
            for j in self.CatalogoPersonas: #se recorre los edificios de la ciudad
                #se va recorriendo las personas del catalogo
                if j.esta_sano():
                     contador_sanos+=1
            return contador_sanos
        
        
        #Función que devuelve el total de personas infectadas
        def personas_infectadas(self):
            contador_infectados = 0
            for j in self.CatalogoPersonas:
                if j.esta_sano() != True:
                    contador_infectados +=1              
            return contador_infectados 
        
        
        def defuncionesPorEdades(self):
            if(len(self.cementerio) == 0):
                print("Nada que imprimir")
            else:
                PrimeraDivision = 0
                SegundaDivision = 0
                TerceraDivision = 0
                CuartaDivision = 0
                divisiones = []
                edades=[]

                for i in range (len(self.cementerio)):
                    if self.cementerio[i].edad <= 20:
                        PrimeraDivision += 1
                    elif  20 < self.cementerio[i].edad  <= 40:
                        SegundaDivision += 1
                    elif  40 < self.cementerio[i].edad  <= 60:
                        TerceraDivision += 1
                    elif  60 < self.cementerio[i].edad:
                        CuartaDivision += 1
                
                
                if PrimeraDivision > 0:
                    divisiones.append(PrimeraDivision)
                    edades.append("0-20")
                    
                if SegundaDivision > 0:
                    divisiones.append(SegundaDivision)
                    edades.append("20-40")
                    
                if TerceraDivision > 0:
                    divisiones.append(TerceraDivision)
                    edades.append("40-60")
                    
                if CuartaDivision > 0:
                    divisiones.append(CuartaDivision)
                    edades.append("60+")
                              
                plt.subplot()
                plt.bar(edades,divisiones, color ='maroon', width = 0.4)
                plt.xlabel("Edades de personas") 
                plt.ylabel("Numero de defunciones ") 
                plt.title('Defuncion por edades ') 
                plt.show()
                
                for i in range (len(divisiones)):
                    print(f"Franja edad {i+1} - numero muertos {divisiones[i]}")
                    
                                     
                    
                           
        def menuGraficas(self):
            sns.set()
            print("¡Welcome! Este es el menu que permite la visualizacion de algunas graficas")
            while True:
                print("Elige la grafica que deseas ver! pulsando 0 veras las opcciones disponibles")
                
                eleccion = (int)(input("Mi eleccion es: "))
                clear_output(wait=True)   
                if(eleccion ==0):
                    print("¿Que deseas ver?")
                    print("1- Mostrar cementerio")
                    print("2- Mostrar grafico con las edades de las personas")
                    print("3- Mostrar grafico con las personas sanas ahora mismo")
                    print("4- Mostrar el numero de defunciones por edades")
                    print("5- Mostrar las personas sanas a lo largo de la simulacion")
                    print("6- Mostrar los tiempos de ejecucuion del simulador")
                    print("7- Mostrar las personas infectadas a lo largo de la simulacion")
                    print("-1 Salir del menu, Tschüs!!")
                    
                 
                if(eleccion ==1):
                    self.mostrarcementerio()
                    print()
                elif(eleccion == 2):
                    self.graficoPersonasEdades()
                    print()
                elif(eleccion == 3):
                    self.graficoPersonasSanasActuales()
                    print()
                elif(eleccion == 4):
                    self.defuncionesPorEdades()
                    print()
                elif(eleccion == 5):
                    self.graficoPersonasSanas()
                    print()
                elif(eleccion == 6):
                    self.mostrarTiempo()
                    print()
                elif(eleccion == 7):
                    self.graficoPersonasInfectadas()
                    print()
                elif(eleccion == -1):
                    break
                
            print("Bye Bye")
