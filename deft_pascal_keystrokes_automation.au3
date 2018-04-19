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

;Start Compiler
Send("DRIVE 0{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send("PASCAL")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

;Wait for the compiler to start and present the prompt cursor on the screen
$x = 595
$y = 347
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;Source File
Send($CmdLine[1])
Send("/PAS:1{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 595
$y = 396
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;Object File
Send($CmdLine[1])
Send("/OBJ:1{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 595
$y = 442
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;Listing
Send($CmdLine[1])
Send("/LST:1{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 595
$y = 490
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

;Debug Information
Send("N{ENTER}")

;Wait for the cursor to be prompted on the screen
$x = 693
$y = 540
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until $iColor <> 524032

Send("{ENTER}")

;Wait for the compiler to finish its execution
$x = 335
$y = 624
;MouseMove($x,$y,10)
Do
   $iColor = PixelGetColor($x,$y)
   Sleep(500)
Until ($iColor = 32000)

;Sleep(5000)
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



