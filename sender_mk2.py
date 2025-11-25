import socket
import struct
import time

from inputs import get_gamepad

SEND_INTERVAL = 0 # 0.02  # 50 Hz
last_send = time.time()
MANUAL_MAX_STRAFE = True
STRAFE_MAX = 24000 # max is 32768

# Target PC IP and UDP port
TARGET_IP = "192.168.1.67"  # replace with your receiver PC
TARGET_PORT = 9999

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# struct format: <hhhhBBH
# lx, ly, rx, ry = sticks (signed 16-bit)
# lt, rt = triggers (unsigned byte)
# buttons = 16-bit unsigned mask
PACK_FMT = "<hhhhBBH"

# Button bitmask mapping
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

# D-Pad bits: map hat to buttons
DPAD_BITS = {
    "ABS_HAT0X": (0x0004, 0x0008),  # Left, Right
    "ABS_HAT0Y": (0x0001, 0x0002),  # Up, Down
}

# Initialize values
buttons = 0
lx = ly = rx = ry = 0
lt = rt = 0

def normalize_stick(value):
    if -32768 <= value <= 32767:
        return value
    # Scale 0..65535 to -32768..32767
    return int((value - 32768) / 32768 * 32767)

def normalize_trigger(value):
    if value > 255:
        return int(value / 65535 * 255)
    return value

def max_left_stick(value):
    sign = 1
    if value < 0:
        sign = -1
    if abs(value) > STRAFE_MAX:
        return STRAFE_MAX * sign
    else:
        return value

print("Sending ReWASD controller state over UDP...")

while True:
    now = time.time()
    if now - last_send >= SEND_INTERVAL:
        for ev in get_gamepad():
            if ev.ev_type == "Key":
                bit = BUTTON_MAP.get(ev.code)
                if bit:
                    if ev.state:
                        buttons |= bit
                    else:
                        buttons &= ~bit

            elif ev.ev_type == "Absolute":
                # Sticks
                if ev.code == "ABS_X": lx = normalize_stick(ev.state)
                elif ev.code == "ABS_Y": ly = -normalize_stick(ev.state)  # invert Y
                elif ev.code == "ABS_RX": rx = normalize_stick(ev.state)
                elif ev.code == "ABS_RY": ry = -normalize_stick(ev.state)
                # Triggers
                elif ev.code == "ABS_Z": lt = normalize_trigger(ev.state)
                elif ev.code == "ABS_RZ": rt = normalize_trigger(ev.state)
                # D-Pad
                elif ev.code in DPAD_BITS:
                    neg_bit, pos_bit = DPAD_BITS[ev.code]
                    if ev.state == 0:
                        buttons &= ~neg_bit
                        buttons &= ~pos_bit
                    elif ev.state < 0:
                        buttons |= neg_bit
                        buttons &= ~pos_bit
                    else:
                        buttons |= pos_bit
                        buttons &= ~neg_bit

            # Clamp stick values to signed 16-bit
            lx = max(-32768, min(32767, int(lx)))
            ly = max(-32768, min(32767, int(ly)))
            rx = max(-32768, min(32767, int(rx)))
            ry = max(-32768, min(32767, int(ry)))

            # Fix strafe on left stick
            if MANUAL_MAX_STRAFE:
                lx = max_left_stick(lx)

            # Pack and send
            # print(lx, ly, rx, ry)
            msg = struct.pack(PACK_FMT, lx, ly, rx, ry, lt, rt, buttons)
            print(lx, ly, rx, ry)
            print("Sending bytes:", list(msg), "Length:", len(msg))
            sock.sendto(msg, (TARGET_IP, TARGET_PORT))
            last_send = now
