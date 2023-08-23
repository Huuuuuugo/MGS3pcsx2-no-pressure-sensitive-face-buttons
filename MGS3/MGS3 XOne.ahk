#Include <XInput>
#Include <ButtonIsDown>
#SingleInstance force
#Persistent 
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

XInput_Init()
L3 := 0
holdingX := 0
holdingY := 0
holdingLB := 0
holdingB := 0
Btimer := 0
aimLock := 1
Loop
{
    Loop, 1
	{
        BT := XInput_GetState(A_Index-1).wButtons


                    /*
                    ; Start of Toggle R3
                    if (XInputButtonIsDown( "RStick", BT ))
                    {
                        if (R3 = 0)
                        {
                            SendInput {Numpad6 Down}
                            Sleep 500
                            R3 := 1
                        }
                        else
                        {
                            SendInput {Numpad6 Up}
                            Sleep 200
                            R3 := 0
                        }
                    }
                    ; End of Toggle R3
                    */ 

        ; Start of Square to Numpad3
        if (!XInputButtonIsDown( "X", BT ) && holdingX = 1)
        {
            SendInput {Numpad3 Up}
            holdingX := 0
        }
        
        if (XInputButtonIsDown( "X", BT ) && holdingX = 0)
        {
            SendInput {Numpad3 Down}
            holdingX := 1
        }
        ; End of Square to Numpad3


        ; Start of L3 to Numpad2
        if (XInputButtonIsDown( "LStick", BT ) && L3 = 0)
        {
            SendInput {Numpad2 Down}
            Sleep 500
            L3 := 1
        }
        if (!XInputButtonIsDown( "LStick", BT ) && L3 = 1)
        {
            SendInput {Numpad2 Up}
            Sleep 200
            L3 := 0
        }
        ; End of L3 to Numpad2


        ; Start of Proper Aim With L1
        if (XInputButtonIsDown( "LB", BT ))
        {
            SendInput {Numpad1 Down}
            SendInput {Numpad4 Down}

            if (!XInputButtonIsDown( "X", BT ))
            {
            SendInput {Numpad3 Down}
            }
            while (XInputButtonIsDown( "LB", BT ))
            {
                Loop, 1
                {
                    BT := XInput_GetState(A_Index-1).wButtons

                    ; Start of Firing Loop
                    if (XInputButtonIsDown( "X", BT ))
                    {
                        SendInput {Numpad3 Down}
                        SendInput {Numpad1 Up}
                        Loop
                        {
                            Loop, 1
                            {
                                BT := XInput_GetState(A_Index-1).wButtons
                                if (!XInputButtonIsDown( "X", BT ))
                                {
                                    SendInput {Numpad1 Down}
                                    SendInput {Numpad3 Up}
                                    Sleep 40
                                    SendInput {Numpad3 Down}
                                    break 2
                                }
                                if (!XInputButtonIsDown( "LB", BT ))
                                {
                                    break 2
                                }
                            }
                        }
                    }
                    ; End of Firing Loop

                    ; Start of B to Toggle Aim
                    if (!XInputButtonIsDown( "B", BT ) && holdingY = 1)
                    {
                        holdingY := 0
                    }
                    if (XInputButtonIsDown( "B", BT ) && holdingY = 0)
                    {
                        if (aimLock = 1)
                        {
                            SendInput {Numpad4 Up}
                            aimLock := 0
                        }
                        else
                        {
                            SendInput {Numpad4 Down}
                            aimLock := 1
                        }
                        holdingY := 1
                    }
                    ; End of B to Toggle Aim
                }
            }
            SendInput {Numpad1 Up}
            if (!XInputButtonIsDown( "X", BT ))
            {
                SendInput {Numpad5 Down}
                Sleep 40
                SendInput {Numpad5 Up}
                SendInput {Numpad3 Up}
            }
            SendInput {Numpad4 Up}
            aimLock := 1
        }
        ; End of Proper Aim With L1


        ; Start of No Pressure Grabbing
        if (XInputButtonIsDown( "B", BT ))
        {
            SendInput {Numpad1 Down}
            Sleep 250
            Loop
            {
                Loop, 1
                {
                    BT := XInput_GetState(A_Index-1).wButtons
                    RT := XInput_GetState(A_Index-1).bRightTrigger

                    ; Start of Toggle L3
                    if (XInputButtonIsDown( "LStick", BT ))
                    {
                        if (L3 = 0)
                        {
                            SendInput {Numpad2 Down}
                            Sleep 500
                            L3 := 1
                        }
                        else
                        {
                            SendInput {Numpad2 Up}
                            Sleep 200
                            L3 := 0
                        }
                    }
                    ; End of Toggle L3

                    ; Start of Square to Numpad3
                    if (!XInputButtonIsDown( "X", BT ) && holdingX = 1)
                    {
                        SendInput {Numpad3 Up}
                        holdingX := 0
                    }
                    
                    if (XInputButtonIsDown( "X", BT ) && holdingX = 0)
                    {
                        SendInput {Numpad2 Up}
                        SendInput {Numpad3 Down}
                        holdingX := 1
                    }
                    ; End of Square to Numpad3

                    ; Start of L1 to Numpad4
                    if (XInputButtonIsDown( "LB", BT ) && holdingLB = 0)
                    {
                        SendInput {Numpad4 Down}
                        holdingLB := 1
                    }
                    if (!XInputButtonIsDown( "LB", BT ) && holdingLB = 1)
                    {
                        SendInput {Numpad4 Up}
                        holdingLB := 0
                    }
                    ; End of L1 to Numpad4

                    ; Start of Hide Weapon While Grabbing
                    if (holdingX = 1 && RT > 40)
                    {
                        SendInput {Numpad2 Down}
                        Sleep 400
                    }
                    if (XInputButtonIsDown( "B", BT ) && holdingB = 0)
                    {
                        SendInput {Numpad2 Up}
                        holdingB := 1
                    }
                    ; End of Hide Weapon While Grabbing

                    ; Start of Leting Go Sequence
                    if (XInputButtonIsDown( "Y", BT ))
                    break 2

                    if (!XInputButtonIsDown( "B", BT ))
                    {
                        Btimer := 0
                        holdingB := 0
                        Loop
                        {
                            Loop, 1
                            {
                                BT := XInput_GetState(A_Index-1).wButtons
                                Btimer++
                                Sleep 1

                                if (XInputButtonIsDown( "B", BT ) || XInputButtonIsDown( "X", BT ))
                                break 2

                                if (Btimer = 30)
                                break 4
                            }
                        }
                    }
                    ; End of Leting Go Sequence
                }
            }
            L3 := 0
            holdingB := 0
            SendInput {Numpad1 Up}
            SendInput {Numpad2 Up}
            Sleep 500
        }
        ; End of No Pressure Grabbing
    }
}

^0::
ExitApp