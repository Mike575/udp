import socket


def send_msg(udp_socket):
    dest_ip = input("请输入对方的ip:")
    dest_port = int(input("请输入对方的port:"))
    send_data = input("请输入要发送的消息：")
    udp_socket.sendto(send_data.encode("utf-8"),(dest_ip,dest_port))

def recv_msg(udp_socket):
    recv_data = udp_socket.recvfrom(1024)
    print(recv_data)
    #print("&s:%s" % (str(recv_data[1]), recv_data[0].decode("utf-8")))

def main():
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定信息
    udp_socket.bind(("", 7789))
    print("-----udp碰撞误差统计-----")
    op = input("作为接受端按 1，作为发送端按 2, 结束 0\n")

    while True:
        if (op == "2"):
            # 发送
            send_msg(udp_socket)
        elif (op == "1"):
            # 接受并显示
            recv_msg(udp_socket)
        elif (op == "0"):
            break;
        else:
            print("输入有误请重新输入")
            break;
    udp_socket.close()

if __name__ == "__main__":
    main()
