# DeftPascalToolchain

A tool chain to automate the build (compile and link) of Deft Pascal projects for the Tandy (Radio Shack) TRSCOLOR (a.k.a. CoCo)

[23/08/2018] - Toolchain in review. Instructions below are outdated. Focus now is to redevelope the whole solution in Python.

----

Requirements:

- Windows (as the .bat files were written on a Windows 10 machine) 
- Deft Pascal II V4.1 - http://www.colorcomputerarchive.com/coco/Disks/Programming/Deft%20Pascal%204.1%20(DEFT%20Systems).zip
- AGS Library v16 (for using the graphic primitives and graphic UI objects) - http://www.kenandmartha.com/coco/AGS.html
- Mame 0196b or higher (CoCo emulator where Deft Pascal will run) - http://mamedev.org
- ROM files for Mame - I am currently emulating a CoCo 2B -  http://www.colorcomputerarchive.com/coco/ROMs/MESS/
- AutoIT v3 or higher - freeware - (to automate the keystrokes when running Deft Pascal) - https://www.autoitscript.com/site/
- a source code editor (currently I am using ConTEXT v0.98.6 - freeware - www.contexteditor.org)

For convenience I have assembled a DSK containing the Deft Pascal and AGS Library in a single disk ready for use with Mame. You will find it on this repository.

How to Use:

First step is to ensure you have all required software installed on your computer. You can find guides for that on the internet and on the discussion foruns of the respective softwares.

In general terms:

1. Mame

Make sure Mame is installed on your machine. A front end is not needed for this toolchain.

Make sure the CoCo roms are placed in the /ROM folder under the mame folder. 

To confirm installation is working, from a DOS prompt, go to Mame folder and simply run mame64.exe. 

You should get the Mame emulator native interface opening and a list containing the ROMs to choose. If you double click on the ROM (coco2b was used) and on "Start Empty" on the next screen you should get the cool radioactive green screen typical of a CoCo.

As a final test, run  following command from a DOS prompt and from the Mame folder: mame64.exe coco2b

You should get a window with the emulated CoCo prompt.

NOTE: There are some parameters to be adjusted on MAME. Need to explain which and what values.

2. AutoIT

Download and install the software on your machine. No specific settings required.

3. ConTEXT

Download and install the software on your machine. No specific settings required.

4. Assumed Folder Structure

The scripts assume a pre-defined folder structure exists in your computer:

PROJECTS FOLDER - this is the main folder and will hold the automation scripts and your Deft Pascal projects. On the context of this toolchain, a project is simple a folder and the files contained in it.

An example:
A WINDOWS FOLDER
-PROJECTS 
     -HELLO1 
     -DEMO 
     -HELLO2 
     -APROJ1 
     -HELLO3 
 
 NOTES & LIMITATIONS: 
 - CoCo file name conventions and limitations apply here. So your folder and files must comply to the 8 characters size.
 - Folders and files must always be in uppercase.
 
 On the PROJECTS FOLDER you will need to place following files:
- deft_pascal_toolchain_configuration.bat
- create_new_deft_pascal_project.bat 
- deft_pascal_compile_source.bat
- deft_pascal_link_objects.bat
- deft_pascal_run_project.bat
- deft_automation_library.au3
- deft_automation.ini
- deft_linker_keystrokes_automation.au3
- deft_pascal_keystrokes_automation.au3
- drive_0_loadm_and_exec_keystrokes_automation.au3
- new_deft_pascal_project_disk.dsk
- new_deft_pascal_project_objects_file.txt
- new_deft_pascal_project_source.pas

5. Using the scripts:

- deft_pascal_toolchain_configuration.bat

This script contain the definition of the needed folders and files. It needs to be adjusted to match your own folder configuration.

The following variables must be declared:
     - EDITOR_FOLDER - This is the installation folder of your source code editor
     - EDITOR_EXECUTABLE - this is the executable of your source code. Only the file name and extension are needed.
     - DEFT_DSK_FOLDER - this is the folder where the dsk file is located. 
     - DEFT_DSK_FILE - this is the dsk file name and extension
     - DEFT_PROJECTS_FOLDER - folder where your toolchain scripts are located and where all projects subfolders will be created
     - MAME_FOLDER - This is the installation folder of Mame
     - AUTOIT_FOLDER - This is the installation folder for the AUTOIT sofrware

