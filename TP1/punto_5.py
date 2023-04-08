import sys
# Usando la libreria para Stemming para Espaniol
import re
from os import listdir
from os.path import join, isdir


def main():
    if len(sys.argv) < 3:
        print('Es necesario pasar como argumentos: directorio_entrenamiento y de testeo.')        
        sys.exit(0)
    dir_entrenamiento = sys.argv[1]
    dir_tests = sys.argv[2]

    if (isdir(dir_entrenamiento)):
        

if __name__ == '__main__':
    main()
    
