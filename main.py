#!/usr/bin/env python
# -*- coding: utf-8 -*-
import string
import pythoncom
import pyHook
import thread

import serial
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.font_manager as font_manager
import scipy.signal as signal

from wx import wx

# wxWidgets object ID for the timer
TIMER_ID = wx.NewId()
# number of data points
POINTS = 400

class PlotFigure(wx.Frame):
    global chars, index, rssi, flag
    """Matplotlib wxFrame with animation effect"""
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title="BLE RSSI Monitor", size=(1220, 838))    #size=816, 524(816, 638)(1220, 838)
        # Matplotlib Figure
        self.fig = Figure((12, 8), 100)
        # bind the Figure to the backend specific canvas
        self.canvas = FigureCanvas(self, wx.ID_ANY, self.fig)
        # add a subplot
        self.ax = self.fig.add_subplot(111)
        # limit the X and Y axes dimensions
        self.ax.set_ylim([-100, -36])
        self.ax.set_xlim([0, POINTS+5])

        self.ax.set_autoscale_on(False)
        self.ax.set_xticks(range(0, POINTS+5,25))
        # we want a tick every 10 point on Y (101 is to have 10
        self.ax.set_yticks(range(-100, -36, 2))
        # disable autoscale, since we don't want the Axes to ad
        # draw a grid (it will be only for Y)
        self.ax.grid(True)
        # generates first "empty" plots
        self.user = [0] * POINTS
        self.mean = [0] * POINTS
        self.x5 = [0] * POINTS
        self.paintflag = 15
        self.x4 = 0
        self.x8 = 0

        self.l_user, = self.ax.plot(range(POINTS),self.user,label='original  RSSI dbm')
        self.l_native, = self.ax.plot(range(POINTS), self.mean, label='max+mid  RSSI dbm')
        # self.l_native, = self.ax.plot(range(POINTS),self.mean,label='mean+mid  RSSI dbm')
        self.l_junzhi, = self.ax.plot(range(POINTS), self.x5, label='mean+mid RSSI dbm')
        # add the legend
        self.ax.legend(loc='upper center',
                           ncol=4,
                           prop=font_manager.FontProperties(size=10))
        # force a draw on the canvas()
        # trick to show the grid and the legend
        self.canvas.draw()
        # save the clean background - everything but the line
        # is drawn and saved in the pixel buffer background
        self.bg = self.canvas.copy_from_bbox(self.ax.bbox)
        # bind events coming from timer with id = TIMER_ID
        # to the onTimer callback function
        wx.EVT_TIMER(self, TIMER_ID, self.onTimer)

    def onTimer(self, evt):
        """callback function for timer events"""
        # restore the clean background, saved at the beginning
        self.canvas.restore_region(self.bg)
                # update the data
        #temp =np.random.randint(10,80)
        newdata = ser.readline()
        newdatavalue = newdata[:-1]
        if(newdatavalue[1] == '-'):
            newdatavalue = newdatavalue[1:]
        print newdatavalue
        if (newdatavalue[1] == '1'):
            newdatavalue = self.x8
        newrssi = int(newdatavalue)
        # print newrssi
        if newrssi<-20:
            temp = newrssi
        else:
            temp = self.user[-1]
        self.user = self.user[1:] + [temp]

        # if(self.paintflag == 0):
        #     self.paintflag = 15
            # x6 = signal.medfilt(self.user, 11)
        x7 = sorted(self.user[POINTS-25:])
        self.x8 =0
        for xx in range(5,20,1):
            self.x8 = self.x8 + x7[xx]
        self.x8 = self.x8/(20-5)
        self.x5 = self.x5[1:] + [self.x8]

        x3 = sorted(self.user[POINTS-25:])
        self.x4 = x3[20]#int((x3[3] + x3[4] + x3[5] + x3[6])/4)
        self.mean = self.mean[1:] + [self.x4]
        # else:
        # self.x5 = self.x5[1:] + [self.x8]
        # self.mean = self.mean[1:] + [self.x4]
            # self.paintflag -=1

        # update the plot
        self.l_user.set_ydata(self.user)
        self.l_native.set_ydata(signal.medfilt(self.mean, 11))
        self.l_junzhi.set_ydata(signal.medfilt(self.x5,11))


        # just draw the "animated" objects
        self.ax.draw_artist(self.l_user) # It is used to efficiently update Axes data (axis ticks, labels, etc are not updated)
        self.ax.draw_artist(self.l_native)
        self.ax.draw_artist(self.l_junzhi)

        self.canvas.blit(self.ax.bbox)

