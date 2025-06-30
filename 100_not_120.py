import threading as th
import random as rd
import time
import math

class Celula(th.Thread):
    def __init__(self, id, tipo):
        '''
        Clase para cada célula como una hebra independiente

        Atributos
        id: identificador único
        tipo: 'alien' o 'humano'
        
        infectada: booleano de infeccion
        ronda_infeccion: ronda en la que se infecta
        infectado_por: id de quien la infecta
        
        pareja: pareja del enfrentamiento actual
        lock: Lock para la sincronización
        shutdown: Evento para terminar la hebra
        '''
        super().__init__()
        self.id = id
        self.tipo = tipo 
        self.infectada = False if tipo == 'humano' else True
        self.ronda_infeccion = None
        self.infectado_por = None
        self.pareja = None
        self.lock = th.Lock()
        self.shutdown = th.Event()
        
    def set_pareja(self,pareja):
        # Asigna pareja
        self.pareja = pareja
    
    def infectar(self, ronda, id_infectado):
        # Infecta humanos, solo humanos
        if self.tipo == 'humano':
            self.infectada = True
            self.ronda_infeccion = ronda
            self.infectado_por = id_infectado
            
    # La función se ejecuta al iniciar la hebra
    def run(self):

        # Se sigue ejecutando si es que no se ha activado el shutdown
        while not self.shutdown.is_set():
            
            # Se espera que todas las demás hebras estén listas y el padre otorgue la luz verde
            barrera.wait()

            # Se revisa si es que se asigno una pareja
            if self.pareja != None:
                # Se ordenan los lock para que siempre se ejecuten en el mismo orden (previene deadlocks)
                primero,segundo = ((self.lock,self.pareja.lock) if self.id < self.pareja.id else (self.pareja.lock,self.lock))
                
                # Solo 1 hebra entra a la vez
                with primero:
                    with segundo:
                        if self.tipo == 'alien' and self.pareja.tipo == 'humano' and not self.pareja.infectada:
                            if rd.randint(1,10) <= 7:
                                with lock_ronda:
                                    self.pareja.infectar(ronda, self.id)
                        
                        self.pareja = None
            
            barrera2.wait()
            barrera3.wait()
            # La hebra con el id más grande se encarga de escribir el enfrentamiento
            '''
            with primero:
                with segundo:
                    if self.id > self.pareja.id:
            '''

# EHhh, más o menos
class Anticuerpo(th.Thread):
    def __init__(self):
        super().__init__()
        self.lock = th.Lock()
        self.shutdown = th.Event()
    
    def curar(self, celula_1):
        celula_1.tipo = "humano"
        return celula_1
    
    def eliminar(self, celula_alien, pos):
        celula_alien.shutdown.set()
        del celulas[pos]

    def run(self):
        # Se sigue ejecutando si es que no se ha activado el shutdown
        while not self.shutdown.is_set():
            
            if ronda >= 2:
                pos_ant = rd.sample(range(len(celulas)), 4)
                ataca = True
                # Solo 1 hebra entra a la vez
                for pos in pos_ant:
                    with self.lock:
                        with celulas[pos].lock:
                            with lock_ronda:
                                if celulas[pos].tipo == 'alien':
                                    self.eliminar(celulas[pos], pos)
                                    ataca = True
                                elif celulas[pos].tipo == 'humano' and celulas[pos].ronda_infeccion != None:
                                    if ronda - celulas[pos].ronda_infeccion  <= 2:
                                        celulas[pos] = self.curar(celulas[pos])
                                        ataca= False
                    enf_anti.append([ronda, pos, ataca, celulas[pos].tipo])

            # Se espera que todas las demás hebras estén listas y el padre otorgue la luz verde
            barrera_anti.wait()
            barrera_anti.wait()


def crear_celulas(celulas_totales, cel_alien):
    # crea celulas iniciales
    
    # ids de todas las celulas
    posiciones = list(range(celulas_totales))
    
    # Seleccionar 16 ids aleatorios para aliens
    pos_alien = rd.sample(posiciones, cel_alien)

    # Crear lista de células
    celulas = []
    
    for pos in posiciones:
        # crea celulas con los tipos correspondientes
        tipo = 'alien' if pos in pos_alien else 'humano'
        celula = Celula(pos, tipo)
        celulas.append(celula)
    
    return celulas

