#include <MsgBoxConstants.au3>

Func waitForPrompt($sSection, $sKey) 
    ; Wait until the prompt cursor is presented on the screen
    ; Use relative coordinates read from INI file.
    Local $sIniValue
    Local $iX = 0
    Local $iY = 0
    Local $wP
    Local $iColor = 0

    $sIniValue =StringSplit(IniRead("C:\CODING\TRSCOLOR\DeftPascal\Projects\deft_automation.ini",$sSection,$sKey,""),",");
    If $sIniValue[0] <> 2 then
        MsgBox($MB_SYSTEMMODAL, "", "error")
        exit
        break
    EndIf
    Do
       $wP = WinGetPos("[CLASS:MAME]", "")
       $iX = Int($sIniValue[1]) + $wP[0]
       $iY = Int($sIniValue[2]) + $wP[1]
       MouseMove($iX, $iY)
       $iColor = PixelGetColor($iX, $iY)
       Sleep(500)    
    Until ($iColor > 0) AND ($iColor <> 524032)
    Return
EndFunc

; Start of script
WinWait("[CLASS:MAME]", "")
WinActivate("[CLASS:MAME]", "")
AutoItSetOption ( "SendKeyDownDelay" , 45 )

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
