import sys
import re
import os
from os import listdir
from os.path import join, isdir

list_terms={}

regex_alpha_words = re.compile(r'[^a-zA-Z0-9]') # Cadenas alfanumericas sin acentos
# Extrae los tokens en una lista
def tokenizer(line):
    result = []
    initial_list_split = line.split()
    for token in initial_list_split:
        word = re.sub(regex_alpha_words,'',token)
        if word != '':
            result.append(word)
    return result


def main():
    if len(sys.argv) < 2:
        print('Es necesario pasar nombre del directorio')        
        sys.exit(0)
    dirname = sys.argv[1]
    
    if (isdir(dirname)):
        arch_salida = open(f'punto_8_heaps.txt', "x",encoding='utf-8')
        terms_total = 0
        terms_uniq = 0
        for filename in listdir(dirname):
            filepath = join(dirname, filename)
            with open(filepath,'r',encoding='utf-8') as f:
                print(f"Processing file: {filepath}")
                for line in f:
                    terms_list = tokenizer(line)
                    for term in terms_list:
                        terms_total += 1
                        if term in list_terms:
                            list_terms[term]+=1
                        else:
                            list_terms[term]= 1
                            terms_uniq +=1
        
            # Escribimos en el archivo
            arch_salida.write(str(terms_total)+' '+str(terms_uniq)+"\n")
        arch_salida.close()

if __name__ == '__main__':
    main()
    