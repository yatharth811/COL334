from socket import *
import threading
import pickle


SERVER = '127.0.1.1'
PORT = 5050
ADDR = (SERVER, PORT)
HEADER = 2048
FORMAT = 'utf-8'
COUNT = 2

def ceil(a, b):
    return (a+b-1)//b

def send(client, msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)


def createNewClientSocket(i):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDR)

    rcvd_sum = 0
    send(client, f'#{i}')
    container = pickle.loads(client.recv(2048))


    lsz = container[0]
    print(f'Len: {lsz}')
    print(i, container[1])
    rcvd_sum += len(container[1])

    #last packet => (i+1)*(container[0]/COUNT) + 1 
    packet = (min((i+1)*ceil(lsz, COUNT)-1, lsz-1) + 1)%lsz

    while(rcvd_sum != lsz):
        send(client, f'#R{packet}')
        print(i, pickle.loads(client.recv(2048)))
        rcvd_sum += 1
        packet = (packet+1)%lsz
    
    send(client, '!DISCONNECT')
    


for i in range(0, COUNT):
    thread = threading.Thread(target=createNewClientSocket, args=(i, ))
    thread.start()


