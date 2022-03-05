# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 17:33:28 2021

@author: User
"""

def vigenere_encrypt(text:str,key:str, alph):
    ''' Шифровка текста шифром Вижинера
    Алфавит это кортеж из двух чисел 
    (кол-во букв в алфавите, кодировка первого символа в юникоде)'''
    N, c = alph[0], alph[1]
    res_text=''
    # удлинение ключа
    rem, quotient = len(text) % len(key), len(text) // len(key)
    ext_key = key*(quotient) + key[:rem]
    # перевод символов в коды
    key_codes, text_codes = [ord(i) for i in ext_key], [ord(i) for i in text]
        
    for i in range(len(text)):
        res_code = (text_codes[i] + key_codes[i]) 
        res_text += chr(res_code % N + c)
        
    return res_text



def vigenere_decrypt(text:str,key:str, alph):
    ''' Расшифровывает сообщение, если известен ключ'''
    N, c = alph[0], alph[1]
    res_text=''
    # удлинение ключа
    rem, quotient = len(text) % len(key), len(text) // len(key)
    ext_key = key*(quotient) + key[:rem]
    
    key_codes, text_codes = [ord(i) for i in ext_key], [ord(i) for i in text]
        
    for i in range(len(text)):
        res_code = (text_codes[i] - key_codes[i]) 
        res_text += chr(res_code % N + c)
        
    return res_text

