import os
import math
import time
import socket
import struct

FLAGS = _ = None
DEBUG = False


def get_filedict(rootpath):
    files = {}
    with os.scandir(rootpath) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                info = get_fileinfo(entry.path)
                info['path'] = entry.path
                files[entry.name] = info
    return files


def get_fileinfo(path):
    size = 0
    value = None
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(1380)
            chunk_size = len(chunk)
            if chunk_size == 0: # if not data:
                break
            size = size + chunk_size
    return {'size': size}


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    files = get_filedict(FLAGS.files)
    if DEBUG:
        print(f'Ready to file transfer')
        for key, value in files.items():
            print(f'{key}: {value}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))
    print(f'Listening on {sock}')

    while True:
        try:
            data, client = sock.recvfrom(1380)
            data = data.decode('utf-8')
            data = data.split(' ')

            if len(data) < 2:
#                response = 'Error'
#                sock.sendto(response.encode('utf-8'), client)
                continue

            command = data[0].upper()
            target = ' '.join(data[1:])
            print(f'{command} {target} from {client}')


            if target not in files.keys():
                print(f'{target} was not found (requested by {client})')
                response = '404 Not Found'
                sock.sendto(response.encode('utf-8'), client)
                continue

            info = files[target]
            path = info['path']
            size = info['size']

            if command == 'INFO':
                response = f'{size}'
                sock.sendto(response.encode('utf-8'), client)
            elif command == 'DOWNLOAD':
                remain = size
                cache = []
                window = []
                for i in range(16):
                    cache.append(None)
                    window.append(i)
                seq = 0
                cseq = 0
                cseq2 = 0
                lseq = window[0]
                rseq = window[15]
                nseq = seq
                sock.settimeout(FLAGS.timeout)
                status_transfer = True
                status_reading = True
                with open(path, 'rb') as f:
                    while status_transfer:
                        if seq != rseq:
                            if cache[seq] == None:
                                read = f.read(1379)
                                if len(read) == 0:
                                    #if DEBUG:
                                    #    print(f'Read All: {seq} {lseq} {rseq} {nseq} {cseq}')
                                    rseq = seq
                                    continue
                                cache[seq] = read
                                remain = remain - len(read)
                            byte_chunk = cache[seq]
                            byte_seq = struct.pack('>B', seq)
                            chunk = byte_seq + byte_chunk
                            if DEBUG:
                                print(f'Transfering to {client} with {seq}/{rseq}: {size-remain}/{size}')
                                input()
                            sock.sendto(chunk, client)
                            seq = (seq+1)%16
                        else:
                            #nseq = window[0]
                            while True:
                                try:
                                    data, client = sock.recvfrom(1380)
                                    cseq = struct.unpack('>B', data[:1])[0]
                                    #if DEBUG:
                                    #    print(f'Ack Received Our: {seq}, Client: {cseq}, Next: {nseq}, Right: {rseq}')
                                    if rseq == cseq:
                                        if remain == 0:
                                            status_transfer = False
                                        nseq = cseq
                                        if DEBUG:
                                            print(f'Ack Received, Server: {seq}, Client: {cseq}, Next: {nseq}, Right: {rseq}')
                                        #sock.settimeout(0.000001)
                                        sock.settimeout(10**-6)
                                        while True:
                                            try:
                                                data, client = sock.recvfrom(1380)
                                            except socket.timeout:
                                                sock.settimeout(FLAGS.timeout)
                                                break
                                        break
                                    elif window.index(nseq) < window.index(cseq):
                                        nseq = cseq
                                    if DEBUG:
                                        print(f'Ack Received, Server: {seq}, Client: {cseq}, Next: {nseq}, Right: {rseq}')
                                except socket.timeout:
                                    break
                            while window[0] != nseq:
                                rseq = window.pop(0)
                                cache[rseq] = None
                                window.append(rseq)
                            lseq = window[0]
                            rseq = window[15]
                            seq = lseq
                while True:
                    try:
                        data, client = sock.recvfrom(1380)
                    except socket.timeout:
                        break
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.bind((FLAGS.address, FLAGS.port))
                sock.settimeout(None)
            print(f'File transfer complete {target}')
        except KeyboardInterrupt:
            print(f'Shutting down... {sock}')
            break


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')
    parser.add_argument('--address', type=str, default='0.0.0.0',
                        help='The address to serve service')
    parser.add_argument('--port', type=int, default=38442,
                        help='The port to serve service')
    parser.add_argument('--timeout', type=int, default=3,
                        help='The timeout seconds')
    parser.add_argument('--files', type=str, default='./files',
                        help='The file directory path')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    FLAGS.files = os.path.abspath(os.path.expanduser(FLAGS.files))

    main()

