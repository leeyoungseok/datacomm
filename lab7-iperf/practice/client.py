import iperf3
import matplotlib.pyplot as plt

def create_client(server_ip, port):
    client = iperf3.Client()
    client.server_hostname = server_ip
    client.port = port
    return client

def plot_bandwidth(result_json):
    intervals = result_json["intervals"]
    bandwidths = [interval["sum"]["bits_per_second"] * 1e-6 for interval in intervals]

    plt.plot(bandwidths)
    plt.xlabel("Interval Index")
    plt.ylabel("Bandwidth (Mbps)")
    plt.title("Bandwidth Over Time")
    plt.savefig("bandwidth_graph.png", dpi=300)
    plt.close()

def main():
    ## 작성해야할 부분
    ## 서버의 IP주소와 PORT 번호 작성
    ## server_ip, port = 
    ##
    client = create_client(server_ip, port)
    client.duration = 5
    result = client.run()
    plot_bandwidth(result.json)
    
if __name__ == "__main__":
    main()
