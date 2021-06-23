import socket
import sys
import pickle
from _thread import *
from player import Player

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


players = [Player(150, 600, 0, 0),
           Player(600, 600, 1, 0)]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            print(f"player : {player}")
            data = pickle.loads(conn.recv(2048))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if (player == 1):
                    reply = players[0]
                else:
                    reply = players[1]

                print("Recieved : ", reply)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))

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
