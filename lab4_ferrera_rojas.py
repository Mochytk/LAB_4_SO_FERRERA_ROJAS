import threading as th
import random as rd
import time
import math

class Celula(th.Thread):
    def __init__(self, id, tipo):
        self.id = id
        self.tipo = tipo  # 'alien' o 'humano'
        self.infectada = False
        self.ronda_infeccion = None
        self.lock = th.Lock()

def logica_rondas(rondas, celulas):
    while rondas:
        t_in = time.time()
        while time.time() - t_in <= 10:
            pos_1 = rd.random(0, 511)
            pos_2 = rd.random(0, 511)
            celula_1 = celulas[pos_1]
            celula_2 = celulas[pos_2]
            if pos_1 != pos_2:
                celula_1, celula_2 = enfrentamiento(celula_1, celula_2)
                # escribir en el archivo rondas
        rondas -= 1

def enfrentamiento(celula_1, celula_2):
    if celula_1.tipo == "alien" and celula_2.tipo == "humano":
        if rd.random() > 0.3:
            celula_2.tipo = "alien"
    if celula_2.tipo == "alien" and celula_1.tipo == "humano":
        if rd.random() > 0.3:
            celula_1.tipo = "alien"
    return celula_1, celula_2

def main_bonus():
    a = 0
    print("main_bonus")

def main_base():
    a = 0
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