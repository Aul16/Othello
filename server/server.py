import socket as sc
from _thread import *
from game import Game
import pickle

server = "0.0.0.0"
port = 5555

s = sc.socket(sc.AF_INET, sc.SOCK_STREAM)  # Défini type de connexion


try:
    s.bind((server, port))  # Connecte au serveur
except sc.error as e:
    str(e)


s.listen()
print("Waiting for a connection, Server Started")


connected = set()
games = {}


def threaded_client(conn, player_number, game, gameId):
    if player_number == 2:
        game.ready = True

    reply = ""
    data = conn.recv(2048).decode()
    while data:
        if gameId in games:
            game = games[gameId]

            if (
                player_number == game.player_turn and data != "get"
            ):  # Joue le coup si le bon joueur
                coo = data.split(",")
                game.jouer_coup(game.player_turn, (int(coo[0]), int(coo[1])))

            reply = game
            conn.sendall(pickle.dumps(reply, pickle.HIGHEST_PROTOCOL))

            data = conn.recv(2048).decode()
        else:
            break

    # Quit game
    print("Lost connection")
    if player_number == 1:
        try:
            del games[gameId]
        except:
            pass
    conn.close()


# Main loop : handle connection
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    gameId = conn.recv(2048).decode()  # Receive gameId
    print(type(gameId))
    conn.send(
        pickle.dumps("Ok", pickle.HIGHEST_PROTOCOL)
    )  # Send ok to client to confirm

    if not gameId in games.keys():  # If game doesn't exist
        games[gameId] = Game(nb_players=2)  # Create new game
        player_number = 1  # Set player number to 1
        print("Creating a new game:", gameId)

        conn.send(str.encode(str(player_number)))  # Send whose player it is
        start_new_thread(threaded_client, (conn, player_number, games[gameId], gameId))

    elif not games[gameId].ready:  # Prevent from having too much player
        player_number = 2  # If game does exist, set player number to 2
        games[gameId].ready = True
        print("Joining game: ", gameId)
    

        conn.send(str.encode(str(player_number)))  # Send whose player it is
        start_new_thread(threaded_client, (conn, player_number, games[gameId], gameId))
