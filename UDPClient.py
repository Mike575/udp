# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 20:53:09 2019

@author: Administrator
"""

import socket

def main():
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定信息
    udp_socket.bind(("", 9040))
    while True:
        try:
            recv_data = udp_socket.recvfrom(1024)
            print(recv_data[0].decode("utf-8"))
        except:           
            udp_socket.close()
            break;

if __name__ == "__main__":
    main()
