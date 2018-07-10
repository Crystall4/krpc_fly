#! /usr/bin/env python2
# -*- coding: utf-8 -*-
import socket
import threading
import Queue
import time

# Определяем константу содержащую имя ОС
# для учёта особенностей данной операционной системы
import platform
OS_NAME = platform.system()

# Константы
HOST = 'localhost'
PORT = 1777

# Единственная глобальная переменная
# доступная всем потокам
run = True
sysq = Queue.Queue()

def shutdown_socket(s):
    # В Linux'ах просто закрыть заблокированный сокет будет мало,
    # он так и не выйдет из состояния блокировки. Нужно передать
    # ему команду на завершение. Но в Windows наоборот, команда
    # на завершение вызовет зависание, если сокет был заблокирован
    # вызовом accept(), а простое закрытие сработает.
    #if OS_NAME == 'Linux':
        #s.shutdown(socket.SHUT_RDWR)
    s.close()    

def reciver(client, q):
    while run:
        try:
            # Здесь поток блокируется до тех пор
            # пока не будут считаны все имеющиеся
            # в сокете данные
            data, addr = client.recvfrom(1024)
            if data: # Если есть данные
                # Отправляем в очередь сообщений кортеж
                # содержащий сокет отправителя
                # и принятые данные
                if data =='exit': sysq.put((data))
                else:
					q.put((addr, data))
					print('От {} получено: {}'.format(str(addr), data.decode()))
                
        except:
            break # В случае ошибки выходим из цикла

def sender(q, connections):
    while run:
        try:
            # Получаем из очереди сообщений
            # сокет отправителя и принятые данные
            sender, message = q.get(timeout=0.1)
        except Queue.Empty:
            pass # Игнорируем отсутствие сообщений в очереди
        else: # Если же сообщения есть
            connections.sendto(message, sender)
            print('Ответ {} отправлен клиенту: {}'.format( message.decode(), str(sender)))
            q.task_done() # Сообщаем, что сообщение обработано

if __name__ == '__main__':
	print('Запуск...')
	#global sysq
	# Очередь сообщений, через которую будут общаться потоки
	q = Queue.Queue()

    # Множество соединений
	connections = set()

    #server = socket.socket()
	udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	udp_socket.bind((HOST, PORT))
	udp_socket.setblocking(5)    
    #server.listen(5)

	print(u'Сервер запущен на {}\n'.format(udp_socket.getsockname()))

    # Поток получающий сообщения из очереди
    # и отправляющий их всем сокетам в множестве connections
	threading.Thread(target=sender, args=(q, udp_socket)).start()
    # Поток принимающий новые соединения
	threading.Thread(target=reciver, args=(udp_socket, q)).start()

	while True:
		command = ''
		time.sleep(0.1)
		try:
			# Получаем из очереди сообщений
			# сокет отправителя и принятые данные
			command = sysq.get(timeout=0.1)
		except Queue.Empty:
			pass # Игнорируем отсутствие сообщений в очереди
		else: # Если же сообщения есть
			print 'Получена комманда: '+str(command)
			if command == 'exit': # Если получена команда exit
				run = False # отменяем выполнение циклов во всех потоках
			sysq.task_done() # Сообщаем, что сообщение обработано
			
		if run == False: # Если в консоли введена команда exit
			break # и выходим из этого цикла
	shutdown_socket(udp_socket)
