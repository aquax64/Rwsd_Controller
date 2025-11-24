import socket
import struct
from inputs import get_gamepad

TARGET_IP = "192.168.1.50"   # <-- PC #2 IP
TARGET_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

PACK_FMT = "<HBBhhhh"   # matches XUSB_REPORT

buttons = 0
lt = rt = 0
lx = ly = rx = ry = 0

BUTTON_MAP = {
    "BTN_SOUTH":   0x1000,  # A
    "BTN_EAST":    0x2000,  # B
    "BTN_NORTH":   0x4000,  # Y
    "BTN_WEST":    0x8000,  # X
    "BTN_SELECT":  0x0010,  # Back
    "BTN_START":   0x0020,  # Start
    "BTN_TL":      0x0100,  # LB
    "BTN_TR":      0x0200,  # RB
    "BTN_THUMBL":  0x0040,  # LS press
    "BTN_THUMBR":  0x0080,  # RS press
}

DPAD_MAP = {
    "ABS_HAT0X": lambda v: ("left", v < 0, 0x0004, 0x0008),
    "ABS_HAT0Y": lambda v: ("up",   v < 0, 0x0001, 0x0002),
}

print("Sending ReWASD controller state...")

while True:
    for ev in get_gamepad():
        if ev.ev_type == "Key":
            bit = BUTTON_MAP.get(ev.code)
            if bit:
                if ev.state:
                    buttons |= bit
                else:
                    buttons &= ~bit

        elif ev.ev_type == "Absolute":
            if ev.code == "ABS_Z": lt = ev.state
            elif ev.code == "ABS_RZ": rt = ev.state
            elif ev.code == "ABS_X": lx = ev.state
            elif ev.code == "ABS_Y": ly = -ev.state
            elif ev.code == "ABS_RX": rx = ev.state
            elif ev.code == "ABS_RY": ry = -ev.state

            elif ev.code in DPAD_MAP:
                _, neg, pos_bit, neg_bit = DPAD_MAP[ev.code](ev.state)
                if ev.state == 0:
                    buttons &= ~pos_bit
                    buttons &= ~neg_bit
                elif neg:
                    buttons |= pos_bit
                    buttons &= ~neg_bit
                else:
                    buttons |= neg_bit
                    buttons &= ~pos_bit

        msg = struct.pack(PACK_FMT, buttons, lt, rt, lx, ly, rx, ry)
        sock.sendto(msg, (TARGET_IP, TARGET_PORT))
