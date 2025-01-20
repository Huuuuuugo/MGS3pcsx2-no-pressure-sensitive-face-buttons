## FEATURES
# hold TRIANGLE to stick to the wall without needing to hold the analog stick
# quick press R2 to hide weappon

import time

from pynput.keyboard import Controller, Key, KeyCode
import pygame

# constants
CROSS = 0
CIRCLE = 1
SQUARE = 2
TRIANGLE = 3

START = 7
SELECT = 6

L_DEADZONE = 0.1
LY = 1
LX = 0

L1 = 4
R1 = 5

L2 = 4
R2 = 5

L3 = 8
R3 = 9


# Define numpad key mapping
numpad = {
    0: KeyCode.from_vk(96),
    1: KeyCode.from_vk(97),
    2: KeyCode.from_vk(98),
    3: KeyCode.from_vk(99),
    4: KeyCode.from_vk(100),
    5: KeyCode.from_vk(101),
    6: KeyCode.from_vk(102),
    7: KeyCode.from_vk(103),
    8: KeyCode.from_vk(104),
    9: KeyCode.from_vk(105)
}

# joystick and keyboard setup
keyboard = Controller()

pygame.init()
pygame.joystick.init()

# TODO FIXME: only works if the controller is on before starting
while not pygame.joystick.get_count():
    pygame.event.get()
    time.sleep(0.2)

else:
    gamepad = pygame.joystick.Joystick(0)
    print("connected")

# "hide weappon with R2" variables
hide_weappon = True
hide_timer = 0

# "stick to wall" variables
LY_value = 0
LX_value = 0

dpad_controller = {
    'u': 'w',
    'd': 's',
    'l': 'a',
    'r': 'd'
}


# main logic
while True:
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            # hide weappon with R2
            # activate trigger for hiding weappon
            if event.axis == R2:
                if (not hide_weappon 
                    and event.value <= -1
                    ):
                    hide_weappon = True
                
                # send input when appropriate 
                if (hide_weappon 
                    and event.value > -1
                    ):
                    hide_timer = time.perf_counter()
                    hide_weappon = False
                    pressed = False
                    # while on the time window 
                    while (time.perf_counter() - hide_timer) <= 0.20 and not pressed:
                        for event in pygame.event.get():
                            if event.type == pygame.JOYAXISMOTION:
                                # break and send input if the trigger is unpressed within the time window
                                if (event.axis == R2 
                                    and event.value <= -1
                                    ):
                                    keyboard.press(numpad[1])
                                    time.sleep(1/20)
                                    keyboard.release(numpad[1])
                                    pressed = True
                                    hide_weappon = True
                                    break                
                        
                        time.sleep(0.005)
                
            # save left analog stick values to use when
            # sticking to the wall
            if event.axis == LY:
                LY_value = event.value
            elif event.axis == LX:
                LX_value = event.value
        
        # alternate dpad bindings to stick to the wall
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == TRIANGLE:
                abs_LY_value = abs(LY_value)
                abs_LX_value = abs(LX_value)
                if (abs_LY_value + abs_LX_value) >= 2*L_DEADZONE:
                    # if movement is on the Y axis
                    if abs_LY_value > abs_LX_value:
                        # if left analog is up
                        if LY_value > 0:
                            keyboard.press('s')
                            dpad_controller = {
                                'u': 'q',
                                'd': 'q',
                                'l': 'd',
                                'r': 'a'
                            }
                        
                        # if left analog is down
                        if LY_value < 0:
                            keyboard.press('w')
                            dpad_controller = {
                                'u': 'q',
                                'd': 'q',
                                'l': 'a',
                                'r': 'd'
                            }

                    # if movement is on the X axis
                    else:
                        # if left analog is left
                        if LX_value > 0:
                            keyboard.press('d')
                            dpad_controller = {
                                'u': 'q',
                                'd': 'q',
                                'l': 'w',
                                'r': 's'
                            }
                
                        # if left analog is right
                        if LX_value < 0:
                            keyboard.press('a')
                            dpad_controller = {
                                'u': 'q',
                                'd': 'q',
                                'l': 's',
                                'r': 'w'
                            }
                
        # reset depad controller
        if event.type == pygame.JOYBUTTONUP:
            if event.button == TRIANGLE:
                keyboard.release('w')
                keyboard.release('s')
                keyboard.release('a')
                keyboard.release('d')
                dpad_controller = {
                    'u': 'w',
                    'd': 's',
                    'l': 'a',
                    'r': 'd'
                }
        
        # send dpad input
        if event.type == pygame.JOYHATMOTION:
            match event.value[0]:
                case 0:
                    keyboard.release(dpad_controller['l'])
                    keyboard.release(dpad_controller['r'])
                
                case 1:
                    keyboard.press(dpad_controller['r'])
                
                case -1:
                    keyboard.press(dpad_controller['l'])

            match event.value[1]:
                case 0:
                    keyboard.release(dpad_controller['u'])
                    keyboard.release(dpad_controller['d'])
                
                case 1:
                    keyboard.press(dpad_controller['u'])

                case -1:
                    keyboard.press(dpad_controller['d'])
            
        time.sleep(0.01)
    time.sleep(0.01)



