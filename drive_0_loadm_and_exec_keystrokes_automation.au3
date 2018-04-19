#include <MsgBoxConstants.au3>

WinWait("[CLASS:MAME]", "")
WinActivate("[CLASS:MAME]", "")

AutoItSetOption ( "SendKeyDownDelay" , 45 )

;Wait until the computer has booted and a prompt cursor is presented on the screen
Local $x = 337
Local $y = 390
Local $iColor = 0
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until ($iColor > 0) AND ($iColor <> 524032)

;Start Program
Send("DRIVE 0{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send($CmdLine[1])
Send("/BIN")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

MsgBox($MB_OK, "Project Binary Started...", "Press OK to return to editor.")

WinClose("[CLASS:MAME]", "")



;Run("notepad.exe")
;Do
;   $aPos = MouseGetPos()
;   Local $iColor = PixelGetColor($aPos[0],$aPos[1])
;   WinActivate("Untitled - Notepad")
;   Send("[")
;   Send($aPos[0])
;   Send(":")
;   Send($aPos[1])
;   Send("=")
;   Send($iColor)
;   Send("]")
;   Send("{ENTER}")
;   WinActivate("[CLASS:MAME]", "")
;Until $aPos[0] <= 10
