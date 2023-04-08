# Script que recorre los archivos de un directorio, lee su contenido, 
# normaliza los tokens que se encuentran dentro, y al final genera un diccionario,
#Calucla el DF y TF de todos los terminos que sera escrito en un archivo de salida
import sys
# Usando la libreria para Stemming para Espaniol
import nltk
# Esto descargara los recursos necesarios para utilizar el algoritmo SnowballStemmer para español.
nltk.download('snowball_data')
import re
from os import listdir
from os.path import join, isdir
from nltk.stem.snowball import SpanishStemmer

#Variables
long_min = 2   #longitud minimma del token
long_max = 50  #longitud maxima del token

# Expresiones Regulares
regex_alpha_words = re.compile(r'[^a-zA-Z0-9]') # Cadenas alfanumericas sin acentos

# Listas de terminos
list_terms={}


def normalize(token):
    return token.lower()
    

def retrieve_stopword(file_stopword):
    list_sw = []
    with open(file_stopword,'r') as f:
        for line in f:
            tokens = line.strip().split()
            for token in tokens:             
                list_sw.append(token)
    return list_sw

                    
def save_frecuencies_in_file(list_highest,list_lowest,file_name):
    file_out = open(file_name, "x",encoding='utf-8')
    if len(list_highest)>0:
        for term_high in list_highest:
            file_out.write(term_high[0]+' '+ str(term_high[1])+"\n")
    
    if len(list_lowest)>0:    
        for term_low in list_lowest:
            file_out.write(term_low[0]+' '+ str(term_low[1])+"\n")
    file_out.close()
    
# Extrae los tokens en una lista
def tokenizer(line):
    result = []
    initial_list_split = line.split()
    for token in initial_list_split:
        word = re.sub(regex_alpha_words,'',token)
        if word != '' and len(word)>long_min:
            result.append(word)
    return result
    
def main():
    if len(sys.argv) < 3:
        print('Es necesario pasar como argumentos: un path al corpus , usar_stop_word("y" or "n") , nombre_Archivo_stopwords(opcional en caso de que no)')        
        sys.exit(0)
        
    dirname = sys.argv[1]
    # Reviso si el argumento de usar stopwords
    use_stopword = True if sys.argv[2].lower() == 'y' else False
    file_index = 0 # Identifica a cada archivo con id incremental (ademas, sirve para tener la cantidad de archivos total)

    if (isdir(dirname)):
        list_stopwords =[]
        #Valido uso de Stopwords
        if use_stopword:
            if len(sys.argv) < 4: 
                print('Es necesario el nombre_archivo_stopwords')
                sys.exit(0)
            # Recuperos los stopwords del archivo    
            list_stopwords = retrieve_stopword(sys.argv[3])
            
        for filename in listdir(dirname):
            filepath = join(dirname, filename)
            print(f"Processing file: {filepath}")
            with open(filepath,'r',encoding='utf-8') as f:
                for line in f:
                    tokens_list = tokenizer(line)
                    for token in tokens_list:
                        token_in_stopwords = token in list_stopwords #Token existe en la list de stopwords?
                        token_long_acept = long_min<= len(token) <= long_max #longitud del Token aceptable?
                        if token_long_acept:
                            if (not token_in_stopwords):
                                term = normalize(token)
                                term_long_acept = term != '' #Termino aceptable luego de Normalizacion?
                                
                                if term_long_acept:
                                    if term in list_terms:
                                        if file_index in list_terms[term]:
                                            list_terms[term][file_index] +=1
                                        else:
                                            list_terms[term][file_index] = 1   
                                    else:
                                        list_terms[term]={}
                                        list_terms[term][file_index] = 1
            
            file_index += 1    
    
    #Al final guardo las listas de terminos com su DF y TF  en el archivo "terminos.txt"
    
    arch_terms_salida = open("terminos.txt", "x",encoding='utf-8')
    terms_ordered = sorted(list_terms.keys())  
    for term in terms_ordered:
        frecuency = 0
        documents = 0
        for key, value in list_terms[term].items():
            frecuency += value
            documents += 1             
        arch_terms_salida.write(term+" "+ str(frecuency)+" "+ str(documents)+"\n")
    arch_terms_salida.close()
    
if __name__ == '__main__':
    main()
    
