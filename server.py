import socket, time, json, threading
from queue import Queue

connection = False
handshake = False
transfer = Queue()
receive = Queue()

if __name__ == "__main__":
    main = True
else:
    main = False

def get(request):
    if request == "conn" or request == "connection":
        return connection
    if request == "f_ip":
        return conn_ip
    if request == "handshake":
        return handshake

def start_server(ip):
    t = threading.Thread(target=server_side, args=(ip,))
    t.daemon = True
    t.start()

def start_client(ip):
    t = threading.Thread(target=client_side, args=(ip,))
    t.daemon = True
    t.start()

def do_transfer(data):
    msg = "DATA:" + json.dumps(data)
    transfer.put(msg)

def get_receive():
    if receive:
        buffer = receive.get()
        buffer = json.loads(buffer)
        return buffer
    return None

def server_side(ip):
    global transfer, receive, handshake, connection, conn_ip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((ip, 5000))
            conn_ip = ip
        except:
            print("Failed to start a server...")
            return
        s.listen()
        conn, addr = s.accept()
        with conn:
            connection = True
            try:
                while True:
                    try:
                        data = conn.recv(1024)
                        #print("\nSERVER: Raw received", data)
                        data = data.decode("utf-8")
                        #print("\nSERVER: Server received", data[5:])
                        if not data == "handshake":
                            receive.put(data[5:])
                        else:
                            if main:
                                print("Handshake")
                            handshake = True
                    except: pass
                
                    string = "handshake"
                    if transfer:
                        transfer_data = transfer.get()
                        conn.sendall(transfer_data.encode("utf-8"))
                    else:
                        conn.sendall(string.encode("utf-8"))
                    time.sleep(0.05)
            except:
                print("Disconnected")
                return
                            
                
def client_side(ip):
    global transfer, receive, handshake, connection, conn_ip
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, 5000))
            conn_ip = ip
        except:
            print("Connection failed... Are you sure the Host has started")
        connection = True
        while True:
            try:
                string = "handshake"
                if transfer:
                    transfer_data = transfer.get()
                    s.sendall(transfer_data.encode("utf-8"))
                else:
                    s.sendall(string.encode("utf-8"))
                try:
                    received = s.recv(1024)
                    #print("\nSERVER: Raw Received", received)
                    received = received.decode("utf-8")
                    #print("\nSERVER: Client received", received[5:])
                    if not received == "handshake":
                        receive.put(received[5:])
                    else:
                        if main:
                            print("Handshake")
                        handshake = True
                except: pass
                time.sleep(0.05)
            except:
                if main:
                    print("Error")
                break
