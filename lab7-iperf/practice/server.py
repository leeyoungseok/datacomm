# server.py
import iperf3

def create_server(port):
    server = iperf3.Server()
    server.bind_port = port
    return server

def main():
    port = 5201
    server = create_server(port)
    server.run()

if __name__ == "__main__":
    print("Start Server")
    print("Waiting Client..")
    main()
    print("Done")