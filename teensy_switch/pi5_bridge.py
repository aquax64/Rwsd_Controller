# Code modified from the receiver
import serial
import socket
import struct
import time


# Ethernet
LISTEN_PORT = 9999
PACK_FMT = "<hhhhBBH" #"<HBBhhhh"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LISTEN_PORT))

print("Listening for controller input on UDP", LISTEN_PORT)

DEADZONE = 5000
prev_lx, prev_ly, prev_rx, prev_ry = 0, 0, 0, 0

def clamp(val, _min, _max):
    return max(_min, min(val, _max))

def signed16_to_minus1_1(val):
    return max(-1.0, min(1.0, val/32767 if val >= 0 else val / 32768))


# UART
ser = serial.Serial(
    port='/dev/serial0',
    baudrate=115200,
    timeout=0
)
time.sleep(2) # allow time for teensy?

while True:
    data, addr = sock.recvfrom(1024)

    if len(data) != struct.calcsize(PACK_FMT):
        continue

    ser.write(data)

    print("Forwarded packet:", list(data))

    #(
    #    lx, ly,
    #    rx, ry,
    #    lt, rt,
    #    buttons
    #) = struct.unpack(PACK_FMT, data)

    #print("Recieved bytes:", list(data), "Length:", len(data))
    #print(
    #    f"\rLX: {str(lx)}  LY: {str(ly)}  RX: {str(rx)}  RY: {str(ry)}  LT: {str(lt)}  RT: {str(rt)}  Buttons: {str(buttons)} )",
    #    end="")
