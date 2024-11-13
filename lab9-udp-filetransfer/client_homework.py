import socket
import hashlib

def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def connect_to_server(server_ip, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)  # 타임아웃 설정 (예: 5초)

    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print('서버가 오프라인 입니다')
        return None

    print('서버가 온라인입니다.')
    return client_socket

def send_connection_check(client_socket:socket.socket, server_ip, server_port):
    client_socket.sendto(b'ConnectionCheck', (server_ip, server_port))

    try:
        response, _ = client_socket.recvfrom(1024)
    except socket.timeout:
        print('서버 응답을 기다리는 동안 타임아웃이 발생하였습니다.')
        client_socket.close()
        return None
    
    if response is None:
        client_socket.close()
        return None

    if response != b'Connected':
        print('서버 연결에 실패하였습니다.')
        client_socket.close()
        return None

    return response

def send_student_id(client_socket:socket.socket, student_id:str, server_ip, server_port):
    
    ## 작성할 부분 ##
    client_socket.sendto(client_socket.sendto(student_id.encode(), (server_ip, server_port)))
    response, _ = 
    #################
    
    if response == b'FileNotFound':
        print('서버에 요청한 파일이 존재하지 않습니다.')
        client_socket.close()
        exit()
        
    return response

def receive_file(client_socket:socket.socket, student_id:str):
    file_path = f'{student_id}.jpg'
    with open(file_path, 'wb') as file:
        while True:
            try:
                response, _ = client_socket.recvfrom(1024)
                file.write(response)
            except socket.timeout:
                break
            if response == b'END':
                break
    return file_path

def download_file(server_ip, server_port):
    student_id = input('다운로드할 학번을 입력하세요: ')
    
    client_socket = connect_to_server(server_ip, server_port)
    if client_socket is None:
        return

    send_connection_check(client_socket, server_ip, server_port)
    send_student_id(client_socket, student_id, server_ip, server_port)

    file_path = receive_file(client_socket, student_id)
    client_socket.close()
    print(f'파일 다운로드가 완료되었습니다. 저장 위치: {file_path}')

    calculated_checksum = calculate_checksum(file_path)
    print(calculated_checksum)

if __name__ == '__main__':
    server_ip = '' 
    server_port = 0
    download_file(server_ip, server_port)
