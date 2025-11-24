import socket
import struct
import vgamepad as vg

LISTEN_PORT = 9999
PACK_FMT = "<HBBhhhh"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LISTEN_PORT))

print("Listening for controller input on UDP", LISTEN_PORT)

gamepad = vg.VX360Gamepad()  # virtual Xbox 360 controller

while True:
    data, addr = sock.recvfrom(1024)

    if len(data) != struct.calcsize(PACK_FMT):
        continue

    (
        buttons,
        lt, rt,
        lx, ly,
        rx, ry
    ) = struct.unpack(PACK_FMT, data)

    # Buttons
    gamepad.press_button(buttons=buttons)
    gamepad.left_trigger(value=lt)
    gamepad.right_trigger(value=rt)

    gamepad.left_joystick(x_value=lx, y_value=ly)
    gamepad.right_joystick(x_value=rx, y_value=ry)

    gamepad.update()
