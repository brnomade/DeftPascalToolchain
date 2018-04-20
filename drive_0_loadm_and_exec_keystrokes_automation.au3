#include <MsgBoxConstants.au3>
#include "deft_automation_library.au3"
#include "deft_automation_initialisation.au3"

; Start of script
WinWait("[CLASS:MAME]", "")
WinActivate("[CLASS:MAME]", "")

;Start Program
waitForPrompt("Power Up Prompt","Boot")
Send("DRIVE 0{ENTER}")
Send("LOADM")
Send("{LSHIFT down}2{LSHIFT up}")
Send($CmdLine[1])
Send("/BIN")
Send("{LSHIFT down}2{LSHIFT up}")
Send(":EXEC{ENTER}")

MsgBox($MB_OK, "Project Binary Started...", "Press OK to return to editor.")

WinClose("[CLASS:MAME]", "")