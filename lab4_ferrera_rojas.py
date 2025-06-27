import threading as th
import random as rd
import time
import math

from regex import T

class Celula(th.Thread):
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo  # 'alien' o 'humano'
        self.infectada = False
        self.ronda_infeccion = None
        self.lock = th.Lock()

    def infectar(self, ronda):
        with self.lock:
            if self.tipo == 'humana':
                self.tipo = 'alien'
                self.infectada = True
                self.ronda_infeccion = ronda
    
def crear_celulas_base(total_celulas = 512, aliens_iniciales = 16):
    # Números del 0 al 511 (ids de cada celula)
    tot_cel = list(range(total_celulas))
    cel_ali = rd.sample(tot_cel, aliens_iniciales)

    celulas = []

    for id in tot_cel:

        if id in cel_ali:
            tipo = 'alien'
        else:
            tipo = 'humano'

        celula = Celula(id, tipo)
        celulas.append(celula)

    return celulas

def main_bonus():
    print("main_bonus")

def main_base():
    celulas = crear_celulas_base()
    
    print("main_base")

bonus = False
print("Quiere ejecutar el BONUS? (Por ahora no hay)")
print("No : 0")
print("Si : 1")
bonus = int(input())
if bonus:
    main_bonus()
else:
    main_base()