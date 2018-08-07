@ECHO OFF

SETLOCAL

ECHO LAUNCH MAME WITH DSK FILES
ECHO SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO MAME FOLDER: %MAME_FOLDER%
ECHO HOME LOCATION: %~dp0%
ECHO DSK 1 : %~1
ECHO DSK 2 : %~2

ECHO ------------------------
ECHO INVOKING MAME
ECHO ------------------------

cd "%MAME_FOLDER%"
@ECHO ON
START /W .\mame64.exe coco2b -flop1 "%~1" -flop2 "%~2" -window -keepaspect -natural -speed 9.0
@ECHO OFF

ECHO ------------------------
PAUSE
@ECHO ON