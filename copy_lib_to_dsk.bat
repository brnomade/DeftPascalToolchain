@ECHO OFF

SETLOCAL

ECHO COPY LIBRARY FILE TO DSK
ECHO SCRIPT - VERSION 1.0
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO LIBRARY NAME: %~1
ECHO SOURCE PROJECT: %~2
ECHO TARGET PROJECT: %~3
ECHO MAME FOLDER: %MAME_FOLDER%

ECHO ------------------------
ECHO SOURCE PROJECT DSK CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk"

ECHO ------------------------
ECHO TARGET PROJECT DSK CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk"

ECHO ------------------------
ECHO UPDATING TARGET DSK FILE
ECHO ------------------------

ECHO Deleting old %~1.LIB on %~3.dsk
"%MAME_FOLDER%\imgtool.exe" del coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk" %~1.LIB
ECHO Deleting old %~1.INT on %~3.dsk
"%MAME_FOLDER%\imgtool.exe" del coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk" %~1.INT

ECHO Retrieving %~1.LIB from %~2.dsk
"%MAME_FOLDER%\imgtool.exe" get coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk" %~1.lib
ECHO Retrieving %~1.INT from %~2.dsk
"%MAME_FOLDER%\imgtool.exe" get coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~2\%~2.dsk" %~1.int

ECHO Copying %~1.LIB to %~3.dsk
"%MAME_FOLDER%\imgtool.exe" put coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk" %~1.lib %~1.LIB
ECHO Copying %~1.INT to %~3.dsk
"%MAME_FOLDER%\imgtool.exe" put coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk" %~1.int %~1.INT --ftype=binary --filter=ascii

ECHO ------------------------
ECHO TARGET PROJECT DSK CONTENTS
ECHO ------------------------

"%MAME_FOLDER%\imgtool.exe" dir coco_jvc_rsdos "%DEFT_PROJECTS_FOLDER%\%~3\%~3.dsk"

ECHO ------------------------
@ECHO ON