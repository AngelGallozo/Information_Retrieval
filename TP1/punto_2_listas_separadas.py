# Script que recorre los archivos de un directorio, lee su contenido, 
# normaliza los tokens que se encuentran dentro, y al final genera un diccionario,
#Calucla el DF y TF de todos los terminos que sera escrito en un archivo de salida
import sys
from os import listdir
from os.path import join, isdir
import re


#Variables
long_min = 2   #longitud minimma del token
long_max = 50  #longitud maxima del token
limit_top_frec = 10 #Limite del Top de frecuencias

#Listas de TOP por tipo
list_term_lowest_sort = {}
list_term_highest_sort = {}


# Expresiones Regulares
regex_alpha_words = re.compile(r'(^[a-zA-Z0-9áéíóúÁÉÍÓÚñÑ]+$)') # Cadenas alfanumericas con y sin acentos
regex_abrev_1 = re.compile(r'\b[A-Z][a-z]+\.') # Abreviaturas como: Dir.
regex_abrev_2 = re.compile(r'\b[a-z]+\.') # Abreviaturas como: etc.
regex_emails = re.compile(r'^[a-zA-Z0-9._?%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}')  #Correos electronicos

#Expresiones Regulares - Cantidades y Telefonos
regex_tel_1 = re.compile(r'^\+[0-9]{10,13}') # numeros de tel como: +541122334455
regex_tel_2 = re.compile(r'^[0]+[0-9]{2}-[0-9]{8}') # numeros de tel como: 011-22334455
regex_tel_3 = re.compile(r'[0-9]{2,3}-[0-9]{2,3}-[0-9]{3,}-*[0-9]{2}') # numeros de tel como: 022-333-55555 o 11-22-333-33
regex_int_posit = re.compile(r'^[0-9]+$') # Numeros enteros positivos 
regex_int_negat = re.compile(r'^-[0-9]+$') # Numeros enteros negativos
regex_float_point_posit = re.compile(r'^[0-9]{1,}\.[0-9]+') # Numeros reales con punto positivos
regex_float_point_negat = re.compile(r'^-{1}[0-9]{1,}\.[0-9]+') # Numeros reales negativos con punto
regex_float_coma_posit = re.compile(r'^[0-9]{1,}\,[0-9]+') # Numeros reales con coma positivos
regex_float_coma_negat = re.compile(r'^-{1}[0-9]{1,}\,[0-9]+') # Numeros reales negativos con coma

# Expresiones Regulares- URLs
regex_url_1 = re.compile(r'http[s]?://(?:[A-Za-z]|[0-9]|[+_@$-.&]|[*,!/:?=#\(\)])+') # URLs como: http o https
regex_url_2 = re.compile(r'^www\.(?:[A-Za-z]|[0-9]|[+_@$-.&]|[*,!/:?=#\(\)])') # URL como: www. ejemplo.com.ar 

# Listas de terminos
list_terms_urls = {}
list_terms_alphanum_words = {}
list_terms_abrev = {}
list_terms_emails = {}
list_terms_cants = {}
list_terms_names = {}

# Token Counter - Lleva el conteo de cada token extraido y hace el conteo segun su tipo (alfanumerico,abreviatura,cantidad,url,email,nombre propio)
tokens_counter = {}

# Cantidad Tokens de Documentos largo y corto por tipo de token
cant_tokens_doc_short = {}
cant_tokens_doc_long = {}

# Cantidad Terminos de Documentos largo y corto por tipo de token
cant_term_doc_long = {}
cant_term_doc_short = {}

#Contadores de tokens por documento, se almacenan segun el tipo
tokens_counter_for_doc = {}

# Guardo la cantidad total de terminos por tipo de token       
terms_counter = {}

# Guardo cantidad de termionos con frecuencia 1 por tipo de termino
cant_term_collecfrec_1 = {}

# Largos promedios de terminos por tipo
sum_long_terms = {}


def normalize(token):
    return token.lower()

