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
    
    def infectar(self, ronda):
        with self.lock:
            if self.tipo == 'humano':  # Solo humanos pueden infectarse
                self.tipo = 'alien'
                self.infectada = True
                self.ronda_infeccion = ronda

def crear_celulas(celulas_totales, cel_alien):
    posiciones = list(range(celulas_totales))
    
    # Seleccionar 16 IDs aleatorios para aliens
    pos_alien = rd.sample(posiciones, cel_alien)

    # Crear lista de células
    celulas = []
    
    for pos in posiciones:
        
        tipo = 'alien' if pos in pos_alien else 'humano'
        celula = Celula(pos, tipo)
        celulas.append(celula)
    
    return celulas

def escribir_ronda(ronda, enfrentamientos):
    nombre_archivo = f"ronda_{ronda}.txt"
    
    with open(nombre_archivo, "w") as f:
        
        f.write(f"=== RONDA {ronda} ===\n")
        
        for cel1, cel2, resultado in enfrentamientos:
            f.write(f"Celula{cel1.id} vs Celula{cel2.id}: {resultado}\n")

def logica_rondas(rondas, celulas):
    
    ronda = 0
    enfrentamientos = []
    
    while ronda < rondas:
        
        print("Ronda " + str(ronda))
        t_in = time.time()
        
        while time.time() - t_in <= 10:
            
            pos_1 = rd.randrange(0, 511)
            pos_2 = rd.randrange(0, 511)
            
            celula_1 = celulas[pos_1]
            celula_2 = celulas[pos_2]
            
            if pos_1 != pos_2:
                
                celula_1, celula_2 = enfrentamiento(celula_1, celula_2, ronda)
                
                if celula_1.infectada and celula_1.ronda_infeccion == ronda:
                    resultado = str(celula_1.id) + " infectada"
                
                elif celula_2.infectada and celula_2.ronda_infeccion == ronda:
                    resultado = str(celula_2.id) + " infectada"
                
                else:
                    resultado = "Nada pasó"
                
                enfrentamientos.append([celula_1, celula_2, resultado])
        
        print("Escribiendo ronda " + str(ronda))
        
        escribir_ronda(ronda, enfrentamientos)
        
        print("Ronda " + str(ronda) + " escrita")
        
        ronda += 1
    
    return celulas

def enfrentamiento(celula_1, celula_2, ronda):
    if celula_1.tipo == "alien":
        if rd.random() > 0.3:
            celula_2.infectar(ronda)
    if celula_2.tipo == "alien":
        if rd.random() > 0.3:
            celula_1.infectar(ronda)
    return celula_1, celula_2

def escribir_aislamiento(celulas):
    with open("aislamiento.txt", "w") as f:
        f.write("ID\tTipo_Inicial\n")
        for celula in celulas:
            f.write(f"{celula.id}\t{celula.tipo}\n")

def escribir_final(celulas):
    with open("diagnostico_final.txt", "w") as f:
        f.write("ID\tTipo_Final\n")
        for celula in celulas:
            f.write(f"{celula.id}\t{celula.tipo}\n")

def main_bonus():
    a = 0
    print("main_bonus")

def main_base():
    print("main_base")
    celulas = crear_celulas(512, 16)
    
    print("Cuántas rondas simulará? (El mínimo es 5)")
    rond_jug = int(input())
    
    if rond_jug <= 5:
        print("El mínimo es 5")
        rond_jug = 5

    escribir_aislamiento(celulas)
    
    celulas = logica_rondas(rond_jug, celulas)
    
    escribir_final(celulas)

bonus = False
print("Quiere ejecutar el BONUS? (Por ahora no hay)")
print("No : 0")
print("Si : 1")
bonus = int(input())
if bonus:
    main_base()
else:
    main_base()