def escribir_ronda(ronda_a, enfrentamientos, first):

    # escribe los archivos ronda1.txt, ronda2.txt, ...
    nombre_archivo = f"ronda_{ronda_a}.txt"
    with open(nombre_archivo, "a") as f:
        
        # Si es la primera vez que se llama se escribe el titulo
        if first:
            f.write(f"=== RONDA {ronda_a} ===\n")
        
        # Se escriben los enfrentamientos, está feo pero funciona
        for enfrentamiento in enfrentamientos:
            resultado = ""
            cel1 = enfrentamiento[0]
            cel2 = enfrentamiento[1]
            
            
            if cel1.tipo == cel2.tipo == 'humano' and not cel1.infectada and not cel2.infectada:
                resultado = "Las 2 celulas son humanas, no ocurrio nada."

            elif cel1.tipo == cel2.tipo == 'alien':
                resultado = "Las 2 celulas alienigenas intentan cooperar entre ellas."

            elif (cel1.tipo == 'humano' and cel1.infectada and cel1.ronda_infeccion != ronda_a and cel1.infectado_por == cel2.id and cel2.tipo == 'alien') or (cel2.tipo == 'humano' and cel2.infectada and cel2.ronda_infeccion != ronda_a and cel2.infectado_por == cel1.id and cel1.tipo == 'alien'):
                resultado = "Una celula humana infectada intenta colaborar con una alienigena."
                
            elif cel1.infectada and cel2.infectada and cel1.infectado_por != cel2.id and cel1.infectado_por != cel1.id:
                resultado = f"Ambas celulas infectadas intentan cooperar entre ellas"

            # Infección exitosa
            elif cel1.tipo == 'humano' and cel1.infectada and cel2.ronda_infeccion == ronda_a and cel1.infectado_por == cel2.id:
                resultado = f"La celula{cel2.id} (infectada) ha infectado a celula{cel1.id} (humana)"

            elif cel2.tipo == 'humano' and cel2.infectada and cel1.ronda_infeccion == ronda_a and cel2.infectado_por == cel1.id:
                resultado = f"La celula{cel1.id} (infectada) ha infectado a celula{cel2.id} (humana)"
                
            elif cel1.tipo == 'alien' and cel2.ronda_infeccion == ronda_a and cel2.infectado_por == cel1.id:
                resultado = f"La celula{cel1.id} (alienigena) ha infectado a celula{cel2.id} (humana)"
                
            elif cel2.tipo == 'alien' and cel1.ronda_infeccion == ronda_a and cel1.infectado_por == cel2.id:
                resultado = f"La celula{cel2.id} (alienigena) ha infectado a celula{cel1.id} (humana)"
                
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
                resultado = "No se pudo determinar lo que ocurrio (Esto no debería pasar mucho)."
                    
            f.write(f"Celula{cel1.id} vs Celula{cel2.id}: {resultado}\n")

def logica_rondas(rondas, celulas):
    
    started = False
    ronda = 1
    
    # Creamos los archivos
    for i in range(1,rondas+1):
        nombre_archivo = f"ronda_{ronda}.txt"
    
        with open(nombre_archivo, "w") as f:
            pass
            
    # loop para las rondas
    for i in range(1,rondas+1):
        
        # Iniciamos las hebras
        if not started:
            for celula in celulas:
                celula.start()
                started = True
        
        # Mensaje por pantalla y variables para control de tiempo y escritura de archivo
        print("Ronda " + str(ronda))
        enfrentamientos = []
        first = True
        t_in = time.time()
        
        # Mensaje por pantalla
        print("Escribiendo ronda " + str(ronda))
        
        # Loop de tiempo
        while time.time() - t_in < 10:
            enfrentamientos = []
            
            # mezclamos las celulas, tomamos dos grandes grupos
            rd.shuffle(celulas)
            celulas1 = celulas[:math.floor(len(celulas)/2)]
            celulas2 = celulas[math.floor(len(celulas)/2):]
            
            # Seteamos las parejas
            for i,j in zip(celulas1,celulas2):
                enfrentamientos.append([i,j])
                i.set_pareja(j)
                j.set_pareja(i)
            
            # Esperamos a que todos estén listos y damos luz verde
            barrera.wait()

            # Esperamos a que todos terminen
            barrera2.wait()
            
            # Escribimos los resultados de la ronda
            escribir_ronda(ronda, enfrentamientos, first)
            
            # Para no escribir el titulo del archivo más de una vez
            if first:
                first = False
            
            # Esperamos a que todos terminen
            barrera3.wait()
        
        barrera.wait()
        
        # Si terminamos las rondas terminamos todas las hebras
        if ronda == rondas:
            for celula in celulas:
                celula.shutdown.set()   
        
        # La variable ronda es global y evitamos condicion de carrera al acceder a ella
        with lock_ronda:
            ronda = ronda + 1
        
        # De nuevo, esperamos a que todos terminen
        barrera2.wait()
        barrera3.wait()
    
    return celulas

def escribir_aislamiento(celulas):
    
    # Sencillo, escribimos las ids y su tipo
    
    with open("aislamiento.txt", "w") as f:
        f.write("ID\tTipo_Inicial\n")
        for celula in celulas:
            f.write(f"{celula.id}\t{celula.tipo}\n")

def escribir_final(celulas):
    
    # Sencillo, escribimos las ids y su tipo, si fueron infectadas pasan a ser alien

    with open("diagnostico_final.txt", "w") as f:
        
        f.write("ID\tTipo_Final\n")
        
        for celula in celulas:
            if (celula.tipo == 'humano' and celula.infectada):
                celula.tipo = "alien"
                f.write(f"{celula.id}\t{celula.tipo} (infectada {celula.ronda_infeccion})\n")
            else:
                f.write(f"{celula.id}\t{celula.tipo}\n")

