#include <MsgBoxConstants.au3>
#include "deft_automation_library.au3"

; Initialise
AutoItSetOption ("SendKeyDownDelay" , Int(IniReadWrapper("Control Values","KeyPressDelay")))

; Start script
WinWait("[CLASS:MAME]", "")
WinActivate("[CLASS:MAME]", "")

;Start Linker
waitForPrompt("Power Up Prompt","Boot")
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
MsgBox($MB_OK, "Waiting for Disk to Finish Operating", "Press OK to return to editor.")
WinClose("[CLASS:MAME]", "")
