## FEATURES
# full support for controllers without analog buttons
#
# grabbing:
# - hold CIRCLE to grab the enemy
# - hold CIRCLE and TRIANGLE to kill the grabbed enemy
# - press L3 to interrogate (instead of holding)
#
# use gun while grabbing:
# - hold SQUARE to aim while holding an enemy
# - press R2 while aiming to put down weapon
#   - after putting down the weapon keep holding SQUARE or CIRCLE to keep the enemy on the grabbed state
#
# aiming:
# - press L1 to auto aim
#   - while aiming with L1, press CIRCLE to alternate between free aim and auto aim
 
import time

from pynput.keyboard import Controller, Key, KeyCode
import pygame

# constants
CROSS = 0
CIRCLE = 1
SQUARE = 2
TRIANGLE = 3

L_DEADZONE = 0.1
LY = 1
LX = 0

L1 = 4
R1 = 5

L2 = 4
R2 = 5

START = 7
SELECT = 6

R3 = 9
L3 = 8

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

# main logic
while True:
    for event in pygame.event.get():
        # press buttons
        if event.type == pygame.JOYBUTTONDOWN:
            print(event.button)
            # square to numpad 3
            if event.button == SQUARE:
                print("normal press")
                keyboard.press(numpad[3])

            # L3 to numpad 2
            elif event.button == L3:
                keyboard.press(numpad[2])
            
            # proper aim with L1
            elif event.button == L1:
                aim_switch = 1 # used to properly alternate the auto aim state
                keyboard.press(numpad[1]) # activate light press
                keyboard.press(numpad[4]) # activate L1

                if not gamepad.get_button(SQUARE): # lightly press fire to aim
                    keyboard.press(numpad[3])

                # aim loop
                while gamepad.get_button(L1):
                    # toggle aim with circle
                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            # toggle aim
                            if event.button == CIRCLE:
                                if aim_switch:
                                    keyboard.release(numpad[4])
                                    aim_switch = 0
                                
                                else:
                                    keyboard.press(numpad[4])
                                    aim_switch = 1

                            # firing sequence
                            if event.button == SQUARE:
                                keyboard.release(numpad[1]) # deactivate light press to start firing

                                while gamepad.get_button(SQUARE) and gamepad.get_button(L1): # wait for square or L1 to be released
                                    for event in pygame.event.get():
                                        if event.type == pygame.JOYBUTTONUP:
                                            if event.button == SQUARE:
                                                keyboard.press(numpad[1]) # reactivate light press
                                                keyboard.release(numpad[3]) # stop firing
                                                time.sleep(1/20)
                                                keyboard.press(numpad[3]) # press fire again to keep auto aim
                                        time.sleep(1/60)
                    
                    time.sleep(1/60)
                
                else:
                    if not gamepad.get_button(SQUARE):
                        keyboard.press(numpad[5])
                        time.sleep(1/40)
                        keyboard.release(numpad[3]) # stop firing
                        time.sleep(1/40)
                        keyboard.release(numpad[5])

                    keyboard.release(numpad[4]) # activate L1
                    keyboard.release(numpad[1]) # activate light press
        
            # no pressure grabbing
            elif event.button == CIRCLE:
                exit_grab_timer = 0
                L3_toggle = 0
                keyboard.press(numpad[6])
                keyboard.press(numpad[1]) # activate light press
                detect_hold_circle = time.perf_counter() # used to detect if the circle button was pressed or holded

                while (
                    gamepad.get_button(CIRCLE) 
                    or gamepad.get_button(SQUARE) 
                    or (time.perf_counter() - exit_grab_timer) <= 0.5):
                    for event in pygame.event.get():
                        if event.type == pygame.JOYBUTTONDOWN:
                            # alternate interrogation action
                            if event.button == L3:
                                if L3_toggle:
                                    keyboard.release(numpad[2])
                                    L3_toggle = 0

                                else:
                                    keyboard.press(numpad[2])
                                    L3_toggle = 1
                            
                            # cut throat
                            elif event.button == TRIANGLE:
                                keyboard.release(numpad[1])
                                time.sleep(1/20)
                                break

                            elif event.button == CIRCLE:
                                keyboard.press(numpad[6])
                                keyboard.press(numpad[1]) # activate light press
                            
                            # use gun while holding enemy
                            elif event.button == SQUARE:
                                keyboard.press(numpad[3])
                                keyboard.release(numpad[6])
                                pull_down_toggle = 1
                                while gamepad.get_button(SQUARE):
                                    for event in pygame.event.get():
                                        if event.type == pygame.JOYAXISMOTION:
                                            # put down gun without firing
                                            if event.axis == R2:
                                                if event.value >= -1 and pull_down_toggle:
                                                    pull_down_toggle = 0
                                                    print("pulling down")
                                                    keyboard.press(numpad[7])
                                                    time.sleep(1/20)
                                                    keyboard.press(numpad[8])
                                                    time.sleep(1/20)
                                                    keyboard.release(numpad[3])
                                                    keyboard.release(numpad[7])
                                                    keyboard.release(numpad[8])
                                                    keyboard.press(numpad[6])
                                                    break
                                        
                                        # fire
                                        if event.type == pygame.JOYBUTTONUP:
                                            if event.button == SQUARE:
                                                exit_grab_timer = time.perf_counter() # used to keep the grabbing state even when no buttons aren't being pressed
                                                keyboard.release(numpad[3])
                                                break
                        
                        # add delay before exiting the grabbing loop
                        if event.type == pygame.JOYBUTTONUP:
                            if event.button == CIRCLE:
                                if (time.perf_counter() - detect_hold_circle) >= 0.5:
                                    exit_grab_timer = time.perf_counter()
                                    keyboard.release(numpad[6])
                
                keyboard.release(numpad[6])
                keyboard.release(numpad[3])
                keyboard.release(numpad[2])
                keyboard.release(numpad[1])
                    
        # release buttons
        if event.type == pygame.JOYBUTTONUP:
            print(event.button)
            # square ro numpad 3
            if event.button == SQUARE:
                keyboard.release(numpad[3])
            
            # L3 to numpad 2
            if event.button == L3:
                keyboard.release(numpad[2])

            # CIRCLE to numpad 6
            if event.button == L3:
                keyboard.release(numpad[6])
    
    time.sleep(0.01)