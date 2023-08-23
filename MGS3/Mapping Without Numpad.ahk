#SingleInstance force
#Persistent 
#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

1::
SendInput, {Numpad1}
Return

2::
SendInput, {Numpad2}
Return

3::
SendInput, {Numpad3}
Return

4::
SendInput, {Numpad4}
Return

5::
SendInput, {Numpad5}
Return

^0::
ExitApp