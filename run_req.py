"""
Ejecucion para instalar / actualizar requerimientos de la ejecucion de la
herramienta can base en el archivo requirements.txt
"""
import subprocess
import sys

def main():
    with open("requirements.txt", "r") as req_file:
        for library in req_file.readlines():
            subprocess.call(
                ['pip', 'install', '-U', library], stdout=sys.stdout)

if __name__ == "__main__":
    main()
