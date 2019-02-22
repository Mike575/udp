# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 21:29:35 2019

@author: Administrator
"""

import socket
import threading
import time
import inspect
import ctypes
import traceback

global dest_ip
global dest_port


def _async_raise(tid, exctype):
   """raises the exception, performs cleanup if needed"""
   tid = ctypes.c_long(tid)
   if not inspect.isclass(exctype):
      exctype = type(exctype)
   res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
   if res == 0:
      raise ValueError("invalid thread id")
   elif res != 1:
      # """if it returns a number greater than one, you're in trouble,
      # and you should call it again with exc=NULL to revert the effect"""
      ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
      raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
   _async_raise(thread.ident, SystemExit)


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

def waitOrder(udp_socket):
    try:
        print("wait order")
        recv_data = udp_socket.recvfrom(1024)
        print("recv order")
        if recv_data:
            message = recv_data[0].decode("utf-8")
            orderhost = recv_data[1]
            orderhost_ip = orderhost[0]
            orderhost_port = orderhost[1]
            answer = "收到命令"
            udp_socket.sendto(answer.encode("utf-8"),
                              (orderhost_ip, orderhost_port))
            order = message.split(' ')  #"127.0.0.1 9050 1000"
            dest_ip = order[0]
            dest_port = int(order[1])
            send_times = int(order[2])
            for i in range(send_times):
                send_data = str(i)
                udp_socket.sendto(send_data.encode("utf-8"), (dest_ip, dest_port))
        else:
            print("nothing")
    except Exception as e:
        print ('str(Exception):\t', str(Exception))
        print ('str(e):\t\t', str(e))
        print ('repr(e):\t', repr(e))
        print ('traceback.print_exc():', traceback.print_exc())
        print ('traceback.format_exc():\n%s' % traceback.format_exc())
        print ('########################################################')


def main():
    global dest_ip
    global dest_port
    # 创建套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 绑定信息
    udp_socket.bind(("", 9052))
    
    try:
    
        print("-----聊天-----")
        dest_ip = input("请输入对方的ip:")
        dest_port = int(input("请输入对方的port:"))
    
        recv_thread = threading.Thread(target=recv_msg,args=(udp_socket,))
        recv_thread.setDaemon(True)
        recv_thread.start()
        while True:
            option = input("请输入功能:1.聊天\t2.退出\t3.等待命令\n")
            if (option == '1'):
                if recv_thread.isAlive == False:
                    recv_thread.start()
                send_msg(udp_socket)
            elif(option == '2'):
                udp_socket.close()
                break
            elif(option == '3'):
                #if recv_thread.isAlive == True:
                stop_thread(recv_thread)
                waitOrder(udp_socket)
    except:
        udp_socket.close()

if __name__ == "__main__":
    main()
