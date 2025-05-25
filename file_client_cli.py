import socket
import json
import base64
import logging
import os

server_address=('0.0.0.0',7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        data_received="" 
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except:
        logging.warning("error during data receiving")
        return False


def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str=f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        namafile= hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile,'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    if not os.path.exists(filepath):
        print(f"Error: File {filepath} not found")
        return False
    
    filename = os.path.basename(filepath)
    
    with open(filepath, 'rb') as fp:
        file_content = fp.read()
        file_content_b64 = base64.b64encode(file_content).decode()
    
    command_str = f'UPLOAD "{filename}" "{file_content_b64}"'
    
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(hasil['data'])
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False

def remote_delete(filename=""):
    command_str=f'DELETE "{filename}"'
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print(hasil['data'])
        return True
    else:
        print(f"Gagal: {hasil['data']}")
        return False


if __name__=='__main__':
    server_address=('172.16.16.101',7777)
    remote_list()
    # remote_get('donalbebek.jpg')
    # Test upload
    # remote_upload('pokijan2.jpg')
    # Test delete
    remote_delete('pokijan2.jpg')