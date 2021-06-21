import socket
from _thread import *
import sys

# Local
server = "192.168.1.13"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

# Max client
s.listen(2)

print("Waiting for a connection, server started")


# baca posisi player
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


# starting position
pos = [(250, 600), (500, 600)]


def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            print(f"player : {player}")
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if (player == 1):
                    reply = pos[0]
                else:
                    reply = pos[1]

                print("Recieved : ", reply)
                print("Sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))

        except:
            print("Error")
            break
    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
