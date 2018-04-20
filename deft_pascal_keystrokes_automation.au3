#include <MsgBoxConstants.au3>
#include "deft_automation_library.au3"
#include "deft_automation_initialisation.au3"

; Start of script
WinWait("[CLASS:MAME]", "")
WinActivate("[CLASS:MAME]", "")

;Start compiler
waitForPrompt("Power Up Prompt","Boot")
Send("DRIVE 0{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send("PASCAL")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

;Type Source file name
waitForPrompt("Deft Pascal Prompts","Source")
Send($CmdLine[1])
Send("/PAS:1{ENTER}")

;Type Object file name
waitForPrompt("Deft Pascal Prompts","Object")
Send($CmdLine[1])
Send("/OBJ:1{ENTER}")

;Type List file name
waitForPrompt("Deft Pascal Prompts","List")
Send($CmdLine[1])
Send("/LST:1{ENTER}")

;Type Debug Directive
waitForPrompt("Deft Pascal Prompts","Debug")
Send("N{ENTER}")

;Type Compiler Directives
waitForPrompt("Deft Pascal Prompts","Directive")
Send("{ENTER}")

;Wait before closing Mame
MsgBox($MB_OK, "Waiting for Disk to Finish Operating", "Press OK to return to editor.")
WinClose("[CLASS:MAME]", "")