# NO Listo
def escribir_anticuerpo():
    with open("acciones_anticuerpo.txt", "w") as f:
        
        f.write("ID\tTipo_Final\n")
        
        for enfrentamiento in enf_anti:
            if enfrentamiento[2]:
                if enfrentamiento[3] == "alien":
                    f.write(f"Ronda {enfrentamiento[0]}\t - \t Ataca Célula {enfrentamiento[1]} (Alienigena) - Resultado: Eliminada\n")
                else:
                    f.write(f"Ronda {enfrentamiento[0]}\t - \t Ataca Célula {enfrentamiento[1]} - (Humana) Resultado: No afecta\n")
            else:
                f.write(f"Ronda {enfrentamiento[0]}\t - \t Cura Célula {enfrentamiento[1]} - (Infectada) Resultado: Curada\n")

# Raro
def log_ronda_anti(rondas, celulas, anticuerpo):
    started = False
    ronda = 1

    for i in range(1,rondas+1):
        nombre_archivo = f"ronda_{ronda}.txt"
    
        with open(nombre_archivo, "w") as f:
            pass
    
    for i in range(1,rondas+1):

        with lock_ronda:
            ronda = i

        if not started:
            for celula in celulas:
                celula.start()
            anticuerpo.start()
            started = True
        
        print("Ronda " + str(ronda))
        enfrentamientos = []
        first = True
        t_in = time.time()
        
        print("Escribiendo ronda " + str(ronda))
        barrera_anti.wait()
        while time.time() - t_in < 1:
            enfrentamientos = []
            rd.shuffle(celulas)
            celulas1 = celulas[:math.floor(len(celulas)/2)]
            celulas2 = celulas[math.floor(len(celulas)/2):]
            
            for i,j in zip(celulas1,celulas2):
                enfrentamientos.append([i,j])
                i.set_pareja(j)
                j.set_pareja(i)
            
            barrera.wait()
            barrera2.wait()
            
            escribir_ronda(ronda, enfrentamientos, first)
            if first:
                first = False
            
            barrera3.wait()
        
        barrera.wait()
        
        if ronda == rondas:
            for celula in celulas:
                celula.shutdown.set()   
            anticuerpo.shutdown.set()
        
        
        with lock_ronda:
            ronda = ronda + 1
        
        barrera_anti.wait()
        barrera2.wait()
        barrera3.wait()
    
    return celulas

def main_bonus():
    # Un monton de variables globales para el control y la sicnronización
    global barrera_anti
    global barrera
    global barrera2
    global barrera3
    global celulas
    global enf_anti
    global ronda
    global lock_ronda
    
    # Inicializaciones 
    ronda = 1
    lock_ronda = th.Lock()
    enf_anti = []
    
    # Creamos las celulas
    celulas = crear_celulas(512, 16)
    
    # Creamos las barreras
    barrera = th.Barrier(513)
    barrera2 = th.Barrier(513)
    barrera3 = th.Barrier(513)
    barrera_anti = th.Barrier(2)
    
    # Creamos al anticuerpo
    anticuerpo = Anticuerpo()
    
    # Mensaje por pantalla
    print("main_bonus")
    
    # Escribimos al aislamiento
    escribir_aislamiento(celulas)
    
    # Preguntas para saber cuantas rondas simular (Minimo 5)
    print("Cuántas rondas simulará? (El mínimo es 5)")
    rond_jug = int(input())
    
    if rond_jug <= 5:
        print("El mínimo es 5")
        rond_jug = 5
    
    
    # Ejecutamos las rondas y retornamos las celulas
    celulas = log_ronda_anti(rond_jug, celulas, anticuerpo)
    
    # Escribimos el archivo final
    escribir_final(celulas)
    
    # Escribimos las acciones del anticuerpo
    escribir_anticuerpo()

def main_base():
    # Un monton de variables globales para el control y la sicnronización
    global barrera
    global barrera2
    global barrera3
    global ronda
    global lock_ronda
    
    # Inicializaciones de locks y barreras, además de la ronda
    lock_ronda = th.Lock()
    barrera = th.Barrier(513)
    barrera2 = th.Barrier(513)
    barrera3 = th.Barrier(513)
    ronda = 1
    
    # Mensaje por pantalla
    print("main_base")
    
    # Creamos las celulas
    celulas = crear_celulas(512, 16)

    # Preguntas para saber cuantas rondas simular (Minimo 5)
    print("Cuántas rondas simulará? (El mínimo es 5)")
    rondas = int(input())
    
    if rondas <= 5:
        print("El mínimo es 5")
        rondas = 5

    # Escribimos al aislamiento
    escribir_aislamiento(celulas)
    
    # Ejecutamos las rondas y retornamos las celulas
    celulas = logica_rondas(rondas, celulas)
    
    # Escribimos el archivo final
    escribir_final(celulas)

def main():
    # Booleanos para el bonus
    bonus = False
    
    # Preguntamos
    print("Quiere ejecutar el BONUS? (Se ejecuta pero el archivo de salida está defectuoso)")
    print("No : 0")
    print("Si : 1")
    
    # Tomamos la respuesta y ejecutamos según corresponda
    bonus = int(input())
    if bonus:
        main_bonus()
    else:
        main_base()


# Inicio de todo
if __name__ == "__main__":
    main()