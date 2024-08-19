import socket
import threading

clients = set()
clients_lock = threading.Lock()
server_running = True

def listener(client, address):
    print("Accepted connection from:", address)
    with clients_lock:
        clients.add(client)
    try:
        while server_running:
            data = client.recv(1024)
            if not data:
                break
            else:
                print(repr(data))
                if b'PASS' in data:
                    msg = """:tmi.twitch.tv 001 bbuzhibujuelllll :Welcome, GLHF!
:tmi.twitch.tv 001 bbuzhibujuelllll :Welcome, GLHF!
:tmi.twitch.tv 002 bbuzhibujuelllll :Your host is tmi.twitch.tv
:tmi.twitch.tv 003 bbuzhibujuelllll :This server is rather new
:tmi.twitch.tv 004 bbuzhibujuelllll :-
:tmi.twitch.tv 375 bbuzhibujuelllll :-
:tmi.twitch.tv 372 bbuzhibujuelllll :You are in a maze of twisty passages, all alike.
:tmi.twitch.tv 376 bbuzhibujuelllll :>
"""
                    data = msg.encode('ascii')
                if b'JOIN' in data:
                    msg = """:bbuzhibujuelllll!bbuzhibujuelllll@bbuzhibujuelllll.tmi.twitch.tv JOIN #bbuzhibujuelllll
:bbuzhibujuelllll.tmi.twitch.tv 353 bbuzhibujuelllll = #bbuzhibujuelllll :bbuzhibujuelllll
"""
                    data = msg.encode('ascii')
                with clients_lock:
                    for c in clients:
                        c.sendall(data)
                        print(data.decode('utf-8'))
    except ConnectionAbortedError:
        pass
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()

host = '0.0.0.0'
port = 6667

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(3)
threads = []

def accept_connections():
    global server_running
    while server_running:
        try:
            print("Server is listening for connections...")
            client, address = s.accept()
            thread = threading.Thread(target=listener, args=(client, address))
            thread.start()
            threads.append(thread)
        except OSError:
            break

accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

try:
    while True:
        accept_thread.join(1)
except KeyboardInterrupt:
    print("Shutting down server...")
    server_running = False
    s.close()
    with clients_lock:
        for client in clients:
            client.close()
    for thread in threads:
        thread.join()
    print("Server has been shut down.")
