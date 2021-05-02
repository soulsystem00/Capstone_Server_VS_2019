from socket import *
import threading
from dataclasses import dataclass
import time

@dataclass
class User: 
    User_Socket: socket = None
    User_MMR: int = None
    User_Connection_Time: float = None

def sendword(connectionSocket, number):
    while True:
        try:

            connectionSocket.send(str(number).encode())
            print("send function" + str(number))
            if(number < 2):
                connectionSocket.send("low".encode())
                
                print("send low")
            else:
                connectionSocket.send("up".encode())
                print("send up")
        
        except Exception as e:
            
            print('send error')
            print(e)
            break
        #sentence = connectionSocket.recv(1024).decode()

        # print(sentence)
        # if sentence == 'close':
        #     number = number - 1
        #     connectionSocket.close()
        #     print('close connect')
        #     break
        # else:
        #     connectionSocket.send(sentence.encode()) 
        # print('send error')
        # print(e)

def getword(connectionSocket, number):
    while(True):
        try:
            print("getfunction" + str(number))
            sentence = connectionSocket.recv(1024).decode()
            if sentence == "close":
                number = number - 1
                connectionSocket.close()
                print('close connect')
                break
            else:
                connectionSocket.send(sentence.encode()) 
                print(sentence)
        except Exception as e:
            number = number - 1
            print('get error')
            print(e)
            break

def MakeRoom(userarry, room):
    while(True):
        try:
            i = 0
            if(len(userarry) > 0):
                for j in range(len(userarry)):
                    for i in range(len(room)):
                        if(len(room[i]) == 1):
                            if(time.time() - userarry[j].User_Connection_Time > 15):
                                print("send Bot")
                                userarry[j].User_Socket.send("bot".encode())
                                tmp_user = userarry.pop(j)
                                for k in range(len(room)):
                                        if(room[k] is not None):
                                            if(room[k][0] == tmp_user):
                                                room[k].pop(0)
                            else:
                                if(room[i][0] != userarry[j]):
                                    MMR_Diff = abs(int(room[i][0].User_MMR) - int(userarry[j].User_MMR))
                                    MMR_Diff_MAX = abs(time.time() - userarry[j].User_Connection_Time) * 3
                                    if(MMR_Diff < MMR_Diff_MAX):
                                        print("room made")
                                        tmp_user = userarry.pop(j)
                                        room[i].append(tmp_user)
                                        tmp_user = room[i][0]
                                        for k in range(len(userarry)):
                                            if(userarry[k] == tmp_user):
                                                userarry.pop(k)

                                        for k in range(len(room)):
                                            if(k != i):
                                                if(room[k] is not None):
                                                    if(room[k][0] == tmp_user):
                                                        room[k].pop(0)
                                        break
                        elif(len(room[i]) == 0 and len(userarry) > 0):
                            room[i].append(userarry[j])
                            



                for i in range(10):
                    if(len(room[i]) == 2):
                        sendStart(room[i][0], room[i][1])
                        game1 = threading.Thread(target= fight,args= (room[i][0], room[i][1], userarry, room))
                        game2 = threading.Thread(target= fight,args= (room[i][1], room[i][0], userarry, room))
                        game1.daemon = True
                        game2.daemon = True
                        game1.start()
                        game2.start()

                        # fight(room[i][0],room[i][1])
                        # fight(room[i][1],room[i][0])
                        room.pop(0)
                        room.append([])
                    elif(len(room[i]) == 1):
                        sendWaiting(room[i])
        except Exception as e:

            print(e)

def sendStart(client1, client2):
    print("send start message")
    client1.User_Socket.send("start".encode())
    client2.User_Socket.send("start".encode())
    
def sendWaiting(room):
    for i in range(len(room)):
        room[i].User_Socket.send("Waiting".encode())
        time.sleep(0.1)
        print(room[i])
        print("Send Waiting")

def fight(client1, client2, userarry, room):
    while(True):
        try:
            sentence = client1.User_Socket.recv(1024).decode()
            if sentence == "lose":
                client1.User_Socket.send("lose".encode())
                client2.User_Socket.send("win".encode())
                client1.User_Socket.close()
                client2.User_Socket.close()
                print('close connect')
                break
            elif sentence == "close":
                print(len(userarry))
                for i in range(len(userarry)):
                    if(userarry[i] == client1):
                        userarry.pop(i)
                print(len(room))
                for i in range(len(room)):
                    if(len(room[i]) >= 1):
                        if(room[i][0] == client1):
                            room[i].pop(0)

                connectionSocket.close()
                print('close connect')
                break
            else:
                client2.User_Socket.send(sentence.encode())
                print(sentence)
        except Exception as e:
            print('fight error')
            print(e)
            break

def getClose(connectionSocket, userarry, room):
    while(True):
        try:
            sentence = connectionSocket.recv(1024).decode()
            if sentence == "close":
                print(len(userarry))
                for i in range(len(userarry)):
                    if(userarry[i] == connectionSocket):
                        userarry.pop(i)
                print(len(room))
                for i in range(len(room)):
                    if(len(room[i]) >= 1):
                        if(room[i][0] == connectionSocket):
                            room[i].pop(0)

                connectionSocket.close()
                print('close connect')
                break
        except Exception as e:
            print('get Close Error')
            print(e)
            break

def append_Socket(connectionSocket, userarry):
    try:
        sentence = connectionSocket.recv(1024).decode()
        connectionSocket
    except Exception as e:
        print(e)


def print_room(room):
    while(True):
        print(room)
        time.sleep(5)

serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

number = 0

userarry = []
room = []
for i in range(10):
    room.append([])
T1 = threading.Thread(target = MakeRoom, args= (userarry, room))
T1.daemon = True
T1.start()

T2 = threading.Thread(target = print_room, args = (room, ))
T2.daemon = True
T2.start()


while True:
    serverSocket.listen(1)
    print("server Start")
    connectionSocket, addr = serverSocket.accept()
    print(str(addr))
    #connectionSocket.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
    #connectionSocket.setblocking(False)
    # T2 = threading.Thread(target= getClose, args= (connectionSocket, userarry, room))
    # T2.daemon = True
    # T2.start()
    #getClose(connectionSocket,userarry,room)
    
    print("user come")
    asdf = time.time()
    tmp = User()
    tmp.User_Socket = connectionSocket
    tmp.User_MMR = connectionSocket.recv(1024).decode()
    tmp.User_Connection_Time = time.time()
    userarry.append(tmp)
    print(userarry[0])
    print(len(userarry))
    
    #userarry.append(connectionSocket)


    
    # T2 = threading.Thread(target = getword, args = (connectionSocket, number))
    # T2.daemon = True
    # T2.start()

    # while True:
        
    #     sentence = connectionSocket.recv(1024).decode()
    #     print(sentence)
    #     if sentence == 'close':
    #         connectionSocket.close()
    #         print('close connect')
    #         break
    #     else:
    #         connectionSocket.send(sentence.encode())



