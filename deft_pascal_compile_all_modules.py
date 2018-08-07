import sys
import os
import configparser
import argparse
import subprocess
import shutil

# function to handle windows path names with empty spaces
# in linux or ios this function is neutral
def safepath( str ):
	if sys.platform.startswith('win'):
		stringcommand = '"' + str + '"'
	else: 
		stringcommand = str
	return stringcommand
# end function

# recursive function to navigate all files
def getDependencyList ( folder, file ):
	mylist = file
	lines = open(os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], folder, file ) + ".mod").read().splitlines()
	index = 0
	while lines[index].startswith("%") :
		library = lines[index].split("%C")[1].split("/")[0]
		mylist = mylist + " " + getDependencyList(folder, library)  
		index = index + 1
	return mylist
# end function

# recursive function to navigate all files
def getDependencyList2 ( folder, file ):
	try:
		mylist = file
		lines = open(os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], folder, file ) + ".mod").read().splitlines()
		index = 0
		while lines[index].startswith("%") :
			library = lines[index].split("%C")[1].split("/")[0]
			mylist = mylist + " " + getDependencyList(folder, library)  
			index = index + 1
		#end while
		return mylist
	except FileNotFoundError:
		print('Aborting execution! Library file "' + file + '.mod" in folder "' + folder + '" not found.')
		sys.exit()
	#end try
# end function


print("")
print("DEFT PASCAL II VERSION 4.1")
print("COMPILE ALL MODULES - AUTOMATION SCRIPT VERSION 1.0")
print("DEVELOPED BY ANDRE BALLISTA")
print("")

parser = argparse.ArgumentParser(description="Compile the target Deft Pascal library module and all modules from which it depends.")
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
print("LIBRARY REPOSITORY FOLDER:", safepath(config["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"]))
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
print("IDENTIFYING DEPENDENCIES")
print("------------------------")
print("")

moduleList = getDependencyList2(args.folder, args.file).split(" ")
print(moduleList)
for x in reversed(moduleList):
	print(x + ".lib file exists in DSK?")
	oscommand = safepath( os.path.join(config["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
	oscommand = oscommand + " dir coco_jvc_rsdos"
	oscommand = oscommand + " " + safepath( os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, args.file) + ".dsk" )
	osresult = subprocess.run(oscommand, shell=True, stdout=subprocess.PIPE,encoding='ascii')
	if not (x in osresult.stdout):
		print ("No. Copy from repository...")
		# get source file from from repo (MOD, INT)
		sourcefile = os.path.join(config["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], x) + ".MOD"
		targetfile = os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, x) + ".MOD"
		print('copy ' + sourcefile + ' to ' + targetfile)
		shutil.copy(sourcefile,targetfile)
		sourcefile = os.path.join(config["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], x) + ".INT"
		targetfile = os.path.join(config["PROJECT SETTINGS"]["PROJECTS_HOME"], args.folder, x) + ".INT"
		shutil.copy(sourcefile,targetfile)
		#print('copy ', sourcefile, ' to ', targetfile)
#		put files (MOD, INT)in DSK
#		compile file MOD		
	#end if
#end for

# NO -> get source file from from repo (MOD, INT)
#		put files in DSK
#		compile file MOD
# YES -> skip
# compile file used in the call


print("------------------------")