#Devuelve la  lista de terminos especifica segun el tipo de token
def get_list(tipo_token):
    list_out = {}
    if 'url' == tipo_token:
        list_out = list_terms_urls
    
    if 'alphanum' == tipo_token:
         list_out = list_terms_alphanum_words
    
    if 'abrev' == tipo_token:
         list_out = list_terms_abrev
         
    if 'email' == tipo_token:
        list_out = list_terms_emails 
    
    if 'cant' == tipo_token:
        list_out = list_terms_cants
    
    if 'names' == tipo_token:
        list_out = list_terms_names 
        
    return list_out
         

def retrieve_stopword(file_stopword):
    list_sw = []
    with open(file_stopword,'r') as f:
        for line in f:
            tokens = line.strip().split()
            for token in tokens:             
                list_sw.append(token)
    return list_sw

# Verificar y Almacenar Termino en el top de menos frecuentes segun el tipo  
def store_terms_lowest_frec(tipo_lista,key,frecuency):
    if not (tipo_lista in list_term_lowest_sort):
        list_term_lowest_sort[tipo_lista] = [[key,frecuency]]
    else:
        lista_top = list_term_lowest_sort[tipo_lista]
        below_limit_top = len(lista_top)<limit_top_frec
        for index in range( 0,len(lista_top)):
            term_frec = lista_top[index][1]
            if index < limit_top_frec:
                if  frecuency <= term_frec:
                    lista_top.insert(index,[key,frecuency])
                    if not below_limit_top:
                        list_term_lowest_sort[tipo_lista]= lista_top[:limit_top_frec]
                    break
                else:
                    if index == len(lista_top)-1:
                        lista_top.append([key,frecuency])
                        if not below_limit_top:
                            lista_top = lista_top[:limit_top_frec]
                        break
                
# Verificar y Almacenar Termino en el top de mas frecuentes segun el tipo                
def store_terms_highest_frec(tipo_lista,key,frecuency):
    if not tipo_lista in list_term_highest_sort:
        list_term_highest_sort[tipo_lista] = [[key,frecuency]]
    else:
        lista_top = list_term_highest_sort[tipo_lista]
        below_limit_top = len(lista_top)<limit_top_frec
        for index in range( 0,len(lista_top)):
            term_frec = lista_top[index][1]
            
            if ( frecuency >= term_frec and index < limit_top_frec-1 ):
                lista_top.insert(index,[key,frecuency])
                if not below_limit_top:
                    list_term_highest_sort[tipo_lista]= lista_top[:limit_top_frec]
                break

                    
def save_frecuencies_in_file(list_highest,list_lowest,tipo_lista):
    file_out = open(f"frecuencias_{tipo_lista}.txt", "x",encoding='utf-8')
    if len(list_highest)>0:
        for term_high in list_highest:
            file_out.write(term_high[0]+' '+ str(term_high[1])+"\n")
    
    if len(list_lowest)>0:    
        for term_low in list_lowest:
            file_out.write(term_low[0]+' '+ str(term_low[1])+"\n")
    file_out.close()

# Borra de una cadena los caracteres que le pasen                 
def delete_caracteres(token, caracteres):
    table = str.maketrans('','',caracteres)
    return token.translate(table)
    
# Extrae los tokens en una lista
def tokenizer(line):
    result = []
    initial_list_split = line.split()
    secundary_list_split = initial_list_split.copy()
    # Analisis de URL
    for token in initial_list_split:
        is_url = re.match(regex_url_1,token) or re.match(regex_url_2,token) 
        
        if is_url:
            result.append([token,'url'])
            url_divided_tokens = re.sub("[./#-?=&_:]", " ", token) # Divide el string URL con espacios
            initial_list_split = initial_list_split + url_divided_tokens.split() # Agrega cada elemento del string URL en la lista inicial
            secundary_list_split.remove(token) #Remuevo la url ya analizada
        
        #Tratamientos de Emails
        if re.match(regex_emails,token):
            result.append([token,'email'])
            secundary_list_split.remove(token) #Remuevo el email ya analizada
       
    # Analisis otros patrones
    for token in secundary_list_split:
        # Tratamiento de cadenas alfanumericas
        token_clean = delete_caracteres(token,',.;:/\\')
        if re.findall(regex_alpha_words,token_clean):
            result.append([token_clean,'alphanum'])
        
        #Tratamientos de Abreviaturas
        list_abrev = []
        list_abrev = list_abrev + re.findall(regex_abrev_1,token)
        list_abrev = list_abrev + re.findall(regex_abrev_2,token)
        is_abrev = len(list_abrev)>0
        
        if is_abrev:
            result.append([token,'abrev'])
        
        #Tratemientos de Cantidades
        list_cant = []
        list_cant = list_cant + re.findall(regex_tel_1,token) 
        list_cant = list_cant + re.findall(regex_tel_2,token) 
        list_cant = list_cant + re.findall(regex_tel_3,token) 
        list_cant = list_cant + re.findall(regex_float_point_posit,token) 
        list_cant = list_cant + re.findall(regex_float_coma_posit,token) 
        list_cant = list_cant + re.findall(regex_float_point_negat,token) 
        list_cant = list_cant + re.findall(regex_float_coma_negat,token) 
        list_cant = list_cant + re.findall(regex_int_posit,token) 
        list_cant = list_cant + re.findall(regex_int_negat,token) 
        is_cantidad = len(list_cant)>0
        if is_cantidad:
             result.append([token,'cant']) 
        
    return result

