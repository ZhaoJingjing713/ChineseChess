from os import truncate
import socket
import threading


class service:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.get_data=False
        self.loss_connection=False
        self.if_connect=0
        self.ip = socket.gethostbyname(self.hostname)
        self.port=[1713,1714,1715,1716,1717]
        print(self.ip)
        self.serverrsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        i=0
        for i in range(len(self.port)):
            try:
                self.serverrsocket.bind((self.ip,self.port[i]))
                break
            except OSError:
                print(self.port[i],'被占用')
                continue
        else:
            print("所有端口被占用")
        self.last_msg=''
        self.receive_name=''
        self.receive_current=[]
        self.receive_target=[]
    def connect(self):
        self.serverrsocket.listen(5)
        print('开始连接')
        try:
            self.c=self.serverrsocket.accept()  #线程阻塞
            print("建立一个连接")
            self.if_connect=1
        except TimeoutError:
            print("连接失败")
            self.if_connect=0
    def myrevc(self,c):
        while True:
            try:
                msg=self.c[0].recv(1024)#阻塞
            except ConnectionResetError or ConnectionAbortedError:
                print("关闭连接")
                self.if_connect=0
                self.loss_connection=True
                self.close()
                return
            print(msg.decode())
            rec_data=msg.decode()
            if(rec_data=='' and rec_data==self.last_msg):
                self.get_data=False
                continue
            self.last_msg=rec_data
            self.receive_name=rec_data[:-16]
            self.receive_current=[int(rec_data[-14]),int(rec_data[-11])]
            self.receive_target=[int(rec_data[-6]),int(rec_data[-3])]
            self.get_data=True
            break
    def receive(self):
        self.get_data=False
        threading._start_new_thread(self.myrevc,(self.c[0],))   #新线程接受信息
        #self.myrevc(self.c[0])
    def send(self,name,current,target):
        while True:
            msg=name+str([current,target])
            status=self.c[0].send(msg.encode())
            if(status>=0):
                break
    def close(self):
        self.c[0].close()

class client:
    def __init__(self,ip=''):
        self.c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.if_connect=0
        self.loss_connection=False
        self.get_data=False
        self.receive_name=''
        self.receive_current=[]
        self.receive_target=[]
        self.last_msg=''
        print("创建客户套接字")
        self.ip=ip
        self.port=[1713,1714,1715,1716,1717]
    def connect(self):
        i=0
        for i in range(len(self.port)):
            try:
                try:
                    self.c.connect((self.ip,self.port[i]))
                except OSError:
                    continue
                self.if_connect=1
                print("连接成功")
                break
            except socket.gaierror :
                print('连接失败')

    def myrevc(self,c):
        while True:
            try:
                msg=c.recv(1024)#阻塞
            except ConnectionResetError or ConnectionAbortedError:
                print("关闭连接")
                self.if_connect=0
                self.loss_connection=True
                self.close()
            print(msg.decode())
            rec_data=msg.decode()
            if(rec_data=='' or rec_data==self.last_msg):
                self.get_data=False
                continue
            self.last_msg=rec_data
            self.receive_name=rec_data[:-16]
            self.receive_current=[int(rec_data[-14]),int(rec_data[-11])]
            self.receive_target=[int(rec_data[-6]),int(rec_data[-3])]
            self.get_data=True
            break
    def receive(self):
        self.get_data=False
        #self.myrevc(self.c)
        threading._start_new_thread(self.myrevc,(self.c,))
    def send(self,name,current,target):
        while True:
            msg=name+str([current,target])
            status=self.c.send(msg.encode())
            if(status>=0):
                break
    def close(self):
        self.c.close()