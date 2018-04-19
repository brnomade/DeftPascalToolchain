# DeftPascalToolchain

A tool chain to automate the build (compile and link) of pascal projects written in Deft Pascal for the Tandy (Radio Shack) TRSCOLOR (a.k.a. CoCo)

Requirements:

- Deft Pascal II V4.1 - http://www.colorcomputerarchive.com/coco/Disks/Programming/Deft%20Pascal%204.1%20(DEFT%20Systems).zip
- AGS Library v16 (for using the graphic primitives and graphic UI objects) - http://www.kenandmartha.com/coco/AGS.html
- Mame 0196b or higher (CoCo emulator where Deft Pascal will run) - http://mamedev.org
- AutoIT v3 or higher - freeware - (to automate the keystrokes when running Deft Pascal) - https://www.autoitscript.com/site/
- Windows (as the .bat files were written on a Windows10 machine) 
- a source code editor (currently I am using Context v0.98.6 - freeware - www.contexteditor.org)
- ROM files for Mame - I am currently emulating a CoCo 2B -  http://www.colorcomputerarchive.com/coco/ROMs/MESS/

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



