from socket import *
import threading
from dataclasses import dataclass
import time


Max_Waiting_time = 15
Max_Room = 10
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

def MakeRoom(userarry, room): # 유저 입력 받아 매칭 시켜주는 함수
    while(True):
        try:
            i = 0
            if(len(userarry) > 0):
                for j in range(len(userarry)):
                    for i in range(len(room)):
                        if(len(room[i]) == 1):
                            if(time.time() - userarry[j].User_Connection_Time > Max_Waiting_time): # 최대 매칭 시간에 따른 코드 동작
                                print("send Bot") # 최대 매칭 시간 초과시 봇 시동 메세지 전송
                                userarry[j].User_Socket.send("bot".encode())
                                tmp_user = userarry.pop(j)
                                for k in range(len(room)):
                                        if(room[k] is not None):
                                            if(room[k][0] == tmp_user):
                                                room[k].pop(0)
                            else: # 유저 MMR 비교 
                                if(room[i][0] != userarry[j]): # 이미 방에 들어가있는 유저와 다른 유저 비교함
                                    MMR_Diff = abs(int(room[i][0].User_MMR) - int(userarry[j].User_MMR))
                                    MMR_Diff_MAX = abs(time.time() - userarry[j].User_Connection_Time) * 3 # 웨이팅 시간에 따른 매칭 MMR 범위 결정

                                    if(MMR_Diff < MMR_Diff_MAX): # 매칭 MMR 조건 충족시 매칭 후 게임 스타트
                                        print("room made")
                                        tmp_user = userarry.pop(j) # 현재 비교하교 있는 유저를 방에 입장시킴
                                        room[i].append(tmp_user)

                                        tmp_user = room[i][0] # 이미 방에 들어가 있는 유저를 다른 방에서 빼주기 위한 코드
                                        for k in range(len(userarry)): # 대기열에 있는 유저 빼줌
                                            if(userarry[k] == tmp_user):
                                                userarry.pop(k)

                                        for k in range(len(room)): # 방에 들어가 있는 유저 빼줌
                                            if(k != i):
                                                if(room[k] is not None):
                                                    if(room[k][0] == tmp_user):
                                                        room[k].pop(0)
                                        break
                        elif(len(room[i]) == 0 and len(userarry) > 0): # 방에 아무도 없으면 대기 유저 방에 입장시킴
                            room[i].append(userarry[j])

# todo
# 최초 입력시 모든 방에 최초들어온 인원 들어감
# 이때 다음 인원이 들어오면 기존 조건에 의해 다른 방에 못들어감
# 방의 인원이 1명이면 매칭이 안된 상대는 방에 들어가야 됨
# 어케?                          
                            



                for i in range(Max_Room): # 모든 방 체크해서 유저가 2명이면 게임 시작 쓰레드 동작 시켜줌
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
                    elif(len(room[i]) == 1): # 방의 유저가 1명이면 waiting 메세지 보내줌
                        sendWaiting(room[i])
        except Exception as e:

            print(e)


def MakeRoom_New_Version(userarry, room): # 2중 for문을 이용한 매치 메이킹
    while(True):
        
        try:
            User_Num = len(userarry)

            if(User_Num == 0):      # 대기 유저 0명 일때는 동작 수행 X
                pass

            elif(User_Num == 1):    # 대기 유저 1명일때는 1명한테 waiting 메세지 보냄
                sendWaiting(userarry[0])

            elif(User_Num > 1):     # 대기 유저 2명 이상일때는 매치메이킹 시도
                for i in range(User_Num):
                    Current_User:User = userarry[i]

                    # 대기시간이 맥스 대기시간 초과하면 봇 메세지 전송
                    Waiting_Time = time.time() - Current_User.User_Connection_Time
                    if(Waiting_Time > Max_Waiting_time):
                        print("send bot message")
                        Current_User.User_Socket.send("bot".encode())
                        userarry.pop(i)

                    else:
                        for j in range(User_Num):
                            if(i == j):
                                pass
                            else:
                                Compare_User:User = userarry[j]

                                MMR_Diff = abs(Current_User.User_MMR - Compare_User.User_MMR)
                                MMR_MAX_DIFF = abs(Waiting_Time * 3)

                                if(MMR_Diff < MMR_MAX_DIFF): # 매칭 조건 충족시 room에 넣어주고 대기열에서 빼줌
                                    print("room made")
                                    tmp_list = [Current_User, Compare_User]
                                    room.pop(0)
                                    room.append(tmp_list)
                                    userarry.pop(i)
                                    userarry.pop(j)


            # 대기 유저에게 웨이팅 메세지 보내줌
            # 해당 역할을 하는 다른 쓰레드로 대체


            # room 검사 단계
            for r in room:
                if(len(r) == 2):
                    print("Game start")
                    sendStart(r[0], r[1])
                    game1 = threading.Thread(target= fight,args= (r[0], r[1], userarry, room))  # client 1에서 client 2로 메세지 보내는 쓰레드 실행
                    game1.daemon = True
                    game1.start()

                    game2 = threading.Thread(target= fight,args= (r[1], r[0], userarry, room))  # client 2에서 client 1로 메세지 보내는 쓰레드 실행
                    game2.daemon = True
                    game2.start()

                    room.pop(0)
                    room.append([])


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

def send_Waiting_using_Userarray(userarray):
    while(True):
        try:
            if(len(userarray) >=1):
                user:User
                for user in userarry:
                    user.User_Socket.send("Waiting".encode())
            else:
                pass
            time.sleep(0.1)
        except Exception as e:
            pass
    

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
        try:
            print(room)
            time.sleep(5)
        except Exception as e:
            pass


serverPort = 1234
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))

number = 0

userarry = []
room = []
for i in range(Max_Room):
    room.append([])

T1 = threading.Thread(target = MakeRoom_New_Version, args= (userarry, room))
T1.daemon = True
T1.start()

T2 = threading.Thread(target = print_room, args = (room, ))
T2.daemon = True
T2.start()

T3 = threading.Thread(target = send_Waiting_using_Userarray, arge = (userarry, ))
T3.daemon = True
T3.start()

while True:
    serverSocket.listen(1)
    print("server Start")
    connectionSocket, addr = serverSocket.accept()
    print("User Come" + str(addr))

    asdf = time.time()
    tmp = User()
    tmp.User_Socket = connectionSocket
    tmp.User_MMR = connectionSocket.recv(1024).decode()
    tmp.User_Connection_Time = time.time()
    userarry.append(tmp)