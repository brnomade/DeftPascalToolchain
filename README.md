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

Make sure Mame is installed on yourmachines. A front end is not needed for this toolchain.

Make sure the CoCo roms are placed in the /ROM folder under the mame folder. 

To confirm installation is working, from a DOS prompt, go to Mame folder and simply run mame64.exe. 

You should get the Mame emulator native interface opening and a list containing the ROMs to choose. If you double click on the ROM (coco2b was used) and on [Start Empty] on the next screen you should get the cool radioactive green screen typical of a CoCo.

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
<a windows folder>
|_PROJECTS
  |_HELLO1
  |_DEMO
  |_HELLO2
  |_APROJ1
  |_HELLO3
 
 NOTES & LIMITATIONS: 
 - CoCo file name conventions and limitations apply here. So your folder and files must comply to the 8 characters size.
 - Folders and files must always be in uppercase.
 
 
  









