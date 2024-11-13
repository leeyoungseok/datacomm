import socket
import os
import hashlib

def calculate_checksum(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    server_ip = '0.0.0.0'  # 서버 IP 주소
    server_port = 12000 # 서버 포트 번호

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((server_ip, server_port))
    print('UDP 서버가 시작되었습니다.')

    while True:
        data, addr = server_socket.recvfrom(1024)
        if data.decode() == 'END':
            break

        # 클라이언트의 IP 주소 출력
        client_ip = addr[0]
        #print(f'클라이언트 IP: {client_ip}')

        if data.decode() == 'ServerCheck':
            print(f'클라이언트 IP: {client_ip} 확인')
            server_socket.sendto(b'ServerReady', addr)
            continue

        # 학번에 해당하는 파일 전송
        student_id = data.decode()
        print(f'클라이언트({client_ip})가 요청한 학번 : {student_id}')
        file_path = f'./files/{student_id}.jpg'

        if os.path.isfile(file_path) == False:
            print(f'{student_id}는 존재하지 않습니다.')
            # server_socket.sendto(b'FileNotFound', addr)
            server_socket.sendto(b'FileNotFound', addr)
            continue
            
        if os.path.isfile(file_path):
            server_socket.sendto(b'Sending now!', addr)
            with open(file_path, 'rb') as file:
                chunk = file.read(1024)
                while chunk:
                    server_socket.sendto(chunk, addr)
                    chunk = file.read(1024)
            
            # 파일 체크섬 전송
            checksum = calculate_checksum(file_path)
            print(checksum)
            print('파일 전송이 완료되었습니다.')

    server_socket.close()

if __name__ == '__main__':
    main()


