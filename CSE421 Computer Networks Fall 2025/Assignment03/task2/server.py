import socket

PORT = 5173
DEVICE_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(DEVICE_NAME)
SOCKET_ADDR = (SERVER_IP, PORT)
EXCHANGE_FORMAT = "utf-8"
FIRST_CONTACT_DATA_LENGTH = 10

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SOCKET_ADDR)
server.listen()
print(f"########## Server listening on {PORT} ##########")

conn, client_addr = server.accept()
print(f"########## Connected to client with address {client_addr} ##########")

connected = True
while connected:
    len_encoded_msg = conn.recv(FIRST_CONTACT_DATA_LENGTH).decode()
    if len_encoded_msg:
        msg_from_client = conn.recv(int(len_encoded_msg)).decode()
        
        print("\n****** <Client> ******")
        print(msg_from_client)
        print("****** </Client> ******\n")
        
        if msg_from_client.strip().lower() == "terminate":
            conn.send("Goodbye.".encode(EXCHANGE_FORMAT))
            connected = False
            print(f"########## Received termination order from client: {client_addr} ##########")
        else:
            vowel_count = sum(1 for char in msg_from_client.lower() if char in "aeiou")
            
            if vowel_count == 0:
                response = "Not enough vowels"
            elif vowel_count <= 2:
                response = "Enough vowels I guess"
            else:
                response = "Too many vowels"
            
            conn.send(response.encode(EXCHANGE_FORMAT))

conn.close()
server.close()
