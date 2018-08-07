@ECHO OFF

SETLOCAL

ECHO ADD FILE TO DSK
ECHO SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~2
ECHO FILE NAME: %~1
ECHO MAME FOLDER: %MAME_FOLDER%

ECHO ------------------------
ECHO PROJECT FOLDER CONTENTS
ECHO ------------------------

dir "%DEFT_PROJECTS_FOLDER%\%~2"

ECHO ------------------------
ECHO UPDATING DSK FILE
ECHO ------------------------

ECHO Deleting old %~1 on %~2.dsk
"%MAME_FOLDER%\imgtool.exe" del coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk" %~1
ECHO Copying new %~1 to %~2.dsk
"%MAME_FOLDER%\imgtool.exe" put coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk" "%DEFT_PROJECTS_FOLDER%\%~2\%~1" %~1 --ftype=binary --filter=ascii

ECHO ------------------------
ECHO DSK FILE CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk" 

ECHO ------------------------
@ECHO ON