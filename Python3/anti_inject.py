"""
Список литературы: Техническая документация языка Python 3 версии https://docs.python.org/3/
Для работы необходимо:
    1) установить утилиту Listdlls
    2) создать директроию sigs
"""

process_name = "gameName.exe" #Имя процесса
signatures = "" #Зафиксированные сигнатуры
mode = 1 #Режим
scan_delay = 3 #Промежуток сканирования сигнатур

import os, subprocess, zlib, time #Импорт модулей

def crc(fileName): #Реализуем функцию с одним параметром
    prev = 0
    for eachLine in open(fileName, "rb"): #В цикле открываем файл с именем fileName в бинарном режиме для чтения и бежим по строкам
        prev = zlib.crc32(eachLine, prev) #Вычисляем контрольную сумму CRC из eachLine, начальное значение контрольной суммы = prev
    return "%X"%(prev & 0xFFFFFFFF) #Возврат строки с форматированием в шестнадцатиричное представление

sigs_path = "./sigs/" + process_name + "_sigs.txt" #Путь для хранения сигнатур
sigs_local_path = "./sig.txt" #Путь хранения сигнатур для сравнения

if mode: #Если mode равен 1
    sigs = subprocess.check_output('listdlls ' + process_name).decode("utf-8") #Пишем в переменную sigs результат выполнения команды listdlls с именем процесса, преобразованный в формат utf-8
    f = open(sigs_path, 'w') #Открываем файл по пути sigs_path на запись
    f.write(sigs) #Пишем в открытый файл sigs
    f.close() #Закрываем файл

    print("Сигнатуры процесса " + process_name + " созданы!")

    f = open(sigs_local_path, 'w')
    f.write(sigs)
    f.close()

    while True:
        print("Сканирование...")

        sigs = subprocess.check_output('listdlls ' + process_name).decode("utf-8")
        f = open(sigs_local_path, 'w')
        f.write(sigs)
        f.close()
        
        check = crc(sigs_path) == crc(sigs_local_path) #Пишем в check результат сравнения результатов функции crc

        if (check):
            #Если сигнатуры совпали
            time.sleep(scan_delay) #Приостанавливаем выполнение потока на scan_delay секунд
            continue; #Продолжаем цикл
        else:
            #Иначе
            print("ОБНАРУЖЕН ИНЖЕКТ!!!")
            os.system('taskkill /IM "' + process_name + '" /F') #Выполняем команду с аргументом в подоболочке
            break; #Остановка цикла
