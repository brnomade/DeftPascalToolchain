@ECHO OFF

SETLOCAL

ECHO CREATE NEW DEFT PASCAL PROJECT SCRIPT - VERSION 1.0
ECHO FOR DEFT PASCAL II VERSION 4.1 WITH AGS LIBRARY
ECHO DEVELOPED BY ANDRE BALLISTA

ECHO ------------------------
ECHO ENVIRONMENT SETTINGS 
ECHO ------------------------

CALL "%~dp0%deft_pascal_toolchain_configuration.bat"

ECHO PROJECTS FOLDER: %DEFT_PROJECTS_FOLDER%
ECHO PROJECT FOLDER: %~1
ECHO SOURCE CODE EDITOR FOLDER: %EDITOR_FOLDER%

ECHO ------------------------
ECHO CREATING PROJECT FOLDER
ECHO ------------------------

@ECHO ON
cd "%DEFT_PROJECTS_FOLDER%"
mkdir %~1
@ECHO OFF

ECHO ------------------------
ECHO CREATING PROJECT FILES
ECHO ------------------------

cd "%DEFT_PROJECTS_FOLDER%\%~1"
@ECHO ON
copy "%DEFT_PROJECTS_FOLDER%\new_deft_pascal_project_disk.dsk" "%DEFT_PROJECTS_FOLDER%\%~1\"
rename "%DEFT_PROJECTS_FOLDER%\%~1\new_deft_pascal_project_disk.dsk" %~1.dsk
copy "%DEFT_PROJECTS_FOLDER%\new_deft_pascal_project_source.pas" "%DEFT_PROJECTS_FOLDER%\%~1\"
rename "%DEFT_PROJECTS_FOLDER%\%~1\new_deft_pascal_project_source.pas" %~1.pas
copy "%DEFT_PROJECTS_FOLDER%\new_deft_pascal_project_objects_file.txt" "%DEFT_PROJECTS_FOLDER%\%~1\"
rename "%DEFT_PROJECTS_FOLDER%\%~1\new_deft_pascal_project_objects_file.txt" %~1.prj
echo %~1/OBJ:1 >> "%DEFT_PROJECTS_FOLDER%\%~1\%~1.prj"
echo DEFTAGS/LIB:1 >> "%DEFT_PROJECTS_FOLDER%\%~1\%~1.prj"
@ECHO OFF

ECHO ------------------------
ECHO PROJECT FOLDER CONTENTS
ECHO ------------------------

dir "%DEFT_PROJECTS_FOLDER%\%~1"

ECHO ------------------------
ECHO EXECUTION COMPLETED...
ECHO ------------------------
@ECHO ON