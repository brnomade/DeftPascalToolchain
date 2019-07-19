#include <MsgBoxConstants.au3>
#include "autoit_trscolor_automation_library.au3"

; Created by Andre Ballista - 2019
; GNU General Public License v3.0 - See LICENSE file for details.

; Initialise
initialise_automation()

;Start Script
waitForPrompt("Power Up","Boot")

;Script Body
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send($CmdLine[1])
Send("/BIN")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

; Exit Script
MsgBox($MB_OK, "Message", "Press OK to close emulator and return to editor.")
finalise_automation()
