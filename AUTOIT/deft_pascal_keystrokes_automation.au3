#include <MsgBoxConstants.au3>
#include "autoit_trscolor_automation_library.au3"

; Created by Andre Ballista - 2019
; GNU General Public License v3.0 - See LICENSE file for details.


; Initialise
initialise_automation()

;Start Script
waitForPrompt("Power Up","Boot")

;Script Body
Send("{ENTER}{ENTER}{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send("PASCAL")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

;Type Source file name
waitForPrompt("Deft Pascal Prompts","Source")
Send($CmdLine[1])
Send(":1{ENTER}")

;Type Object file name
waitForPrompt("Deft Pascal Prompts","Object")
Send($CmdLine[2])
Send(":1{ENTER}")

;Type List file name
waitForPrompt("Deft Pascal Prompts","List")
Send($CmdLine[3])
Send(":1{ENTER}")

;Type Debug Directive
waitForPrompt("Deft Pascal Prompts","Debug")
Send("N{ENTER}")

;Type Compiler Directives
waitForPrompt("Deft Pascal Prompts","Directive")
Send("{ENTER}")

;Wait before closing Mame
MsgBox($MB_OK, "Waiting for Disk to Finish Operating", "Press OK to close emulator and return to editor.")
finalise_automation()

