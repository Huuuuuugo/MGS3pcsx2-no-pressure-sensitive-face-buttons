#include <Xinput>
; Constants for gamepad buttons
PovUp       = 0x0001
PovDown     = 0x0002
PovLeft     = 0x0004
PovRight    = 0x0008
Start       = 0x0010
Back        = 0x0020
LStick      = 0x0040
RStick      = 0x0080
LB          = 0x0100
RB          = 0x0200
A           = 0x1000
B           = 0x2000
X           = 0x4000
Y           = 0x8000

XInputButtonIsDown( ButtonName, bidButtonState )
{
   isDown := false  ; If something screws up, we want to return false.
   
   If ( bidButtonState & %ButtonName% )
      isDown := true  ; Return true if bidButtonState matches ButtonName
   Else isDown := false  ; Return false otherwise
   
   Return %isDown%
}

XInputButtonState( bsButtonState )
{
   Status := ""
   
   If XInputButtonIsDown( "A", bsButtonState )
      Status .= "A,"
   If XInputButtonIsDown( "B", bsButtonState )
      Status .= "B,"
   If XInputButtonIsDown( "X", bsButtonState )
      Status .= "X,"
   If XInputButtonIsDown( "Y", bsButtonState )
      Status .= "Y,"
   If XInputButtonIsDown( "LB", bsButtonState )
      Status .= "LB,"
   If XInputButtonIsDown( "RB", bsButtonState )
      Status .= "RB,"
   If XInputButtonIsDown( "LStick", bsButtonState )
      Status .= "LStick,"
   If XInputButtonIsDown( "RStick", bsButtonState )
      Status .= "RStick,"
   If XInputButtonIsDown( "Back", bsButtonState )
      Status .= "Back,"
   If XInputButtonIsDown( "Start", bsButtonState )
      Status .= "Start,"
   If XInputButtonIsDown( "PovUp", bsButtonState )
      Status .= "PovUp,"
   If XInputButtonIsDown( "PovDown", bsButtonState )
      Status .= "PovDown,"
   If XInputButtonIsDown( "PovLeft", bsButtonState )
      Status .= "PovLeft,"
   If XInputButtonIsDown( "PovRight", bsButtonState )
      Status .= "PovRight,"
   
   Return SubStr( Status, 1, -1 ) ; Omit the trailing comma
}