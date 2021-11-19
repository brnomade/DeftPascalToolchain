# DeftPascalToolchain

A tool chain to automate the build (compile and link) of Deft Pascal projects for the Tandy (Radio Shack) TRSCOLOR (a.k.a. CoCo)

----

Requirements:

- Python 3.8 or higher
- Deft Pascal II V4.1 - http://www.colorcomputerarchive.com/coco/Disks/Programming/Deft%20Pascal%204.1%20(DEFT%20Systems).zip
- AGS Library v16 (for using the graphic primitives and graphic UI objects) - http://www.kenandmartha.com/coco/AGS.html
- Mame 0237b or higher (CoCo emulator where Deft Pascal will run) - http://mamedev.org
- ROM files for Mame - I am currently emulating a CoCo 2B -  http://www.colorcomputerarchive.com/coco/ROMs/MESS/
- a source code editor (currently I am using PyCharm Comumnity 2021.1 - www.contexteditor.org)
- PyCharm extension for Pascal: https://plugins.jetbrains.com/plugin/7340-i-pascal

For convenience I have assembled a DSK containing the Deft Pascal and AGS Library in a single disk ready for use with Mame. You will find it on this repository.

How to Use:

First step is to ensure you have all required software installed on your computer. You can find guides for that on the internet and on discussion forum of the respective softwares.

In general terms:

1. Mame

Make sure Mame is installed on your machine. A front end is not needed for this toolchain.

Make sure the CoCo roms are placed in the /ROM folder under the mame folder. 

To confirm installation is working, from a DOS prompt, go to Mame folder and simply run mame64.exe. 

You should get the Mame emulator native interface opening and a list containing the ROMs to choose. If you double click on the ROM (coco2b was used) and on "Start Empty" on the next screen you should get the cool radioactive green screen typical of a CoCo.

As a final test, run  following command from a DOS prompt and from the Mame folder: mame64.exe coco2b

You should get a window with the emulated CoCo prompt.

NOTE: There are some parameters to be adjusted on MAME. Need to explain which and what values.

2. PyCharm

Download and install the software on your machine. No specific settings required.

Install the i-pascal plugin for PyCharm. This is actually optional but can make it easier to code in Pascal.

Create a new PyCharm project on a new folder (for example: c:\DEFTPASCAL). Under this location you will create all your source code.

3. Folders and Directories

Create a new sub folder called Libraries and another one called Projects. In the end, you will have a structure like:

DEFTPASCAL
   |_ PROJECTS
   |_ LIBRARIES

Note, naming convention is flexible (upper or lower case can be used - aim to avoid spaces in the names)

PROJECTS FOLDER - under this, aim to have a new folder for each individual project you create. On the context of this toolchain, a project is simple a folder and the files contained in it.

NOTES & LIMITATIONS:
- CoCo file name conventions and limitations apply here. So your folder and files must comply to the 8 characters size.
- Folders and files must always be in uppercase.

4. Delphi Pascal ToolChain

Install the Delphi Pascal Tool Chain code either via requirements.txt or directly. The source code is in https://github.com/brnomade/DeftPascalToolchain

5. Configure PyCharm configurations - Compile

     name: dptcc - compile 
     script path: should point to dptcc.py (if this is in your python path then no actual path is needed, othewise make sure to setup the complete path)
     parameters: --project_folder $FileDir$  -source_file $FileName$ -dsk_file $FileNameWithoutAllExtensions$.dsk -list ALL
   
6. Configure PyCharm configurations - Link

   name: dptcc - linker
   script path: should point to dptcl.py (if this is in your python path then no actual path is needed, othewise make sure to setup the complete path)
   parameters: --project_folder $FileDir$  -source_file $FileName$ -dsk_file $FileNameWithoutAllExtensions$.dsk -list ALL

7. Configure the ToolChain Ini/Configuration file

- Place the ini file in your root folder (in this example, the DEFTPASCAL folder)
- Define the following variables in the Ini file:

  [COMPILER SETTINGS]
  compiler_folder = C:\CODING\TRSCOLOR\DEFTPASCAL
  compiler_disk = deft.dsk

  [LINKER SETTINGS]

  [RUNNER SETTINGS]

  [REPOSITORY SETTINGS]
  lib_folder = C:\CODING\TRSCOLOR\DeftPascal\Libraries

  [EMULATOR SETTINGS]
  emulator_folder = C:\RetroComputers\TRSCOLOR\Emulators\mame0237b_64bit
  emulator_app = mame
  emulator_rom = coco2b
  emulator_speed = 9
  emulator_delay = 3

 - compiler_folder - this is the folder where the Delphi dsk file is located
 - compiler_disk - this is the compiler dsk file name and extension
 - emulator_folder - This is the installation folder of Mame
 - emulator_app - this is the filename of the mame executable
 - emulator_rom - this is the specific rom the emulator should use
 - emulator_speed - this is how fast the emulator should be throttled
 - emulator_delay - this is the delay in seconds for the toolchain to start running after the emulator has been started 

8. Typical Workflow

The happy path for executing the toolchain is :

- create the project folder in PyCharm
- code and compile the source code using the "Run Compile" in PyCharm. 
- link the resulting obj file with "Run Link" in PyCharm
- run the resulting bin file using "Run Exec"in PyCharm

8. Current Limitations



