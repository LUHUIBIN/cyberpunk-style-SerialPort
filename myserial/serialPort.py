import serial
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from UI import *
from PyQt5.QtCore import QTimer
import re
import serial.tools.list_ports

flag = 0 #串口标志位
baudRate = 0 #波特率
com = '' #串口
port_list = []

def to_hex(data_s):
    if data_s is not None:
        bt = bytes(data_s,"gbk").hex().upper()
        r = re.findall(".{2}",bt)
        data_s_hex = " ".join(r)
        return data_s_hex

class myWindow(QMainWindow,Ui_Form):
    def __init__(self,parent=None):
        global data_s
        #init Ui_Form
        super(myWindow, self).__init__(parent)
        self.setupUi(self)
        #获取串口信息
        self.get_list_ports()
        for i in range(0,len(port_list)):
            self.comboBox_2.addItem(str(port_list[i]).replace(" ",""))
        #链接槽函数
        self.pushButton_2.clicked.connect(self.slot_port)
        self.pushButton.clicked.connect(self.send_data)
        self.pushButton_4.clicked.connect(self.slot_clear_textEdit)
        self.pushButton_5.clicked.connect(self.slot_clear_textEdit2)
        self.pushButton_3.clicked.connect(self.send_hex_data)

        self.comboBox_2.currentIndexChanged.connect(self.slot_com_baudRateChanged)
        self.comboBox.currentIndexChanged.connect(self.slot_com_baudRateChanged)

        self.setWindowTitle("cyberpunk版串口助手 V0.1")
        self.setWindowIcon(QIcon('./images/favicon.ico'))
        #配置定时器与接收函数连接
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.read_data)
        self.timer.start(100)  # 设置计时间隔并启动
        #配置GIF图
        self.movie = QMovie("./images/Cyberpunk-2077-Neon-Logo.gif")
        self.label_3.setMovie(self.movie)
        self.movie.start()

    def get_list_ports(self):
        global port_list
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) == 0:
            QMessageBox.critical(self, 'Info', '未发现可用串口')

    def get_com_baudRate(self):
        global baudRate,com
        baudRate = self.comboBox.currentText()
        com = self.comboBox_2.currentText()[0:4]

    def slot_port(self):
        global ser,flag
        if flag == 0:
            try:
                self.get_com_baudRate()
                ser = serial.Serial(com, baudRate,timeout= 2)
                self.pushButton_2.setText("关闭串口")
                self.pushButton_2.setStyleSheet("background-color: rgb(	255, 99, 71);"
                                              "color: rgb(0,0,0);")
                flag = 1
            except:
                QMessageBox.critical(self, 'Info', '串口打开失败')
        elif flag == 1:
            try:
                ser.close()
                self.pushButton_2.setText("打开串口")
                self.pushButton_2.setStyleSheet("background-color: rgb(	255, 255, 255);"
                                               "color: rgb(0,0,0);")
                flag = 0
            except:
                QMessageBox.critical(self, 'Info', '串口关闭失败')

    def get_data_s(self):
        return self.textEdit.toPlainText()

    def send(self,data_s):
        if not self.checkBox_2.isChecked():
            try:
                if ser.isOpen():
                    for item in data_s:
                        ser.write(bytes(item, 'gbk'))  # 串口写数据
                    ser.write(b' ')
                    print("数据发送成功")
            except:
                QMessageBox.critical(self, 'Info', '串口未打开')
        elif self.checkBox_2.isChecked():
            try:
                if ser.isOpen():
                    for item in data_s:
                        ser.write(bytes(item, 'gbk'))  # 串口写数据
                    ser.write(b'\r\n')
                    print("数据发送成功")
            except:
                QMessageBox.critical(self, 'Info', '串口未打开')

    def send_data(self):
        data_s = self.get_data_s()
        self.send(data_s)

    def send_hex_data(self):
        data_s = self.textEdit.toPlainText()
        data_s_hex = to_hex(data_s)
        self.send(data_s_hex)

    def read_data(self):
        global data_r
        if flag:
            if ser.in_waiting:
                data_r = ser.read(ser.in_waiting).decode("gbk")
                if data_r != None:
                    self.textEdit_2.insertPlainText(data_r)

    def slot_clear_textEdit(self):
        self.textEdit.clear()

    def slot_clear_textEdit2(self):
        self.textEdit_2.clear()

    def slot_com_baudRateChanged(self):
        try:
            if flag == 1:
                self.slot_port()
        except:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = myWindow()
    #配置图标
    myWin.setObjectName("MainWindow")
    myWin.setStyleSheet("#MainWindow{border-image:url(./images/cyberpunk-2077.jpg);}")
    myWin.setWindowOpacity(0.95)
    myWin.show()
    sys.exit(app.exec_())
