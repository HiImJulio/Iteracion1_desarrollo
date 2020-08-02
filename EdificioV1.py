
# coding: utf-8

# In[ ]:


'''
Autores:   Manuel López Amo-Ocón
           Alejangro Galván Pérez-Ilzarbe
           Santiago Cebellán
           Alejandro Meza Tudela
'''


# In[ ]:


#Importacion de librerias
import numpy as np #agrega soporte para vectores y matrices, contituye biblioteca de funciones de alto nivel
from numpy import random #random permite la generacion de numeros aleatorios 
from random import choices #choices esta dedicado a la representacion de pesos 
import os 
import seaborn as sns
import matplotlib.pyplot as plt #Dedicado a la representacion grafica 
from scipy.stats import rv_discrete
import pandas as pd


# In[ ]:


#Clase que representa un edificio
'''
Lista de atributos: 
                   personasEdificio: media de personas por edificio
                   capacidadEdificio: entero que representa la capacidad de habitantes o huespedes del edificio
                   numeroEdificio: identificador del edificio 
                   tipoEdificio: array que contiene los posibles tipos de edificios de la ciudad
'''
class Edificio:
    def __init__(self,personasedificio):
        self.personasEdificio = personasedificio
        self.capacidadEdificio = random.randint(1,personasedificio*3) #entero que representa la capacidad de este edificio 
        self.numeroEdificio #entero que representa un identificador del edificio
        self.tipoEdificio = ["Oficinas", "Viviendas"] 
    
    #Metodo que imprime los atributos de la clase
    def __str__(self):
            return str(self.personasEdificio) + "," + str(self.capacidadEdificio) + "," + str(self.numeroEdificio) + "," +str(self.tipoEdifico)   
        

