import socket

PORT = 5173
DEVICE_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(DEVICE_NAME)
SOCKET_ADDR = (SERVER_IP, PORT)
EXCHANGE_FORMAT = "utf-8"
FIRST_CONTACT_DATA_LENGTH = 10

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SOCKET_ADDR)

def send_message(msg):
    encoded_msg = msg.encode(EXCHANGE_FORMAT)
    len_encoded_msg = len(encoded_msg)
    str_for_server = str(len_encoded_msg) + " " * (FIRST_CONTACT_DATA_LENGTH - len(str(len_encoded_msg)))
    client.send(str_for_server.encode(EXCHANGE_FORMAT))
    
    str_for_server = encoded_msg
    client.send(str_for_server)

client_ip = client.getsockname()[0]
send_message(f"Client IP: {client_ip}, Device Name: {DEVICE_NAME}")

client.close()
