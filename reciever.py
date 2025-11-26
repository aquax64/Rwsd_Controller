import socket
import struct
import time
import vgamepad as vg
from vgamepad import DS4_BUTTONS as ds
from vgamepad import DS4_SPECIAL_BUTTONS as dsSPEC
from vgamepad import DS4_DPAD_DIRECTIONS as dir

LISTEN_PORT = 9999
PACK_FMT = "<hhhhBBH" #"<HBBhhhh"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", LISTEN_PORT))

print("Listening for controller input on UDP", LISTEN_PORT)

# gamepad = vg.VX360Gamepad()  # virtual Xbox 360 controller
gamepad = vg.VDS4Gamepad()  # virtual Dualshock controller

DEADZONE = 5000
prev_lx, prev_ly, prev_rx, prev_ry = 0, 0, 0, 0

def clamp(val, _min, _max):
    return max(_min, min(val, _max))

def signed16_to_minus1_1(val):
    return max(-1.0, min(1.0, val/32767 if val >= 0 else val / 32768))



while True:
    data, addr = sock.recvfrom(1024)

    if len(data) != struct.calcsize(PACK_FMT):
        continue

    #(
    #    buttons,
    #    lt, rt,
    #    lx, ly,
    #    rx, ry
    #) = struct.unpack(PACK_FMT, data)
    (
        lx, ly,
        rx, ry,
        lt, rt,
        buttons
    ) = struct.unpack(PACK_FMT, data)

    #print("Recieved bytes:", list(data), "Length:", len(data))
    print(
        f"\rLX: {str(lx)}  LY: {str(ly)}  RX: {str(rx)}  RY: {str(ry)}  LT: {str(lt)}  RT: {str(rt)}  Buttons: {str(buttons)} )",
        end="")

    #lx = int(round(clamp(lx, -32768, 32767)/8)*8)
    #ly = int(round(clamp(ly, -32768, 32767)/8)*8)
    #rx = int(round(clamp(rx, -32768, 32767)/8)*8)
    #ry = int(round(clamp(ry, -32768, 32767)/8)*8)
    lx = signed16_to_minus1_1(lx)
    ly = signed16_to_minus1_1(ly)
    rx = signed16_to_minus1_1(rx)
    ry = signed16_to_minus1_1(ry)

    # Buttons
    # gamepad.press_button(button=buttons)
    gamepad.left_trigger(value=lt)
    gamepad.right_trigger(value=rt)

    if (lx, ly) != (prev_lx, prev_ly):
        # gamepad.left_joystick(x_value=lx, y_value=ly)
        gamepad.left_joystick_float(x_value_float=lx, y_value_float=ly)
    if (rx, ry) != (prev_rx, prev_ry):
        gamepad.right_joystick_float(x_value_float=rx, y_value_float=ry)

    gamepad.press_button(ds.DS4_BUTTON_CROSS) if buttons & 4096 else gamepad.release_button(ds.DS4_BUTTON_CROSS)
    gamepad.press_button(ds.DS4_BUTTON_CIRCLE) if buttons & 8192 else gamepad.release_button(ds.DS4_BUTTON_CIRCLE)
    gamepad.press_button(ds.DS4_BUTTON_SQUARE) if buttons & 32768 else gamepad.release_button(ds.DS4_BUTTON_SQUARE)
    gamepad.press_button(ds.DS4_BUTTON_TRIANGLE) if buttons & 16384 else gamepad.release_button(ds.DS4_BUTTON_TRIANGLE)
    gamepad.press_button(ds.DS4_BUTTON_OPTIONS) if buttons & 16 else gamepad.release_button(ds.DS4_BUTTON_OPTIONS)
    gamepad.press_button(ds.DS4_BUTTON_SHOULDER_LEFT) if buttons & 256 else gamepad.release_button(ds.DS4_BUTTON_SHOULDER_LEFT)
    gamepad.press_button(ds.DS4_BUTTON_SHOULDER_RIGHT) if buttons & 512 else gamepad.release_button(ds.DS4_BUTTON_SHOULDER_RIGHT)
    gamepad.press_button(ds.DS4_BUTTON_THUMB_LEFT) if buttons & 64 else gamepad.release_button(ds.DS4_BUTTON_THUMB_LEFT)
    gamepad.press_button(ds.DS4_BUTTON_THUMB_RIGHT) if buttons & 128 else gamepad.release_button(ds.DS4_BUTTON_THUMB_RIGHT)
    gamepad.press_special_button(dsSPEC.DS4_SPECIAL_BUTTON_TOUCHPAD) if buttons & 32 else gamepad.release_button(dsSPEC.DS4_SPECIAL_BUTTON_TOUCHPAD)

    noneButtonSelected = True
    cornerDPADEnabled = False

    # NORTHWEST
    if buttons & 5 and cornerDPADEnabled:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_NORTHWEST)
        noneButtonSelected = False
    # WEST
    if buttons & 4 and noneButtonSelected:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_WEST)
        noneButtonSelected = False
    # SOUTHWEST
    if buttons & 6 and noneButtonSelected and cornerDPADEnabled:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_SOUTHWEST)
        noneButtonSelected = False
    # SOUTH
    if buttons & 2 and noneButtonSelected:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_SOUTH)
        noneButtonSelected = False
    # SOUTHEAST
    if buttons & 10 and noneButtonSelected and cornerDPADEnabled:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_SOUTHEAST)
        noneButtonSelected = False
    # EAST
    if buttons & 8 and noneButtonSelected:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_EAST)
        noneButtonSelected = False
    # NORTHEAST
    if buttons & 9 and noneButtonSelected and cornerDPADEnabled:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_NORTHEAST)
        noneButtonSelected = False
    # NORTH
    if buttons & 1 and noneButtonSelected:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_NORTH)
        noneButtonSelected = False
    # None
    if noneButtonSelected:
        gamepad.directional_pad(direction=dir.DS4_BUTTON_DPAD_NONE)

    prev_lx = lx
    prev_ly = ly
    prev_rx = rx
    prev_ry = ry

    gamepad.update()
