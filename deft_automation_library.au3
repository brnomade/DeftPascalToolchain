#include-once
#include <MsgBoxConstants.au3>

Func IniReadWrapper($sSection, $sKey)
   Local $myfile = "deft_automation.ini"
   ;Local $sections = ""
   ;Local $ziniValue = ""

   If Not FileExists(@ScriptDir & "\" & $myfile) Then
                MsgBox($MB_SYSTEMMODAL, "Error", "[" & @ScriptDir & $myfile & "] not found!")
				Exit;
	EndIf

  ; $sections = IniReadSectionNames(@ScriptDir & "\" & $myfile)
  ; MsgBox($MB_SYSTEMMODAL, "2 - INFO", "content from file : [" & @ScriptDir & "\" & $myfile & "] is [" & $sections & "]")

  ; $sections = IniReadSection(@ScriptDir & "\" & $myfile,$sSection)
  ; MsgBox($MB_SYSTEMMODAL, "3 - INFO", "content from file : [" & @ScriptDir & "\" & $myfile & "], section [" & $sSection & "] is [" & $sections & "]")


  ; Local $hFileOpen = FileOpen(@ScriptDir & "\" & $myfile)
  ; If $hFileOpen = -1 Then
  ;      MsgBox($MB_SYSTEMMODAL, "3 - Error", "An error occurred when reading the file.")
  ;      Exit;
  ; EndIf
  ; Local $sFileRead = FileRead($hFileOpen)
  ; FileClose($hFileOpen)
  ; MsgBox($MB_SYSTEMMODAL, "4 - INFO", "Contents of the file:" & @CRLF & $sFileRead)

   Local $sIniValue = IniRead(@ScriptDir & "\" & $myfile,$sSection,$sKey,"")
  ; MsgBox($MB_SYSTEMMODAL, "INI READ WRAPPER 2", "section [" & $sSection & "] key [" & $sKey & "] is [" & $sIniValue & "]")
   RETURN $sIniValue;
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

    $sIniValue = IniReadWrapper($sSection,$sKey)
	;MsgBox($MB_SYSTEMMODAL, "WAIT FROM PROMPT - STEP 1", "section [" & $sSection & "] key [" & $sKey & "] is [" & $sIniValue & "]")
	$sIniValue = StringSplit($sIniValue,",")
	If $sIniValue[0] <> 2 then
        MsgBox($MB_OK + $MB_ICONERROR, "Error in step 1 reading from INI file", "Couldn't find Section '" & $sSection & "' or Key '" & $sKey & "' on file " & @ScriptDir & "\deft_automation.ini" & ". Press OK to return to editor.")
        exit
    EndIf

    $sColorExpected = IniReadWrapper("Prompt Color","Cursor")
    ;MsgBox($MB_SYSTEMMODAL, "WAIT FOR PROMPT - STEP 2", "section [Prompt Color] key [Cursor] is [" & $sColorExpected & "]")
	If $sColorExpected = "" then
        MsgBox($MB_OK + $MB_ICONERROR, "Error in step 2 reading from INI file", "Couldn't find Section [Prompt Color] or Key [Cursor] on file " & @ScriptDir & "\deft_automation.ini" & ". Press OK to return to editor.")
        exit
    EndIf

    Do
       $wP = WinGetPos("[CLASS:MAME]", "")
       $iX = Int($sIniValue[1]) + $wP[0]
       $iY = Int($sIniValue[2]) + $wP[1]
       ;MouseMove($iX, $iY)
       $iColor = PixelGetColor($iX, $iY)
       Sleep(500)
    Until ($iColor > 0) AND ($iColor <> Int($sColorExpected))
    Return
EndFunc
