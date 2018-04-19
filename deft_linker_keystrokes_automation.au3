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

;Start Linker
Send("DRIVE 0{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send("LINKER")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

;Wait for the linker to start and present the prompt cursor on the screen
$x = 855
$y = 347
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;ORIGIN
Send("{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 855
$y = 393
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;LIST FILE
Send($CmdLine[1])
Send("/LST:1{ENTER}")


;Wait for the cursor to be prompted on the screen
$x = 855
$y = 438
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;BINARY FILE
Send($CmdLine[1])
Send("/BIN:1{ENTER}")


;Wait for the cursor to be prompted on the screen
$x = 855
$y = 494
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;PASCAL (Y/N)
Send("Y{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 855
$y = 536
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;DEBUGGER (Y/N)
Send("N{ENTER}")


;Wait for the cursor to be prompted on the screen
$x = 855
$y = 588
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;OBJECT FILES
Send($CmdLine[1])
Send("/PRJ:1{ENTER}")

;Wait for the linker to finish its execution
$x = 702
$y = 657
;$y = 848  -- position on the screen when the linker presents IO errors. Unclear what other errors might be displayed and where...
;MouseMove($x,$y,10)
;Run("notepad.exe")
;Local $aPos
Do
   ;WinActivate("[CLASS:MAME]", "")
   ;$aPos = MouseGetPos()
   ;$iColor = PixelGetColor($aPos[0],$aPos[1])
   $iColor = PixelGetColor($x,$y)
   ;WinActivate("Untitled - Notepad")
   ;Send("[")
   ;Send($aPos[0])
   ;Send(":")
   ;Send($aPos[1])
   ;Send("=")
   ;Send($iColor)
   ;Send("]")
   ;Send("{ENTER}")
   Sleep(500)
Until ($iColor = 31744); $aPos[0] <= 0

;Sleep(3000)
MsgBox($MB_OK, "Waiting for Disk to Finish Operating", "Press OK to return to editor.")

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
