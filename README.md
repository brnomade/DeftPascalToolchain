# DeftPascalToolchain

A tool chain to automate the build (compile and link) of pascal projects written in Deft Pascal for the Tandy (Radio Shack) TRSCOLOR (a.k.a. CoCo)

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
- deft_linker_link_objects.bat
- deft_pascal_run_project.bat
- deft_linker_keystrokes_automation.au3
- deft_pascal_keystrokes_automation.au3
- drive_0_loadm_and_exec_keystrokes_automation.au3
- new_deft_pascal_project_disk.dsk
- new_deft_pascal_project_objects_file.txt
- new_deft_pascal_project_source.pas

5. Using the scripts:

- create_new_deft_pascal_project.bat 

This script will create a brand new FOLDER and PROJECT FILES based on a name passed by parameter.
     - CoCo file name conventions and limitations apply here.
     - Folder and files must comply to the 8 characters size and always be in uppercase.
     - The script does not yet check or enforce such constraints.
 
This script must be executed from the PROJECTS FOLDER

This script requires the following files to be present on the same folder:
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
 ..\deft_pascal_compile_source.bat HELLO1 <br>
     
Above call will copy the .pas and .prj files into the project dsk file. Will than execute mame using the dsk image. Will than start AutoIT to inject keystrokes on the CoCo emulator to start DEFT PASCAL, configure the correct parameters and trigger the source code compilation. Once compilation is completed, the script will extract the compilation report from the dsk file and present it to the editor.

6. Triggering the Toolchain from your editor of choice

7. Typical Workflow




