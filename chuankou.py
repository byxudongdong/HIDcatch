#!/usr/bin/env python
# it's a program of luo, piedgogo@sina.com

import serial
import array
import os
import signal
from time import sleep

flag_stop = False


def onsignal_int(a, b):
    print "sigint!"
    global flag_stop
    flag_stop = True


signal.signal(signal.SIGINT, onsignal_int)
signal.signal(signal.SIGTERM, onsignal_int)

ser = serial.Serial(port='COM2', baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=None, xonxoff=0, rtscts=0)

print "serial.isOpen() =", ser.isOpen()

cmd_send = "7b02000129cc00c80378290400640000cc7d0d0a"
cmd_send = cmd_send.decode("hex")

stop = "7b04047d0d0a"
stop = stop.decode("hex")

cmd_back = ""
cmd_length = 0x00
cmd_count = 0x00

s = ser.write(cmd_send)

while True:
    sleep(0.1)

    if flag_stop:  # read data until Ctrl+c
        ser.write(stop)  # send cmd stop before exit
        print "reset cmd has been sent!"
        sleep(0.05)
        break

    text = ser.read(1)  # read one, with timout
    if text:  # check if not timeout
        n = ser.inWaiting()  # look if there is more to read
        if n:
            text = text + ser.read(n)  # get it
        cmd_back = cmd_back + text
        text = ""

    if len(cmd_back) < 2:  # go back if no enough data recvd
        continue

    if cmd_length == 0x00:  # new loop
        cmd_length = ord(cmd_back[1])  # Type(1 byte),Length of Value(1 byte),Value
        print "new cmd length,", cmd_length

    if (cmd_length + 0x02) > len(cmd_back):  # do nothing until all bytes is recvd
        continue

    # so far, we have got a full cmd

    hex_list = [hex(ord(i)) for i in cmd_back]  # more readable than data.encode("hex")
    print "In buffer:", hex_list

    cmd_back = cmd_back[cmd_length + 2:]  # remove this cmd(TLV) from buffer
    cmd_length = 0
    cmd_count += 1

    print "==> %d cmds recvd." % (cmd_count)
    print "-------------"

ser.close()
