@ECHO OFF

SETLOCAL

ECHO COPY FILE FROM DSK
ECHO SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~1
ECHO FILE TO COPY: %~2
ECHO MAME FOLDER: %MAME_FOLDER%

ECHO ------------------------
ECHO PROJECT FOLDER CONTENTS
ECHO ------------------------

dir "%DEFT_PROJECTS_FOLDER%\%~1"

ECHO ------------------------
ECHO DSK FILE CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" 

ECHO ------------------------
ECHO COPY FILE
ECHO ------------------------

ECHO Deleting old %~2 from project folder
del "%DEFT_PROJECTS_FOLDER%\%~1\%~2"
cd "%DEFT_PROJECTS_FOLDER%\%~1"
ECHO Retrieving new %~2 from %~1.dsk
"%MAME_FOLDER%\imgtool.exe" get coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~1\%~1.dsk" %~2 --filter=ascii

ECHO ------------------------
ECHO PROJECT FOLDER CONTENTS
ECHO ------------------------

dir "%DEFT_PROJECTS_FOLDER%\%~1"

ECHO ------------------------
@ECHO ON