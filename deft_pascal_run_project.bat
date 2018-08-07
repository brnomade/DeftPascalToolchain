@ECHO OFF

SETLOCAL

ECHO DEFT PASCAL II VERSION 4.1
ECHO LOADM AND EXEC AUTOMATION SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~1
ECHO MAME FOLDER: %MAME_FOLDER%

ECHO ------------------------
ECHO DSK FILE CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" 

ECHO ------------------------
ECHO INVOKING MAME
ECHO ------------------------

cd "%MAME_FOLDER%"
@ECHO ON
start .\mame64.exe coco2b -flop1 "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" -window -keepaspect -natural -console -debug
@ECHO OFF

ECHO ------------------------
ECHO EXECUTING DEFT PASCAL 
ECHO ------------------------

@ECHO ON
"%AUTOIT_FOLDER%\autoit3.exe" "%DEFT_PROJECTS_FOLDER%\drive_0_loadm_and_exec_keystrokes_automation.au3" %~1
@ECHO OFF

ECHO ------------------------
ECHO EXECUTION OUTPUT
ECHO ------------------------

ECHO Deleting old %~1.LST from project folder
del "%DEFT_PROJECTS_FOLDER%\%~1\%~1.lst"
cd "%DEFT_PROJECTS_FOLDER%\%~1"

ECHO ------------------------
ECHO EXECUTION COMPLETED...
ECHO ------------------------
@ECHO ON


