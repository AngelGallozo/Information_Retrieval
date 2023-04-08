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
    with open("texto.txt",'r',encoding='utf-8') as f:
        for line in f:
            terms_list = tokenizer(line)
            for term in terms_list:
                if term in list_terms:
                    list_terms[term]+=1
                else:
                    list_terms[term]= 1   











if __name__ == '__main__':
    main()
    