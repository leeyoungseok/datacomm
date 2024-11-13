import time
import socket

# 서버의 IP 주소와 포트 번호를 설정합니다.
HOST = '127.0.0.1'
PORT = 1234

# 소켓 객체를 생성합니다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 서버와 연결합니다.
client_socket.connect((HOST, PORT))

# 송신할 파일의 경로를 설정합니다.
filename = 'send_file.bin'

# 데이터 블록 크기(바이트)를 설정합니다.
block_size = 128

# 파일을 바이너리 모드로 열어서 읽습니다.
with open(filename, 'rb') as f:
    # 시작 시간을 측정합니다.
    start_time = time.time()
    # 파일 데이터를 읽어서 서버에 전송합니다.
    data = f.read(block_size)
    while data:
        client_socket.send(data)
        data = f.read(block_size)
    # 송신이 완료되면 종료 시간을 측정합니다.
    end_time = time.time()


# 소켓을 닫습니다.
client_socket.close()

# 송신 시간을 계산합니다.
duration = end_time - start_time
speed = (len(open(filename, 'rb').read()) / (1024 * 1024)) / duration  # 전송 속도를 계산합니다.

print(f'파일 송신 완료: {filename}')
print(f'전송 시간: {duration:.2f}초')
print(f'전송 속도: {speed:.2f} MB/s')