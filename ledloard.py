__author__ = 'schinken'

import socket
import struct
import time
import sys

class Client:

    socket = None

    CMD_FRAME   = 0xA1
    CMD_PRIO    = 0xA2
    CMD_ACK     = 0xA5

    PRIO_NORMAL = 0xF0
    PRIO_HIGH   = 0xF1
    PRIO_GOD    = 0xF2

    def __init__(self, ip='127.0.0.1', port=1337):

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(1)

        try:
            self.socket.connect((ip,port))
        except socket.error, msg:
            sys.stderr.write("[ERROR] %s\n" % msg[1])
            sys.exit(2)

    def set_priority(self, priority):

        if not priority is self.PRIO_NORMAL or not priority is self.PRIO_HIGH or not priority is self.PRIO_GOD:
            return

        self.write_byte(self.CMD_PRIO)
        self.write_byte(priority)

    def wait_ack(self):

        recv = False
        while recv != self.CMD_ACK:
            recv = self.socket.recv(1)
            recv = struct.unpack(">B", recv)
            recv = int(recv[0])


    def write_byte(self, byte):
        self.socket.send(struct.pack(">B", byte))

    def write_frame(self, frame, width, height):

        self.wait_ack()
        self.write_byte(self.CMD_FRAME)

        for y in range(height):
            for x in range(width):
                self.write_byte(frame[x][y])


