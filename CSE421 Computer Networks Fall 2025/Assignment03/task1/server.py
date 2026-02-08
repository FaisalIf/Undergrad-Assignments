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

len_encoded_msg = conn.recv(FIRST_CONTACT_DATA_LENGTH).decode()
if len_encoded_msg:
    msg_from_client = conn.recv(int(len_encoded_msg)).decode()
    
    print("\n****** <Client> ******")
    print(msg_from_client)
    print("****** </Client> ******\n")

conn.close()
server.close()
