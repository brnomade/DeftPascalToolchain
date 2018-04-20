#include-once
#include <MsgBoxConstants.au3>

Func IniReadWrapper($sSection, $sKey)
     Return IniRead(@ScriptDir & "\deft_automation.ini",$sSection,$sKey,"")
EndFunc

Func waitForPrompt($sSection, $sKey) 
    ; Wait until the prompt cursor is presented on the screen
    ; Use relative coordinates read from INI file.
    Local $sIniValue
    Local $iX = 0
    Local $iY = 0
    Local $wP
    Local $iColor = 0
    Local $sColorExpected

    $sIniValue = StringSplit(IniReadWrapper($sSection,$sKey),",")
    If $sIniValue[0] <> 2 then
        MsgBox($MB_OK + $MB_ICONERROR, "Error reading from INI file", "Couldn't find Section '" & $sSection & "' or Key '" & $sKey & "' on file. Press OK to return to editor.")
        exit
    EndIf

    $sColorExpected = IniReadWrapper("Prompt Colors","Cursor")
    If $sColorExpected = "" then
        MsgBox($MB_OK + $MB_ICONERROR, "Error reading from INI file", "Couldn't find Section '" & $sSection & "' or Key '" & $sKey & "' on file. Press OK to return to editor.")
        exit
    EndIf
 
    Do
       $wP = WinGetPos("[CLASS:MAME]", "")
       $iX = Int($sIniValue[1]) + $wP[0]
       $iY = Int($sIniValue[2]) + $wP[1]
       MouseMove($iX, $iY)
       $iColor = PixelGetColor($iX, $iY)
       Sleep(500)    
    Until ($iColor > 0) AND ($iColor <> Int($sColorExpected))
    Return
EndFunc
