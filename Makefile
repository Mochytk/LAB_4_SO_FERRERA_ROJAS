PYTHON = python3
SCRIPT = LAB4_ferrera_rojas.py
OUTPUT_FILES = aislamiento.txt diagnostico_final.txt ronda_*.txt acciones_anticuerpo.txt

.PHONY: all run clean

all: run

run:
	@echo "Ejecutando simulación..."
	@$(PYTHON) $(SCRIPT)
	@echo "Simulación completada. Ver archivos de salida."

clean:
	@echo "Limpiando archivos generados..."
	@rm -f $(OUTPUT_FILES)
	@echo "Limpieza completada."

help:
	@echo "Opciones disponibles:"
	@echo "  make        - Ejecuta la simulación"
	@echo "  make clean  - Elimina todos los archivos generados"
	@echo "  make help   - Muestra esta ayuda"