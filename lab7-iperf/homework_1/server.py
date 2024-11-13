import time
import socket

# 수신할 IP 주소와 포트 번호를 설정합니다.
HOST = '127.0.0.1'
PORT = 1234

# 소켓 객체를 생성합니다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 소켓을 바인드합니다.
server_socket.bind((HOST, PORT))

# 클라이언트의 연결 요청을 대기합니다.
server_socket.listen()

# 클라이언트의 연결 요청을 수락합니다.
client_socket, addr = server_socket.accept()

# 수신할 파일의 경로를 설정합니다.
filename = 'receive_file.bin'

# 데이터 블록 크기를 설정합니다.
block_size = 128

# 파일을 바이너리 모드로 열어서 쓰기 모드로 생성합니다.
with open(filename, 'wb') as f:
    # 시작 시간을 측정합니다.
    start_time = time.time()
    # 데이터를 수신받아 파일에 씁니다.
    data = client_socket.recv(block_size)
    while data:
        f.write(data)
        data = client_socket.recv(block_size)
    # 수신이 완료되면 종료 시간을 측정합니다.
    end_time = time.time()

# 소켓을 닫습니다.
client_socket.close()
server_socket.close()

# 수신 시간을 계산합니다.
duration = end_time - start_time
speed = (len(open(filename, 'rb').read()) / (1024 * 1024)) / duration  # 수신 속도를 계산합니다.

print(f'파일 수신 완료: {filename}')
print(f'수신 시간: {duration:.2f}초')
print(f'수신 속도: {speed:.2f} MB/s')