This script needs to be adjusted once and should only be changed if you relocate folders/files in your drive.

- create_new_deft_pascal_project.bat 

This script will create a brand new FOLDER and PROJECT FILES based on a name passed by parameter.
     - CoCo file name conventions and limitations apply here.
     - Folder and files must comply to the 8 characters size and always be in uppercase.
     - The script does not yet check or enforce such constraints.
 
This script must be executed from the PROJECTS FOLDER using the DOS command line. Make sure to open a CMD window to run the command.

This script requires the following files to be present on the same folder:
     - deft_pascal_toolchain_configuration.bat
     - new_deft_pascal_project_disk.dsk
     - new_deft_pascal_project_objects_file.txt
     - new_deft_pascal_project_source.pas

This script uses following configurations:
     - DEFT_PROJECTS_FOLDER
     - EDITOR_FOLDER
     - EDITOR_EXECUTABLE

Example Usage: 
 cd PROJECTS FOLDER
 .\create_new_deft_pascal_project.bat HELLO1

Above call will create a new folder called HELLO1 and will place HELLO1.pas, HELLO1.prj and HELLO1.dsk files into it. The script will also atemp to execute the editor passing the .pas and .prj files for opening.

- deft_pascal_compile_source.bat

This script will trigger the compilation of the SOURCE FILE identified by the name passed by parameter. The name must be without any extension. 

This script requires the following files to be present on the same folder:
     - deft_pascal_toolchain_configuration.bat
     - deft_automation.ini
     - deft_automation_library.au3
     - deft_automation_initialisation.au3
     - deft_pascal_keystrokes_automation.au3

This script uses following configurations:
     - DEFT_DSK_FOLDER
     - DEFT_DSK_FILE
     - DEFT_PROJECTS_FOLDER
     - MAME_FOLDER
     - AUTOIT_FOLDER

This script invokes following tools:
     - imgtool.exe from mame 
     - mame64.exe from mame
     - autoit3.exe from autoit

This script must be executed from the PROJECT FOLDER

Example Usage: 
 cd PROJECTS FOLDER 
 cd PROJECT 
 ..\deft_pascal_compile_source.bat HELLO1
     
Above call will copy the .pas and .prj files into the project dsk file. Will than execute mame using the dsk image. Will than start AutoIT to inject keystrokes on the CoCo emulator to start DEFT PASCAL, configure the correct parameters and trigger the source code compilation. Once compilation is completed, the script will extract the compilation report from the dsk file and present it to the editor.

- deft_pascal_link_objects.bat

This script will trigger the linkage of the object and library files defined on the .prj file passed by parameter. The filename must be without any extension. 

This script requires the following files to be present on the same folder:
     - deft_pascal_toolchain_configuration.bat
     - deft_automation.ini
     - deft_automation_library.au3
     - deft_automation_initialisation.au3
     - deft_linker_keystrokes_automation.au3

This script uses following configurations:
     - DEFT_DSK_FOLDER
     - DEFT_DSK_FILE
     - DEFT_PROJECTS_FOLDER
     - MAME_FOLDER
     - AUTOIT_FOLDER

This script invokes following tools:
     - imgtool.exe from mame 
     - mame64.exe from mame
     - autoit3.exe from autoit

This script must be executed from the PROJECT FOLDER

Example Usage: 
 cd PROJECTS FOLDER 
 cd PROJECT 
 ..\deft_pascal_link_objects.bat HELLO1 
 
Above call will copy the .prj file into the project dsk file. Will than execute mame using the dsk image. Will than start AutoIT to inject keystrokes on the CoCo emulator to start DEFT LINKER, configure the correct parameters and trigger the linkage process. Once linkage is completed, the script will extract the linkage report from the dsk file and present it to the editor.

The .prj file is prepared by the create_new_deft_pascal_project.bat when the project is created. You can edit the file and add more objects to be linked. If you change the prj file, observe that file DEFTAGS/LIB should be specified as the last object file to link, with the main file being the first one.

