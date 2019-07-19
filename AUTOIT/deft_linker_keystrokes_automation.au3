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
Send("LINKER")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

;Type ORIGIN
waitForPrompt("Deft Linker Prompts","Origin")
Send("{ENTER}")

;Type LIST FILE
waitForPrompt("Deft Linker Prompts","List")
Send($CmdLine[1])
Send("/LST:1{ENTER}")

;Type BINARY FILE
waitForPrompt("Deft Linker Prompts","BinaryFile")
Send($CmdLine[1])
Send("/BIN:1{ENTER}")

;Type PASCAL (Y/N)
waitForPrompt("Deft Linker Prompts","PascalFlag")
Send("Y{ENTER}")

;Type DEBUGGER (Y/N)
waitForPrompt("Deft Linker Prompts","DebuggerFlag")
Send("N{ENTER}")

;Type OBJECT FILES
waitForPrompt("Deft Linker Prompts","ObjNamesFile")
Send($CmdLine[1])
Send("/PRJ:1{ENTER}")

;Wait before closing Mame
MsgBox($MB_OK, "Waiting for Disk to Finish Operating", "Press OK to close emulator and return to editor.")
finalise_automation()
