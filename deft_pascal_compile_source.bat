@ECHO OFF

SETLOCAL

ECHO DEFT PASCAL II VERSION 4.1
ECHO COMPILE AUTOMATION SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

SET DEFT_DSK_FOLDER=C:\Users\Andre\Downloads\TRS COLOR\DeftPascal\Test
SET DEFT_DSK_FILE=deft.dsk
SET DEFT_PROJECTS_FOLDER=C:\Users\Andre\Downloads\TRS COLOR\DeftPascal\Test\Projects
SET MAME_FOLDER=C:\Users\Andre\Downloads\TRS COLOR\mame0196b_64bit
SET AUTOIT_FOLDER=E:\Program Files (x86)\AutoIt3

ECHO DEFT PASCAL DSK FOLDER: %DEFT_DSK_FOLDER%
ECHO DEFT PASCAL DSK FILE: %DEFT_DSK_FILE%
ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~1
ECHO MAME FOLDER: %MAME_FOLDER%
ECHO AUTOIT FOLDER: %AUTOIT_FOLDER%

ECHO ------------------------
ECHO PROJECT FOLDER CONTENTS
ECHO ------------------------

dir "%DEFT_PROJECTS_FOLDER%\%~1"

ECHO ------------------------
ECHO UPDATING DSK FILE
ECHO ------------------------

ECHO Deleting old %~1.PAS on %~1.dsk
"%MAME_FOLDER%\imgtool.exe" del coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" %~1.PAS
ECHO Copying new %~1.PAS to %~1.dsk
"%MAME_FOLDER%\imgtool.exe" put coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" "%DEFT_PROJECTS_FOLDER%\%~1\%~1.pas" %~1.PAS --ftype=binary --filter=ascii
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
ECHO EXECUTING DEFT PASCAL 
ECHO ------------------------

@ECHO ON
start /W "%AUTOIT_FOLDER%\autoit3.exe" "%DEFT_PROJECTS_FOLDER%\deft_pascal_keystrokes_automation.au3" %~1
@ECHO OFF

ECHO ------------------------
ECHO COMPILATION OUTPUT
ECHO ------------------------

ECHO Deleting old %~1.LST from project folder
del "%DEFT_PROJECTS_FOLDER%\%~1\%~1.lst"
cd "%DEFT_PROJECTS_FOLDER%\%~1"
ECHO Retrieving new %~1.LST from %~1.dsk
"%MAME_FOLDER%\imgtool.exe" get coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" %~1.LST --filter=ascii
type "%DEFT_PROJECTS_FOLDER%\%~1\%~1.lst"

ECHO ------------------------
@ECHO ON