# Calcular DF , CF y guardar en archivo 
def calc_terms(list_terms,tipo_lista):
    arch_terms_salida = open(f"terminos_{tipo_lista}.txt", "x",encoding='utf-8')
    
    terms_ordered = sorted(list_terms.keys())
    
    for term in terms_ordered:
        frecuency = 0
        documents = 0
        for key, value in list_terms[term].items():
            frecuency += value
            documents += 1
            
            # Conteo de termnos de documento mas largo y mas corto
            id_doc_long = cant_tokens_doc_long[tipo_lista][0] #Obtengo id del doc mas largo (cant tokens) 
            if key == id_doc_long:
                if tipo_lista in cant_term_doc_long:
                    cant_term_doc_long[tipo_lista] += value
                else:
                    cant_term_doc_long[tipo_lista] = value
            
            id_doc_short = cant_tokens_doc_short[tipo_lista][0] #Obtengo id del doc mas corto (cant tokens)
            if key == id_doc_short:
                if tipo_lista in cant_term_doc_short:
                    cant_term_doc_short[tipo_lista] += value
                else:
                    cant_term_doc_short[tipo_lista] = value
        
        # Guardo la cantidad total de terminos pot tipo 
        if tipo_lista in terms_counter:
            terms_counter[tipo_lista] += frecuency
        else:
            terms_counter[tipo_lista] = frecuency
        
        # Guardar cantidad de terminos que tienen frecuencia 1 por tipo.
        if frecuency == 1:
            if tipo_lista in cant_term_collecfrec_1:
                cant_term_collecfrec_1[tipo_lista] +=1
            else:
                cant_term_collecfrec_1[tipo_lista] =1

        # Guardar en el top 10 de más y menos frecuentes
        store_terms_highest_frec(tipo_lista,term, frecuency)
        store_terms_lowest_frec(tipo_lista,term, frecuency)
                
        arch_terms_salida.write(term+" "+ str(frecuency)+" "+ str(documents)+"\n")
    arch_terms_salida.close()

