import threading as th
import random as rd
import time
import math


class Celula(th.Thread):
    def __init__(self, id, tipo):
        super().__init__()
        self.id = id
        self.tipo = tipo  # 'alien' o 'humano'
        self.infectada = False
        self.ronda_infeccion = None
        self.pareja = None
        self.lock = th.Lock()
        self.shutdown = th.Event()
        
    def set_pareja(self,pareja):
        self.pareja = pareja
    
    def infectar(self, ronda):
        if self.tipo == 'humano':  # Solo humanos pueden infectarse
            self.infectada = True
            self.ronda_infeccion = ronda
            
    # La función se ejecuta al iniciar la hebra
    def run(self):
        # Se inicializa la variable ronda
        ronda = 1
        
        # Se sigue ejecutando si es que no se ha activado el shutdown
        while not self.shutdown.is_set():
            
            # Se espera que todas las demás hebras estén listas y el padre otorgue la luz verde
            barrera.wait()
            
            # No se trabaja hasta que se asigne una pareja
            while self.pareja == None:
                time.sleep(0.1)
               
            # Se ordenan los lock para que siempre se ejecuten en el mismo orden (previene deadlocks)
            primero,segundo = ((self.lock,self.pareja.lock) if self.id < self.pareja.id else (self.pareja.lock,self.lock))
            
            # Solo 1 hebra entra a la vez
            with primero:
                with segundo:
                    if self.tipo == 'alien' and self.pareja.tipo == 'humano':
                        if rd.randint(1,10) <= 7:
                            self.pareja.infectar(ronda)
                    
                    self.pareja = None
            
            ronda += 1
            barrera2.wait()
            # La hebra con el id más grande se encarga de escribir el enfrentamiento
            '''
            with primero:
                with segundo:
                    if self.id > self.pareja.id:
            '''
                

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
        
        for enfrentamiento in enfrentamientos:
            resultado = ""
            cel1 = enfrentamiento[0]
            cel2 = enfrentamiento[1]
            
            if cel1.tipo == cel2.tipo == 'humano' and not cel1.infectada and not cel2.infectada:
                resultado = "Las 2 celulas son humanas, no ocurrio nada."

            elif cel1.tipo == cel2.tipo == 'alien':
                resultado = "Las 2 celulas alienigenas intentan cooperar entre ellas."

            elif (cel1.tipo == 'humano' and cel1.infectada and cel1.ronda_infeccion != ronda and cel2.tipo == 'alien') or (cel2.tipo == 'humano' and cel2.infectada and cel2.ronda_infeccion != ronda and cel1.tipo == 'alien'):
                resultado = "Una celula humana infectada intenta colaborar con una alienigena."
                
            elif cel1.infectada and cel2.infectada and cel1.ronda_infeccion != ronda and cel2.ronda_infeccion != ronda:
                resultado = f"Ambas celulas infectadas intentan cooperar entre ellas"

            # Infección exitosa
            elif cel1.tipo == 'humano' and cel1.infectada and cel2.ronda_infeccion == ronda:
                resultado = f"La celula{cel2.id} (infectada) ha infectado a celula{cel1.id} (humana)"

            elif cel2.tipo == 'humano' and cel2.infectada and cel1.ronda_infeccion == ronda:
                resultado = f"La celula{cel1.id} (infectada) ha infectado a celula{cel2.id} (humana)"
                
            elif cel1.tipo == 'alien' and cel2.ronda_infeccion == ronda:
                resultado = f"La celula{cel1.id} (alienigena) ha infectado a celula{cel2.id} (humana)"
                
            elif cel2.tipo == 'alien' and cel1.ronda_infeccion == ronda:
                resultado = f"La celula{cel2.id} (infectada) ha infectado a celula{cel1.id} (humana)"
                
            # Fracaso al infectar
            elif cel1.tipo == 'humano' and cel1.infectada and not cel2.infectada:
                resultado = f"La celula{cel1.id} (infectada) fracaso al intentar infectar a celula{cel2.id} (humana)"

            elif cel1.tipo == 'alien' and not cel2.infectada:
                resultado = f"La celula{cel1.id} (alienigena) fracaso al intentar infectar a celula{cel2.id} (humana)"
                
            elif cel2.tipo == 'humano' and cel2.infectada and not cel1.infectada:
                resultado = f"La celula{cel2.id} (infectada) fracaso al intentar infectar a celula{cel1.id} (humana)"

            elif cel2.tipo == 'alien' and not cel1.infectada:
                resultado = f"La celula{cel2.id} (alienigena) fracaso al intentar infectar a celula{cel1.id} (humana)"

            else:
                resultado = "No se pudo determinar lo que ocurrio."
                    
            f.write(f"Celula{cel1.id} vs Celula{cel2.id}: {resultado}\n")

def logica_rondas(rondas, celulas):
    
    for celula in celulas:
        celula.start()
    
    for ronda in range(1,rondas+1):
        
        print("Ronda " + str(ronda))
        enfrentamientos = []
        t_in = time.time()
        
        rd.shuffle(celulas)
            
        celulas1 = celulas[:math.floor(len(celulas)/2)]
        celulas2 = celulas[math.floor(len(celulas)/2):]
        
        for i,j in zip(celulas1,celulas2):
            enfrentamientos.append([i,j])
            i.set_pareja(j)
            j.set_pareja(i)

        barrera.wait()
                
        while time.time() - t_in < 1:
            time.sleep(0.1)
        
        if ronda == rondas:
            for celula in celulas:
                celula.shutdown.set()   
        
        barrera2.wait()
        
        print("Escribiendo ronda " + str(ronda))
        
        escribir_ronda(ronda, enfrentamientos)
        
        print("Ronda " + str(ronda) + " escrita")

    
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
            f.write(f"{celula.id}\t{celula.tipo} (infectada {celula.ronda_infeccion})\n" if (celula.tipo == 'humano' and celula.infectada) else f"{celula.id}\t{celula.tipo}\n")

def main_bonus():
    a = 0
    print("main_bonus")

def main_base():
    global barrera
    global barrera2
    barrera = th.Barrier(513)
    barrera2 = th.Barrier(513)
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
     


def main():
    bonus = False
    print("Quiere ejecutar el BONUS? (Por ahora no hay)")
    print("No : 0")
    print("Si : 1")
    bonus = int(input())
    if bonus:
        main_base()
    else:
        main_base()
    
if __name__ == "__main__":
    main()