import sys
import os
import configparser
import argparse
import subprocess

# function to handle windows path names with empty spaces
# in linux or ios this function is neutral
def safepath( str ):
	if sys.platform.startswith('win'):
		stringcommand = '"' + str + '"'
	else: 
		stringcommand = str
	return stringcommand
# end function


	
print("")
print("DEFT PASCAL II VERSION 4.1")
print("COMPILE SINGLE MODULE - AUTOMATION SCRIPT VERSION 1.0")
print("DEVELOPED BY ANDRE BALLISTA")
print("")

parser = argparse.ArgumentParser(description="Compile a single Deft Pascal library file.")
parser.add_argument("file",help="Library file name to be compiled. File extension is not needed. Filepath is not needed as the location of the file is derived from the configuration (ini) file.")
parser.add_argument("folder",help="Folder name where the library file is located. Folder is assumed to be under the PROJECTS_HOME folder defined in the configuration (ini) file.")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read("deft_pascal_toolchain_configuration.ini")

print("------------------------")
print("SETTINGS") 
print("------------------------")
print("")

print("DEFT PASCAL DSK FOLDER:", safepath(config["DEFT SETTINGS"]["DEFT_DSK_FOLDER"]))
print("DEFT PASCAL DSK FILE:", config["DEFT SETTINGS"]["DEFT_DSK_FILE"])
print("PROJECTS HOME:", safepath(config["PROJECT SETTINGS"]["PROJECTS_HOME"]))
print("PROJECT FOLDER:", args.folder)
print("LIBRARY SOURCE:", args.file + ".MOD")
print("MAME FOLDER:", safepath(config["MAME SETTINGS"]["MAME_FOLDER"]))
print("AUTOIT FOLDER:", safepath(config["AUTOIT SETTINGS"]["AUTOIT_FOLDER"]))

print("")
print("------------------------")
print("PROJECT FOLDER CONTENTS")
print("------------------------")
print("")

if sys.platform.startswith('win'):
	dircommand = "dir"
	typecommand = "type"
else: 
	dircommand = "ls -la"
	typecommand = "cat"
	
oscommand = dircommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder) )
#print(oscommand)
subprocess.call(oscommand, shell=True)

print("")
print("------------------------")
print("UPDATING DSK FILE")
print("------------------------")
print("")


print("Deleting old " + args.file + ".MOD on " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " del coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk")
oscommand = oscommand + " " + args.file + ".MOD"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("Copying new " + args.file + ".MOD to " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " put coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".mod" )
oscommand = oscommand + " " + args.file + ".MOD"
oscommand = oscommand + " --ftype=binary --filter=ascii"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("Deleting old " + args.file + ".INT on " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " del coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + args.file + ".INT"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("Copying new " + args.file + ".INT to " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " put coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".int" )
oscommand = oscommand + " " + args.file + ".INT"
oscommand = oscommand + " --ftype=binary --filter=ascii"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print ("Deleting old " + args.file + ".PRJ on " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " del coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + args.file + ".PRJ"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print ("Copying new " + args.file + ".PRJ to " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " put coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".prj" )
oscommand = oscommand + " " + args.file + ".PRJ"
oscommand = oscommand + " --ftype=binary --filter=ascii"
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("------------------------")
print("DSK FILE CONTENTS")
print("------------------------")

oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " dir coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
#print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("------------------------")
print("INVOKING MAME")
print("------------------------")

os.chdir( config["MAME SETTINGS"]["MAME_FOLDER"] );
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "mame64.exe") )
oscommand = oscommand + " coco2b"
oscommand = oscommand + " -flop1 " + safepath( os.path.join(config["DEFT SETTINGS"]["DEFT_DSK_FOLDER"], config["DEFT SETTINGS"]["DEFT_DSK_FILE"]) )
oscommand = oscommand + " -flop2 " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " -window -keepaspect -natural -speed " + config["MAME SETTINGS"]["MAME_SPEED"]
print(oscommand)
subprocess.Popen(oscommand)
print("")

print("------------------------")
print("EXECUTING DEFT PASCAL") 
print("------------------------")

oscommand = safepath( os.path.join(config["AUTOIT SETTINGS"]["AUTOIT_FOLDER"], "autoit3.exe") )
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], "deft_pascal_keystrokes_automation_for_library_build.au3"))
oscommand = oscommand + " " + args.file
print(oscommand)
subprocess.run(oscommand, shell=True)
print("")

print("------------------------")
print("COMPILATION OUTPUT")
print("------------------------")

print ("Deleting old " + args.file + ".LST from project folder")
oscommand = os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".lst" 
os.remove(oscommand)
os.chdir(os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder) )
print ("Retrieving new " + args.file + ".LST from " + args.file + ".dsk")
oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
oscommand = oscommand + " get coco_jvc_rsdos"
oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
oscommand = oscommand + " " + args.file + ".LST"
oscommand = oscommand + " --filter=ascii"
#print(oscommand)
subprocess.run(oscommand, shell=True)
oscommand = typecommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".lst" ) 
#print(oscommand)
subprocess.run(oscommand, shell=True)


print("------------------------")