#Calcular Promedios y guardar en archivo
def calc_avg(tipo_lista,cant_docs):
    avg_terms_in_doc = round(terms_counter[tipo_lista]/cant_docs, 2)
    avg_tokens_in_doc = round(tokens_counter[tipo_lista]/cant_docs, 2)
    avg_long_terms = round(sum_long_terms[tipo_lista]/terms_counter[tipo_lista], 2)
    
    #Gestion de archivo "estadisticas.txt"
    arch_stats_salida = open(f"estadisticas_{tipo_lista}.txt", "x",encoding='utf-8')
    arch_stats_salida.write(str(cant_docs)+"\n")
    arch_stats_salida.write(str(tokens_counter[tipo_lista])+' '+ str(terms_counter[tipo_lista])+"\n")
    arch_stats_salida.write(str(avg_tokens_in_doc)+' '+ str(avg_terms_in_doc)+"\n")
    arch_stats_salida.write(str(avg_long_terms)+"\n")
    arch_stats_salida.write(str(cant_tokens_doc_long[tipo_lista][1])+' '+ str(cant_term_doc_long[tipo_lista])+' '+str(cant_tokens_doc_short[tipo_lista][1])+' '+ str(cant_term_doc_short[tipo_lista])+"\n")
    arch_stats_salida.write(str(cant_term_collecfrec_1[tipo_lista])+"\n")
    arch_stats_salida.close()



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
                tokens_counter_for_doc.clear()
                for line in f:
                    tokens_list = tokenizer(line)
                    for token in tokens_list:
                        #Obtengo el token y su tipo (alfanumerico,abreviatura,cantidad,url,email,nombre propio)
                        valor_token = token[0]
                        tipo_token = token[1]
                        token_in_stopwords = valor_token in list_stopwords #Token existe en la list de stopwords?
                        token_long_acept = long_min<= len(valor_token) <= long_max #longitud del Token aceptable?
                        if token_long_acept:
                            if tipo_token in tokens_counter:
                                tokens_counter[tipo_token] +=1
                            else:
                                tokens_counter[tipo_token] = 1
                            if tipo_token in tokens_counter_for_doc:
                                tokens_counter_for_doc[tipo_token] +=1
                            else:
                                tokens_counter_for_doc[tipo_token] =1
                            
                            if (not token_in_stopwords):
                                term = normalize(valor_token)
                                term_long_acept = term != '' #Termino aceptable luego de Normalizacion?
                                
                                if term_long_acept:
                                    #Suma las longitudes de los terminos extraidos segun su tipo
                                    if tipo_token in sum_long_terms:
                                        sum_long_terms[tipo_token] += len(term)
                                    else: 
                                        sum_long_terms[tipo_token] = len(term)
                                    
                                    #Obtengo lista segun el tipo de token
                                    list_terms = get_list(tipo_token)
                                    if term in list_terms:
                                        if file_index in list_terms[term]:
                                            list_terms[term][file_index] +=1
                                        else:
                                            list_terms[term][file_index] = 1   
                                    else:
                                        list_terms[term]={}
                                        list_terms[term][file_index] = 1
            
            
            #Guardo todos los contadores de tokens por documento, se guarda un contador por tipo de token
            for tipo_contador,valor_contador in tokens_counter_for_doc.items():
                #Para que se queden como minimos las cantidades del primer documento
                if not (tipo_contador in cant_tokens_doc_short): 
                    cant_tokens_doc_short[tipo_contador] = [file_index,valor_contador]
                
                #Para que se queden como maximos las cantidades del primer documento
                if not (tipo_contador in cant_tokens_doc_long): 
                    cant_tokens_doc_long[tipo_contador] = [file_index,valor_contador]
                    
                #Guarda la mayores cantidades de tokens de un documento
                valor_del_contador = cant_tokens_doc_long[tipo_contador][1]
                if tokens_counter_for_doc[tipo_contador] > valor_del_contador:
                    cant_tokens_doc_long[tipo_contador] = [file_index,valor_contador ]
                
                #Guarda la menores cantidades de tokens de un documento
                valor_del_contador = cant_tokens_doc_short[tipo_contador][1]
                if tokens_counter_for_doc[tipo_contador] < valor_del_contador:
                    cant_tokens_doc_short[tipo_contador] = [file_index,valor_contador ]
            
            file_index += 1    
    
    #Al final guardo las listas de terminos com su DF y TF  en el archivo "terminos.txt"
    calc_terms(list_terms_alphanum_words,'alphanum')
    calc_terms(list_terms_abrev,'abrev')
    calc_terms(list_terms_cants,'cant')
    calc_terms(list_terms_emails,'email')
    calc_terms(list_terms_urls,'url')
    #calc_terms(list_terms_names,'name')
    
    # Calculo de promedios
    calc_avg('alphanum',file_index)
    calc_avg('abrev',file_index)
    calc_avg('cant',file_index)
    calc_avg('email',file_index)
    calc_avg('url',file_index)
    #calc_avg('name',file_index)
    
    #Gestion archivo de "frecuencias.txt"
    
    save_frecuencies_in_file(list_term_highest_sort['alphanum'],list_term_lowest_sort['alphanum'],'alphanum')
    
    
    
if __name__ == '__main__':
    main()
    
