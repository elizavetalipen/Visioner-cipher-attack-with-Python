# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 23:04:33 2021

@author: User
"""
from visualize import table_data
from vigenerechiper import *
from freqanalysis import *



def match_index(text_len:int, letters:dict):
    ''' Вычисляет индекс совпадения (число)
    letters достаётся из словаря, который вернет фнкция count_symbols
    '''
    counts = list(letters.values())
    ind = 0
    for i in range(len(counts)):
        ind = ind + ((counts[i])*(counts[i]-1))/(text_len*(text_len-1))
        
    return ind


def sparse_text(n:int, text:str)->str:
    '''Функция которая проряжает текст, то есть результат состоит из каждой
    n-ой буквы исходного текста'''
    sparsed_text = ''
    group = []
    txtlen = len(text)
    for i in range(0,txtlen,n):
        sparsed_text = sparsed_text + text[i]
    return sparsed_text[1:]



def find_indexes(max_n:int, text:str)->dict:
    '''  Вернет словарь вида {n : ind} , где
    ind - индекс совпадений проряженного текста'''
    
    kys = [i for i in range(2,max_n)]
    vals = []
    for i in range(2,max_n):
        
        t = sparse_text(i,text)
        letters = count_symbols(t)
        ind = match_index(len(t),letters)
        vals.append(ind)
    res = dict(zip(kys,vals))
    return res
    
  
def find_key_length(ci, d:dict)->int:
    ''' Принимает словарь с индексами совпадения проряженного текста
    и значение индекса для открытого текста'''
    indexes = list(d.values())
    delta = min(indexes, key=lambda x: abs(ci-x))
    
    for key, value in d.items():
        if delta == value:
             return key
         
            
def alignInColumns(text, n):
    ''' Делит текст на эн блоков'''
    t = []
    for i in range(0,n):
        t.append("")
    i = 0
    for c in text:
        t[i % n]+=c
        i+=1
    return t


def find_keyword1(substrings, freqs, alphabet, alph):
    '''
    В словаре dist сохраняется относительное распределение частот для 
    каждой подстроки.
    Буква ключа соответствует наименьшему значению параметра fingerprint
    '''
    alphabet = list(alphabet.values())
    keyword = ''

    for string in substrings:
        dist = {}
    
        for letter in string:
            if letter in dist:
                dist[letter] += 1
            else:
                dist[letter] = 1

        for letter in alphabet:
            if letter not in dist:
                dist[letter] = 0

        for letter,occurence in dist.items():
            dist[letter] = (float(occurence)/len(string)) * 10
            
        testRotation = 0
        fingerprint = 1000
        keyLetter = 'A'
        while testRotation < alph[0]:
            diff = 0
            for i in range(alph[0]-1):
                templateKey = alphabet[i]
                distKey = alphabet[(i+testRotation) % (alph[0]-1)]

                diff += pow(freqs[templateKey] - dist[distKey],2)

            if diff < fingerprint:
                fingerprint = diff
                keyLetter = alphabet[testRotation]

            testRotation += 1
        keyword += keyLetter
    return keyword
    

def find_keyword2(blocks:list, freqs:dict, alphabet, l):
    ''' Второй вариант функции, может неккоректно находить некоторые буквы ключа'''
    freqs = sort_data(freqs)
    f_letters = list(freqs.keys())
    keyword = ''
    shifts, key = [], []
    
    for block in blocks:
        dist = analyze(count_symbols(block),len(block))
        # отсортированный словарь частот для данного блока текста
        dist = sort_data(dist) 
        dist_letters = list(dist.keys())
        
        for i in range(len(dist_letters)):
            diff = abs(ord(dist_letters[i])-ord(f_letters[i]))
            shifts.append(diff)
         
        # сдвигом будет самое часто встречающееся значение
        shift = most_frequent(shifts)
        shift = shift + 1
        shifts = []
        key.append(alphabet[shift])
        
    key = key[:l]
    key = ''.join(key)
    return key


    
def most_frequent(List):
    ''' Вспомогательная функция ищет самый частый элемент в списке'''
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num      
     

def main():
    
    key =input('Введите ключ: ')
    
    # установка констант, алфавита для русского языка
    alph = (32,1072)
    alphabet = {i-1071: chr(i) for i in range(1072,1104)}
    #alphabet = list(alphabet.values())
    const_ind = 0.0553
    
    normal_text = read_from_file()
    encr_text = vigenere_encrypt(normal_text, key, alph)
    
    # словарь распределения частот символов для обычного текста
    freqs = analyze(count_symbols(normal_text),len(normal_text))
    # словарь индексов взаимного совпадения для каждого из разбиений текста
    ind_dict = find_indexes(30,encr_text)
    # длина ключа
    key_len = find_key_length(const_ind,ind_dict)
    print('Длина ключа ', key_len)
    # список, состоящий из блоков текста
    blocks = alignInColumns(encr_text, key_len)
    
    kw1 = find_keyword1(blocks,freqs, alphabet, alph)
    kw2 = find_keyword2(blocks, freqs, alphabet, key_len)
    
    print('func1: Возможный ключ: ',kw1)
    print('\nfunc2: Возможный ключ: ',kw2)
    #print(encr_text[:1000])
    
    
if __name__ == '__main__':
    main()