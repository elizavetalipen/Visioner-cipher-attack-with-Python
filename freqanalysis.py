import re
from vigenerechiper import *
from visualize import *


def read_from_file()->str:
    ''' Чтение текста из файла и удаление лишних символов'''
    
    print('Чтение из файла...')
    fname = input('Введите имя файла и расширение(.txt): ')
    file = open(fname, 'r',encoding='utf-8')
    
    line = file.read()
    file.close()
    res_line = line.lower()
    
    # удаляем все лишние символы
    res_line = re.sub("[^а-я]", "", res_line)

    return res_line


def count_symbols(line:str) -> dict:
    ''' Вычисляет количество повторений каждого символа
    {символ: сколько раз встречается}'''
    res = {}
    for kys in line:
        res[kys] = res.get(kys, 0) + 1
    return res


def analyze(freq_d: dict, length: int) -> dict:
    ''' Переводит в % количество повторений каждого символа в словаре'''
    for key, f in freq_d.items():
        f = int(f)
        f = (f / length) * 100
        freq_d[key] = f
    return freq_d


def sort_data(freq_d:dict)->dict:
    ''' Сортировка частот в словаре по убыванию'''
    res_d = {k: freq_d[k] for k in sorted(freq_d, key=freq_d.get, reverse=True)}
    return res_d


def normal_text():
    ''' Вызов функций для анализа обычного текста'''
    line = read_from_file()
    length = len(line)
    freq_d = sort_data(count_symbols(line))
    data = analyze(freq_d, length)
    hist_plot(data)
    table_data(data)
 
    
def encrypted_text(key:str):
    ''' Анализ зашифрованного текста'''
    alph = (32,1072)

    line = read_from_file()
    line = vigenere_encrypt(line, key, alph)
    length = len(line)
    freq_d = sort_data(count_symbols(line))
    data = analyze(freq_d, length)
    hist_plot(data)
    table_data(data)


def main():
    mode = int(input('Нажмите 1 для работы с обычным текстом или 2 для работы с зашифрованным: '))
    
    if mode == 1:
        normal_text()
    elif mode == 2:
        key = input('Введите ключ: ')
        encrypted_text(key)
    else:
        print('Ошибка! Перезапустите программу')
    
if __name__ == '__main__':
    main()