- deft_pascal_run_project.bat

This script will trigger the execution of the resulting binary of the project identified by the name passed by parameter. The filename must be without any extension. 

This script requires the following files to be present on the same folder:
     - deft_pascal_toolchain_configuration.bat
     - deft_automation.ini
     - deft_automation_library.au3
     - deft_automation_initialisation.au3
     - drive_0_loadm_and_exec_keystrokes_automation.au3

This script uses following configurations:
     - DEFT_PROJECTS_FOLDER
     - MAME_FOLDER
     - AUTOIT_FOLDER

This script invokes following tools:
     - imgtool.exe from mame 
     - mame64.exe from mame
     - autoit3.exe from autoit

This script must be executed from the PROJECT FOLDER

Example Usage: 
 cd PROJECTS FOLDER 
 cd PROJECT 
 ..\deft_pascal_run_project.bat HELLO1 
 
Above call will assume the .bin file is present in the project dsk file. Will than execute mame using the dsk image. Will than start AutoIT to inject keystrokes on the CoCo emulator to LOADM and EXEC the binary file. Once completed, the script will return to the editor. No lst file is produced.

6. Typical Workflow

The happy path for executing the toolchain is :

- create the project using create_new_deft_pascal_project.bat
- compile it using deft_pascal_compile_source.bat
- link it using deft_linker_link_objects.bat
- run it using deft_pascal_run_project.bat

7. Triggering the Toolchain from your editor of choice

The ConTEXT editor integrates nicely with the provided scripts. Use the Environment Options and configure the Execute Keys to trigger each script. In my setup I have F9 set to compile; F10 set to Link; F11 set to Run.

The settings I use are:
Execute: the full path and script name
Start in: %p - file path only
Parameter: %F - file name without extension
Save : All files before execution
Capture console output : Yes
Scroll console to the last line : Yes

8. Current Limitations

Due to the emulation based nature of the solution, the AUTOIT scripts depend heavily on PC performance, screen coordinates and graphics card configuration to find out what and when to type on Mame. I have tested the scripts in my desktop and laptop windows 10 machines and both work well. Still, there is a chance that the autoit scripts will need reconfiguration on your setup.

The file where such configurations can be done is deft_automation.ini

- To speed up compilation and linkage, Mame is run at speed 3x factor. My tests have indicated factors higher than that cause the keystrokes injected by AutoIT to be missed or lost, giving an unreliable use of the automation. At 3x factor, the operations is consistently reliable.

If during the execution of the compilation, linkage or execution you notice that the project file name is missed or incorrectly typed on the CoCo (via Mame), it is an indication that the keystrokes are too fast and not being recognised by the emulator. Edit file "deft_automation.ini" file and increase the value for "KeyboardDelay" key. Increase in increments of 5 and try the compilation, linkage and execution. The higher the value, the longer is the interval between key presses. 

- At the end of compilation, linkage or run, the AutoIT script will stop and open a "Click to Continue" message box. Once you click that Mame will be closed and control is returned to the Source Code editor. The message box was added because I found impossible to predict how much seconds were needed for the emulated disk controller to finish its operations. If I closed mame too soon (while the drive spinning sound was still playing) the files being generated by the CoCo wouldn't complete and therefore the compilation result could be broken. The time for drive to shutoff is also proportional (somehow) to the seize of the source code being compiled or linked. So, a fixed wait time at the end of the process was not reliable at all. Since there isn't a way to query mame about the status of its emulation (as far as I know), I decided to add the message box before closing mame and returning to the editor. This does not provide the seemless experience I was aiming for but it is close enough to allow proper development operations with the Deft Pascal system.

- If when running the compiler, linker or executing the resulting binary you notice that the keystrokes are not being placed in the correct fields or not appearing at all, this might indicate that the coordinates configured on the ini file are incorrect.

You can play with the coordinates on sections "Power Up Prompt", "Deft Pascal Prompts" and "Deft Linker Prompts" on the deft_automation.ini file. I am preparing a handy tool to allow calibration of those values. For the moment, the calibration is manual.



