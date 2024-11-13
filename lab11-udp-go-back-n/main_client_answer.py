import time
import socket
import struct

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'Ready to send using {sock}')

    sock.settimeout(5)
    try:
        # filename = input('Filename: ').strip()
        filename = 'unittest'
        stime = time.time()
        request = f'INFO {filename}'
        sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))

        response, server = sock.recvfrom(1380)
        response = response.decode('utf-8')
        if response == '404 Not Found':
            print('404 Not Found')
        size = int(response)

        request = f'DOWNLOAD {filename}'
        sock.sendto(request.encode('utf-8'), (FLAGS.address, FLAGS.port))
        print(f'Request {filename} to ({FLAGS.address}, {FLAGS.port})')

        remain = size
        seq = 0
#            sock.settimeout(FLAGS.timeout)
        with open(filename, 'wb') as f:
            while remain > 0:
                while True:
                    chunk, server = sock.recvfrom(1380)
                    byte_seq = chunk[:1]
                    byte_chunk = chunk[1:]
                    sseq = struct.unpack('>B', byte_seq)[0]
                    if seq == sseq:
                        break
                    else:
                        if DEBUG:
                            print(f'패킷 잘못왔음. 원한거: {seq}, 받은거: {sseq} 다시보내기')
                        sock.sendto(struct.pack('>B', seq), server)
                remain = remain - len(byte_chunk)
                f.write(byte_chunk)
                if DEBUG:
                    #print(f'Receiving from {server} with {seq}: {size-remain}/{size}')
                    print(f'Receiving from {server} with {seq}: {size-remain}/{size} [{byte_chunk.hex()[:8*2]}]')
                seq = (seq+1)%16
                sock.sendto(struct.pack('>B', seq), server)
        etime = time.time()
        sock.settimeout(FLAGS.timeout*2)
        while True:
            try:
                chunk, server = sock.recvfrom(1380)
                sock.sendto(struct.pack('>B', seq), server)
            except socket.timeout:
                break
            
        print(f'File download success')
        sock.settimeout(None)
        print(f'{filename} download during {etime-stime}')
        print(f'> Throughput: {round((size*8)/(etime-stime)):,d} bps')
        
    except socket.timeout:
        exit()
        
    except KeyboardInterrupt :
        print(f'Shutting down... {sock}')
        exit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='localhost',
                        help='The address to send data')
    parser.add_argument('--port', type=int, default=38442,
                        help='The poort to send data')
    parser.add_argument('--timeout', type=int, default=3,
                        help='The timeout seconds')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()


