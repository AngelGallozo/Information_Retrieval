# TP 1 - Analisis de Texto
## Punto 1
Escriba un programa que realice analisis lexico sobre la coleccion RI-tknz-data. El programa debe recibir
como parametros el directorio donde se encuentran los documentos y un argumento que indica si se deben
eliminar las palabras vac´ıas (y en tal caso, el nombre del archivo que las contiene). Defina, ademas, una longitud mınima y maxima para los terminos. Como salida, el programa debe generar:
* a) Un archivo (terminos.txt) con la lista de t´erminos a indexar (ordenado), su frecuencia en la colecci´on
y su DF (Document Frequency). Formato de salida: < termino > [ESP] < CF > [ESP] < DF >.

    Ejemplo:

    casa 238 3

    perro 644 6

    ...

    zorro 12 1

* b) Un segundo archivo (estadisticas.txt) con los siguientes datos (un punto por línea y separados por espacio cuando sean mas de un valor) :
    * 1) Cantidad de documentos procesados
    * 2) Cantidad de tokens y terminos extraıdos
    * 3) Promedio de tokens y terminos de los documentos
    * 4) Largo promedio de un termino
    * 5) Cantidad de tokens y terminos del documento mas corto y del mas largo
    * 6) Cantidad de terminos que aparecen solo 1 vez en la coleccion

* c) Un tercer archivo (frecuencias.txt, con un termino y su CF por lınea) con:
    * 1) La lista de los 10 terminos mas frecuentes y su CF (Collection Frequency)
    * 2) La lista de los 10 terminos menos frecuentes y su CF.

### Sentencia de ejecucuión:
python punto_1.py <diretorio_corpus> <"y" or "n"> <archivo_stopword.txt>

El campo <"y" or "n">, es para que se utilicen el archivo de stopwords o no.

El campo <archivo_stopword.txt>, nno necesita definirse si el argumento <"y" or "n"> es "n".

## Punto 2
Tomando como base el programa anterior, escriba un segundo T okenizer que implemente los criterios del
artıculo de Grefenstette y Tapanainen para definir que es una “palabra” (o termino) y como tratar numeros
y signos de puntuacion. Adem´as, extraiga en listas separadas utilizando en cada caso una funci´on especıfica.
* a) Abreviaturas tal cual estan escritas (por ejemplo, Dr., Lic., S.A., etc.)2
* b) Direcciones de correo electronico y URLs.
* c) Numeros (por ejemplo, cantidades, telefonos).
* d) Nombres propios (por ejemplo, Villa Carlos Paz, Manuel Belgrano, etc.) y los trate como un unico
token.

Genere y almacene la misma informacion que en el caso anterior.

### Sentencia de ejecucuión:
python punto_2.py <diretorio_corpus> <"y" or "n"> <archivo_stopword.txt>

El campo <"y" or "n">, es para que se utilicen el archivo de stopwords o no.

El campo <archivo_stopword.txt>, nno necesita definirse si el argumento <"y" or "n"> es "n".