# Script que recorre los archivos de un directorio, lee su contenido, 
# normaliza los tokens que se encuentran dentro, y al final genera un diccionario,
#Calucla el DF y TF de todos los terminos que sera escrito en un archivo de salida
import sys
# Usando la libreria para Stemming para Espaniol
import re
from os import listdir
from os.path import join, isdir
from nltk import LancasterStemmer
from nltk.stem import PorterStemmer
from time import time


#Variables
long_min = 2   #longitud minimma del token
long_max = 50  #longitud maxima del token
limit_top_frec = 10 #Limite del Top de frecuencias
list_term_lowest_sort = []
list_term_highest_sort = []


# Expresiones Regulares
regex_alpha_words = re.compile(r'[^a-zA-Z0-9]') # Cadenas alfanumericas con y sin acentos

# Listas de terminos
list_terms={}


def main():
    ini_time = time()
    procesar_docs('Porter')
    print("Tiempo Stemming Porter: "+ str(time()-ini_time))
    
    ini_time = time()
    procesar_docs('Lancaster')
    print("Tiempo Stemming Lancaster: "+ str(time()-ini_time))
    
def normalize(token):
    return token.lower()

def stemming(token,tipo_stemmer):
    if(tipo_stemmer == 'Porter'):
        stemmer = PorterStemmer()
    if(tipo_stemmer == 'Lancaster'):
        stemmer = LancasterStemmer()
    return stemmer.stem(token)
    

def retrieve_stopword(file_stopword):
    list_sw = []
    with open(file_stopword,'r') as f:
        for line in f:
            tokens = line.strip().split()
            for token in tokens:             
                list_sw.append(token)
    return list_sw

def store_terms_lowest_frec(key,frecuency):
    global list_term_lowest_sort
    if len(list_term_lowest_sort)==0:
        list_term_lowest_sort.append([key,frecuency])
    else:
        below_limit_top = len(list_term_lowest_sort)<limit_top_frec
        for index in range( 0,len(list_term_lowest_sort)):
            term_frec = list_term_lowest_sort[index][1]
            if index < limit_top_frec:
                if  frecuency <= term_frec:
                    list_term_lowest_sort.insert(index,[key,frecuency])
                    if not below_limit_top:
                        list_term_lowest_sort = list_term_lowest_sort[:limit_top_frec]
                    break
                else:
                    if index == len(list_term_lowest_sort)-1:
                        list_term_lowest_sort.append([key,frecuency])
                        if not below_limit_top:
                            list_term_lowest_sort = list_term_lowest_sort[:limit_top_frec]
                        break
                

def store_terms_highest_frec(key,frecuency):
    global list_term_highest_sort
    if len(list_term_highest_sort)==0:
        list_term_highest_sort.append([key,frecuency])
    else:
        below_limit_top = len(list_term_highest_sort)<limit_top_frec
        for index in range( 0,len(list_term_highest_sort)):
            term_frec = list_term_highest_sort[index][1]
            
            if ( frecuency >= term_frec):
                list_term_highest_sort.insert(index,[key,frecuency])
                break
            else:
                if index == len(list_term_highest_sort)-1:
                    list_term_highest_sort.insert(index,[key,frecuency])
        
        if not below_limit_top:
            list_term_highest_sort = list_term_highest_sort[:limit_top_frec]
            
                    

                    
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
        
    # Analisis otros patrones
    for token in initial_list_split:
        
        word = re.sub(regex_alpha_words,'',token)
        if word != '' and len(word)>long_min:
            result.append(word)
    return result
    
