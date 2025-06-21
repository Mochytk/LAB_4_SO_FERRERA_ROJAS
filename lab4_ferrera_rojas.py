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