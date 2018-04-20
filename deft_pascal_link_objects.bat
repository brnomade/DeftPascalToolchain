@ECHO OFF

SETLOCAL

ECHO DEFT LINKER II VERSION 4.1A
ECHO LINKER AUTOMATION SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO DEFT PASCAL DSK FOLDER: %DEFT_DSK_FOLDER%
ECHO DEFT PASCAL DSK FILE: %DEFT_DSK_FILE%
ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~1
ECHO MAME FOLDER: %MAME_FOLDER%
ECHO AUTOIT FOLDER: %AUTOIT_FOLDER%

ECHO ------------------------
ECHO UPDATING DSK FILE
ECHO ------------------------

ECHO Deleting old %~1.PRJ on %~1.dsk
"%MAME_FOLDER%\imgtool.exe" del coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" %~1.PRJ
ECHO Copying new %~1.PRJ to %~1.dsk
"%MAME_FOLDER%\imgtool.exe" put coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" "%DEFT_PROJECTS_FOLDER%\%~1\%~1.prj" %~1.PRJ --ftype=binary --filter=ascii

ECHO ------------------------
ECHO DSK FILE CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" 

ECHO ------------------------
ECHO INVOKING MAME
ECHO ------------------------

cd "%MAME_FOLDER%"
@ECHO ON
start .\mame64.exe coco2b -flop1 "%DEFT_DSK_FOLDER%\%DEFT_DSK_FILE%" -flop2 "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" -window -keepaspect -natural -speed 3.0
@ECHO OFF

ECHO ------------------------
ECHO EXECUTING DEFT LINKER 
ECHO ------------------------

cd "%AUTOIT_FOLDER%"
@ECHO ON
".\autoit3.exe" "%DEFT_PROJECTS_FOLDER%\deft_linker_keystrokes_automation.au3" %~1
@ECHO OFF

ECHO ------------------------
ECHO LINKER OUTPUT
ECHO ------------------------

ECHO Deleting old %~1.LST from project folder
del "%DEFT_PROJECTS_FOLDER%\%~1\%~1.lst"
cd "%DEFT_PROJECTS_FOLDER%\%~1"
ECHO Retrieving new %~1.LST from %~1.dsk
"%MAME_FOLDER%\imgtool.exe" get coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" %~1.LST --filter=ascii
type "%DEFT_PROJECTS_FOLDER%\%~1\%~1.lst"

ECHO ------------------------
@ECHO ON