def procesar_docs(tipo_stemmer):
    if len(sys.argv) < 3:
        print('Es necesario pasar como argumentos: un path al corpus , usar_stop_word("y" or "n") , nombre_Archivo_stopwords(opcional en caso de que no)')        
        sys.exit(0)
        
    dirname = sys.argv[1]
    # Reviso si el argumento de usar stopwords
    use_stopword = True if sys.argv[2].lower() == 'y' else False
    file_index = 0 # Identifica a cada archivo con id incremental (ademas, sirve para tener la cantidad de archivos total)
    tokens_counter = 0
    terms_counter = 0
    sum_long_terms = 0
    cant_tokens_doc_short = 0
    id_doc_short = -1
    cant_tokens_doc_long = 0
    id_doc_long = -1
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
            with open(filepath,'r',encoding='utf-8') as f:
                tokens_counter_for_doc = 0
                for line in f:
                    tokens_list = tokenizer(line)
                    for token in tokens_list:
                        token_in_stopwords = token in list_stopwords #Token existe en la list de stopwords?
                        token_long_acept = long_min<= len(token) <= long_max #longitud del Token aceptable?
                        if token_long_acept:
                            tokens_counter +=1
                            tokens_counter_for_doc +=1
                            if (not token_in_stopwords):
                                term = normalize(token)
                                term = stemming(term,tipo_stemmer)                                
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
                                        # Guardo la cantidad total de terminos  
                                        terms_counter +=1
                                        # Guardo la suma de longitudes de terminos
                                        sum_long_terms+=len(term)
            
            #Para que se quede como minima la cantidad del primer documento
            if cant_tokens_doc_short == 0: 
                cant_tokens_doc_short = tokens_counter_for_doc
                id_doc_short = file_index
            
            #Guarda la mayor cantidad de tokens de un documento
            if tokens_counter_for_doc > cant_tokens_doc_long:
                cant_tokens_doc_long = tokens_counter_for_doc
                id_doc_long = file_index
            
            #Guarda la menor cantidad de tokens de un documento
            if tokens_counter_for_doc < cant_tokens_doc_short:
                cant_tokens_doc_short = tokens_counter_for_doc
                id_doc_short = file_index 
            
            file_index += 1    
    
    #Al final guardo las listas de terminos com su DF y TF  en el archivo "terminos.txt"
    
    arch_terms_salida = open(f'terminos_Stemming_{tipo_stemmer}.txt', "x",encoding='utf-8')
    terms_ordered = sorted(list_terms.keys())  
    cant_term_doc_long = 0
    cant_term_doc_short = 0
    cant_term_collecfrec_1 = 0
    for term in terms_ordered:
        frecuency = 0
        documents = 0
        for key, value in list_terms[term].items():
            frecuency += value
            documents += 1
            
            # Conteo de termnos de documento mas largo y mas corto
            if key == id_doc_long:
                cant_term_doc_long += 1
                 
            if key == id_doc_short:
                cant_term_doc_short += 1
        
        # Guardar cantidad de terminos que tienen frecuencia 1.
        if frecuency == 1:
            cant_term_collecfrec_1 +=1

        # Guardar en el top 10 de más y menos frecuentes
        store_terms_highest_frec(term, frecuency)
        store_terms_lowest_frec(term, frecuency)
                
        arch_terms_salida.write(term+" "+ str(frecuency)+" "+ str(documents)+"\n")
    arch_terms_salida.close()

    # Calculo de promedios
    avg_terms_in_doc = round(terms_counter/file_index, 5)
    avg_tokens_in_doc = round(tokens_counter/file_index, 5)
    avg_long_terms = round(sum_long_terms/terms_counter, 5)
    
    # Gestion de archivo "estadisticas.txt"
    arch_stats_salida = open(f'estadisticas_Stemming_{tipo_stemmer}.txt', "x",encoding='utf-8')
    arch_stats_salida.write(str(file_index)+"\n")
    arch_stats_salida.write(str(tokens_counter)+' '+ str(terms_counter)+"\n")
    arch_stats_salida.write(str(avg_tokens_in_doc)+' '+ str(avg_terms_in_doc)+"\n")
    arch_stats_salida.write(str(avg_long_terms)+"\n")
    arch_stats_salida.write(str(cant_tokens_doc_long)+' '+ str(cant_term_doc_long)+' '+str(cant_tokens_doc_short)+' '+ str(cant_term_doc_short)+"\n")
    arch_stats_salida.write(str(cant_term_collecfrec_1)+"\n")
    arch_stats_salida.close()
    
    #Gestion archivo de "frecuencias.txt"
    save_frecuencies_in_file(list_term_highest_sort,list_term_lowest_sort,f'frecuencias_Stemming_{tipo_stemmer}.txt')
    
if __name__ == '__main__':
    main()
    