def onMouseEvent(event):
    "处理鼠标事件"
    # fobj.writelines('-' * 20 + 'MouseEvent Begin' + '-' * 20 + '\n')
    # fobj.writelines("Current Time:%s\n" % time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    # fobj.writelines("MessageName:%s\n" % str(event.MessageName))
    # fobj.writelines("Message:%d\n" % event.Message)
    # fobj.writelines("Time_sec:%d\n" % event.Time)
    # fobj.writelines("Window:%s\n" % str(event.Window))
    # fobj.writelines("WindowName:%s\n" % str(event.WindowName))
    # fobj.writelines("Position:%s\n" % str(event.Position))
    # fobj.writelines('-' * 20 + 'MouseEvent End' + '-' * 20 + '\n')
    return True


def onKeyboardEvent(event):
    global chars, index, rssi
    "处理键盘事件"
    # fobj.writelines('-' * 20 + 'Keyboard Begin' + '-' * 20 + '\n')
    # fobj.writelines("Current Time:%s\n" % time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    # fobj.writelines("MessageName:%s\n" % str(event.MessageName))
    # fobj.writelines("Message:%d\n" % event.Message)
    # fobj.writelines("Time:%d\n" % event.Time)
    # fobj.writelines("Window:%s\n" % str(event.Window))
    # fobj.writelines("WindowName:%s\n" % str(event.WindowName))
    if event.Ascii>44 and event.Ascii<0x40:
        # fobj.writelines("Ascii_code: %d\n" % event.Ascii)
        # fobj.writelines("Ascii_char:%s\n" % chr(event.Ascii))
        if chr(event.Ascii) == "-":
            fobj.writelines("\n%s" % chr(event.Ascii))
            rssistring = chars[0] + chars[1] + chars[2]
            # print rssistring
            # rssi = string.atoi(rssistring, [10])
            rssi = int(rssistring)
            print rssi
            chars[0]= "-"
            index[0]=1
            # PlotFigure.onTimer()
        else:
            fobj.writelines("%s" % chr(event.Ascii))
            if index[0] == 1:
                chars[1] = chr(event.Ascii)
                index[0]=2
            elif index[0] == 2:
                chars[2] = chr(event.Ascii)
                index[0]=3
            elif index[0] == 3:
                chars[3] = chr(event.Ascii)
                index[0]=4
        # print chr(event.Ascii)
        # fobj.writelines("Key:%s\n" % str(event.Key))
    # fobj.writelines('-' * 20 + 'Keyboard End' + '-' * 20 + '\n')
    return True

# def data(no, interval):
#     # 创建hook句柄
#     hm = pyHook.HookManager()
#
#     # 监控键盘
#     hm.KeyDown = onKeyboardEvent
#     hm.HookKeyboard()
#     #循环获取消息
#     pythoncom.PumpMessages()

def paint(no, interval):
    app = wx.App()
    frame = PlotFigure()
    t = wx.Timer(frame, TIMER_ID)
    t.Start(60)
    frame.Show()
    app.MainLoop()

def test():
    # thread.start_new_thread(data, (1, 1))
    thread.start_new_thread(paint, (2, 2))

if __name__ == "__main__":
    global chars, index, rssi, flag
    ser = serial.Serial(port='COM18', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1000)
    print "serial.isOpen() =", ser.isOpen()
    '''''
    Function:操作SQLITE3数据库函数
    Input：NONE
    Output: NONE
    author: socrates
    blog:http://blog.csdn.net/dyx1024
    date:2012-03-1
    '''

    #打开日志文件
    # top = Tkinter.Tk()
    # def helloCallBack():
    #     tkMessageBox.showinfo("Hello Python", "Hello World")
    # B = Tkinter.Button(top, text="Hello,Python!", command=helloCallBack)
    # B.pack()
    # top.mainloop()
    #监控鼠标
    # hm.MouseAll = onMouseEvent
    # hm.HookMouse()
    index = [0]
    chars = ["-", "0", "0","0"]
    file_name = "D:\\hook_log.txt"
    fobj = open(file_name, 'w')
    rssi = -000
    # test()
    app = wx.App()
    frame = PlotFigure()
    t = wx.Timer(frame, TIMER_ID)
    t.Start(20)
    frame.Show()

    app.MainLoop()


    # # 创建hook句柄
    # hm = pyHook.HookManager()
    #
    # # 监控键盘
    # hm.KeyDown = onKeyboardEvent
    # hm.HookKeyboard()
    # #循环获取消息
    # pythoncom.PumpMessages()


def __del__( self ):
    #关闭日志文件
    ser.close()
    fobj.close()
