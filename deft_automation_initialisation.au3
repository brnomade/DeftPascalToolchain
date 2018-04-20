#include-once
#include "deft_automation_library.au3"

;initialisation of AutoIT parameters - applies to all scripts

AutoItSetOption ("SendKeyDownDelay" , Int(IniReadWrapper("Control Values","KeyboardDelay")))