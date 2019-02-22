# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:29:35 2019

@author: Administrator
"""

import socket
import threading
import time

global dest_ip
global dest_port

def send_msg(udp_socket):
    global dest_ip
    global dest_port
    send_data = input("请输入要发送的消息：")
    udp_socket.sendto(send_data.encode("utf-8"),(dest_ip,dest_port))

def recv_msg(udp_socket):
    while True:
        recv_data = udp_socket.recvfrom(1024)
        if recv_data:
            print("%s -- %s" % (str(recv_data[1]), time.ctime(time.time())))
            print("%s" % recv_data[0].decode("utf-8"))

def main():
    global dest_ip
    global dest_port
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定信息
    udp_socket.bind(("", 9050))
    print("-----聊天-----")
    dest_ip = input("请输入对方的ip:")
    dest_port = int(input("请输入对方的port:"))

    recv_thread = threading.Thread(target=recv_msg,args=(udp_socket,))
    recv_thread.setDaemon(True)
    recv_thread.start()
    
    while True:     
        option = input("请输入功能:1.发送\t2.退出\n")
        if (option == '1'):
            send_msg(udp_socket)
        elif(option == '2'):
            udp_socket.close()
            break

if __name__ == "__main__":
    main()
