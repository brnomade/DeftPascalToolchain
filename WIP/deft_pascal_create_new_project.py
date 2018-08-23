import sys
import os
import configparser
import argparse
import subprocess
import shutil
from collections import deque

def safepath( str ):
	# function to handle windows path names with empty spaces
	# in linux or ios this function is neutral
	if sys.platform.startswith('win'):
		stringcommand = '"' + str + '"'
	else:
		stringcommand = str
	return stringcommand
# end function



def getPasFileNameFromArguments( arguments ):
	# Return a PAS file name derived from the script arguments
	return arguments.file.strip().split(".")[0] + ".pas"
#end function



def getDskFileNameFromArguments( arguments ):
	# Return a DSK file name derived from the script arguments
	return arguments.file.strip().split(".")[0] + ".dsk"
#end function



def getDskFolderNameFromArguments( arguments ):
	# Return the folder name where the DSK file is located - derived from the script arguments
	return arguments.folder.strip()
#end function



def getPrjFileNameFromArguments( arguments ):
	# Return a PRJ file name derived from the script arguments
	return arguments.file.strip().split(".")[0] + ".prj"
#end function



def getLstFileNameFromArguments( arguments ):
	# Return a PRJ file name derived from the script arguments
	return arguments.file.strip().split(".")[0] + ".lst"
#end function



def copyAllFilesFromRepositoryToProjectFolder( libraryList, aConfiguration, theArguments ):
    #force the refresh of the file from repository folder into project folder
    for libFile in libraryList:
        print("... refreshing '" + libFile + "' from '" + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + "'")
        sourcefile = os.path.join(aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], libFile)
        targetfile = os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, libFile)
        try:
            shutil.copy(sourcefile,targetfile)
        except FileNotFoundError:
            print("")
            print("Aborting execution. Couldn't refresh from repository. Library file not found.")
            print('"' + libFile + '" not located in folder "' + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + '".')
            sys.exit()
        #end try
    #end for
#end function



def copyAbsentFilesFromRepositoryToProjectFolder( libraryList, aConfiguration, theArguments ):
    #refresh only the files not present in the project folder
    for libFile in libraryList :
        targetfile = os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, libFile)
        if os.path.isfile(targetfile):
                print("... refreshing '" + libFile + "' file already exists in '" + aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"] + "'")
        else:
        	print("... refreshing '" + libFile + "' from '" + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + "'")
        	sourcefile = os.path.join(aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], libFile)
        	try:
        		shutil.copy(sourcefile,targetfile)
        	except FileNotFoundError:
        		print("")
        		print("Aborting execution. Couldn't refresh from repository. Library file not found.")
        		print('"' + libFile + '" not located in folder "' + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + '".')
        		sys.exit()
        	#end try
        #end if
    #end for
#end function



def copyNewerFilesFromRepositoryToProjectFolder( libraryList, aConfiguration, theArguments ):
	#refresh only the files that are newer in the repository
	for libFile in libraryList :
		sourcefile = os.path.join(aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], libFile)
		targetfile = os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, libFile)
		try:
			older = (os.stat(targetfile).st_mtime > os.stat(sourcefile).st_mtime)
		except FileNotFoundError:
			print("")
			print("Aborting execution. Couldn't validate files. Library files not found.")
			print('"' + libFile + '" not located in folder "' + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + '"."')
			print('"' + libFile + '" not located in folder "' + aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"] + '".')
			sys.exit()
		#end try
		if older:
		    print("... refreshing '" + libFile + "' already matches the repository file located on '" + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + "'")
		else:
		    print("... refreshing '" + libFile + "' from '" + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + "'")
		    try:
			    shutil.copy(sourcefile,targetfile)
		    except FileNotFoundError:
			    print("")
			    print("Aborting execution. Couldn't refresh from repository. Library file not found.")
			    print('"' + libFile + '" not located in folder "' + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + '".')
			    sys.exit()
			#end try
		#end if
    #end for
#end function




def getDirectDependencyList( aConfiguration, theArguments ):
	# Identify all libraries used by the source code file.
	try:
		lines = open(os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, theArguments.file)).read().splitlines()
	except FileNotFoundError:
		print("Aborting execution. Source file '" + os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder.strip(), theArguments.file.strip()) + "' not found.")
		sys.exit()
	#end try
	importList = list()
	index = 0
	while lines[index].startswith("%"):
		if ("%C" in lines[index]):
			library = lines[index].split("%C")[1].split("/")[0]
			extension = lines[index].split("%C")[1].split("/")[1].split(":")[0]
			importList.append(library + "." + extension)
		#end if
		index = index + 1
	#end while
	return importList
#end function




def getDependencyList( aFileName, aConfiguration ):
	# recursive function to navigate all library files referenced by the main source file
	sourcefile = os.path.join(aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"], aFileName)
	try:
		lines = open(sourcefile).read().splitlines()
	except FileNotFoundError:
		print("")
		print("Aborting execution. Library file not found.")
		print('"' + aFileName + '" not located in "' + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + '".')
		sys.exit()
    #end try

	importList = ""
	index = 0
	while lines[index].startswith("%") :
		if ("%C" in lines[index]):
			library = lines[index].split("%C")[1].split("/")[0]
			extension = lines[index].split("%C")[1].split("/")[1].split(":")[0]
			importList = importList + " " + library + "." + extension
			importList = importList + getDependencyList(library + "." + extension, aConfiguration)
		#end if
		index = index + 1
	#end while
	return importList
#end function



def getIndirectDependencyList( aList, aConfiguration ):
	# Identify all libraries used by the libraries used by the source code file
	importList = list()
	for libFile in aList :
		for tempFile in getDependencyList(libFile, aConfiguration).strip().split():
			importList.append(tempFile)
		#end for
	#end for
	return importList
#end function



def processSourceCodeDependencies( aConfiguration, theArguments ):
	#
	presentScriptSection("PROCESSING DEPENDENCIES")
	directImportList = getDirectDependencyList( aConfiguration, theArguments )
	indirectImportList = getIndirectDependencyList( directImportList, aConfiguration )
	presentDependencies( directImportList, indirectImportList, theArguments )
	return directImportList + indirectImportList
#end function



def performRefreshParameter( libraryList, aConfiguration, theArguments ):
	# process the refresh parameter for the provided list of libraries
	if theArguments.refresh == "ALL":
		copyAllFilesFromRepositoryToProjectFolder(libraryList, aConfiguration, theArguments )
	elif theArguments.refresh == "ABSENT":
		copyAbsentFilesFromRepositoryToProjectFolder(libraryList, aConfiguration, theArguments)
	elif theArguments.refresh == "NEWER":
		copyNewerFilesFromRepositoryToProjectFolder(libraryList, aConfiguration, theArguments)
	#end if
#end function


def deleteFileInDsk( aFileName, aDskFileName, aDskFolderName, aConfiguration ):
	# Delete a aFileName from a aDskFileName located in aDskFolderName
	# Assumption is that aDskFolderName is located inside ["PROJECT SETTINGS"]["PROJECTS_HOME"]
	print("Deleting '" + aFileName + "' from '" + aDskFileName)
	oscommand = safepath( os.path.join(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
	oscommand = oscommand + " del coco_jvc_rsdos"
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], aDskFolderName, aDskFileName) )
	oscommand = oscommand + " " + aFileName
	#print(oscommand)
	if subprocess.run(oscommand, shell=True).returncode == 1 :
		print("")
		print("Aborting execution. Unable to execute Mame imgtool.")
		print('Check if imgtool is located in "' + aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] + '".')
		sys.exit()	
	#end if
	#print("")
#end function



def copyFileToDsk( aFileName, aFileFolderName, aDskFileName, aDskFolderName, aConfiguration ):
	# Copy a aFileName located in aFileFolderName to a aDskFileName located in aDskFolderName
	# Assumption is that aFileFolderName and aDskFolderName are located inside ["PROJECT SETTINGS"]["PROJECTS_HOME"]
	#print("Copying '" + aFileName + "' to '" + aDskFileName)
	oscommand = safepath( os.path.join(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
	oscommand = oscommand + " put coco_jvc_rsdos"
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], aDskFolderName, aDskFileName))
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], aFileFolderName, aFileName))
	oscommand = oscommand + " " + aFileName
	oscommand = oscommand + " --ftype=binary --filter=ascii"
	#print(oscommand)
	if subprocess.run(oscommand, shell=True).returncode == 1 :
		print("")
		print("Aborting execution. Unable to execute Mame imgtool.")
		print('Check if imgtool is located in "' + aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] + '".')
		sys.exit()	
	#end if
	print("")
#end function


def copyFileFromDsk( aFileName, aDskFileName, aDskFolderName, aConfiguration ):
	# Copy a aFileName located in dskFileName to folderName
	# Assumption is that aDskFolderName is located inside ["PROJECT SETTINGS"]["PROJECTS_HOME"]
	print ("Retrieving " + aFileName + " from " + aDskFileName)
	oscommand = safepath( os.path.join(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
	oscommand = oscommand + " get coco_jvc_rsdos"
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], aDskFolderName, aDskFileName))
	oscommand = oscommand + " " + aFileName.capitalize()
	oscommand = oscommand + " --filter=ascii"
	#print(oscommand)
	if subprocess.run(oscommand, shell=True).returncode == 1 :
		print("")
		print("Aborting execution. Unable to execute Mame imgtool.")
		print('Check if imgtool is located in "' + aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] + '".')
		sys.exit()	
	#end if
#end function



def listFilesOnDsk( aDskFileName, aConfiguration, theArguments ):
	# List the files existing in the DSK file
	presentScriptSection("DSK FILE CONTENTS")
	oscommand = safepath( os.path.join(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"], "imgtool.exe") )
	oscommand = oscommand + " dir coco_jvc_rsdos"
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, aDskFileName) )
	#print(oscommand)
	if subprocess.run(oscommand, shell=True).returncode == 1 :
		print("")
		print("Aborting execution. Unable to execute Mame imgtool.")
		print('Check if imgtool is located in "' + aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] + '".')
		sys.exit()	
	#end if
#end function




def listFilesPresentOnProjectFolder( aConfiguration, theArguments ):
	# Execute a call to the operating system to get the list of files on the project folder
	presentScriptSection("PROJECT FOLDER CONTENTS")
	if sys.platform.startswith('win'):
		dircommand = "dir"
	else:
		dircommand = "ls -la"
	oscommand = dircommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder) )
	#print(oscommand)
	if subprocess.call(oscommand, shell=True) == 1 :
		print("")
		print("Aborting execution. Unable to get folder contents.")
		print("Check if '" + dircommand + "' is valid and available on your operating system.")
		#sys.exit()
	#end try
#end function



def startMameAsynchronously( aConfiguration, theArguments ):
	# Start mame as a paralel process and running independently from the scrip
	# The execution of Mame will not block the main script.
	presentScriptSection("STARTING COCO2B VIA MAME")
	try:
		os.chdir( aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] )
	except:
		print("")
		print("Aborting execution. Unable to switch to MAME home folder.")
		print("Check if '" + aConfiguration["MAME SETTINGS"]["MAME_FOLDER"] + "' is valid and available folder in your operating system.")
		sys.exit()
	#end try
	oscommand = safepath( os.path.join(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"], "mame64.exe") )
	oscommand = oscommand + " coco2b"
	oscommand = oscommand + " -flop1 " + safepath( os.path.join(aConfiguration["DEFT SETTINGS"]["DEFT_DSK_FOLDER"], aConfiguration["DEFT SETTINGS"]["DEFT_DSK_FILE"]) )
	oscommand = oscommand + " -flop2 " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, getDskFileNameFromArguments(theArguments)))
	oscommand = oscommand + " -window -keepaspect -natural -speed " + aConfiguration["MAME SETTINGS"]["MAME_SPEED"]
	try:
		subprocess.Popen(oscommand)
	except:
		print("")
		print("Aborting execution. Unable to start MAME.")
		print("Check if 'mame64.exe' is located in '" + aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"] + "'.")
		sys.exit()
	#end try
	return oscommand	
#end function


def startAndWaitCompilationViaAutoIT( aConfiguration, theArguments ):
	# Start AUTOIT and perform the compilation steps
	# The execution of this script will wait until AutoIT is finished with its task
	presentScriptSection("STARTING DEFT PASCAL COMPILATION VIA AUTOIT") 
	oscommand = safepath( os.path.join(aConfiguration["AUTOIT SETTINGS"]["AUTOIT_FOLDER"], "autoit3.exe") )
	oscommand = oscommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], "deft_pascal_keystrokes_automation.au3"))
	oscommand = oscommand + " " + theArguments.file.strip().split(".")[0]
	print(oscommand)
	if subprocess.run(oscommand, shell=True).returncode == 1 :
		print("")
		print("Aborting execution. Unable to execute AUTOIT.")
		print('Check if autoit3.exe is located in "' + aConfiguration["AUTOIT SETTINGS"]["AUTOIT_FOLDER"] + '".')
		sys.exit()	
	#end if	
#end function



def refreshDskWithAllRelevantFiles( aDependencyList, aConfiguration, theArguments ):
	#
	presentScriptSection("REFRESHING ALL RELEVANT FILES ON DSK")
	aPasFileName = getPasFileNameFromArguments(theArguments) 
	aPrjFileName = getPrjFileNameFromArguments(theArguments) 
	aDskFileName = getDskFileNameFromArguments(theArguments) 
	#
	deleteFileInDsk( aPasFileName, aDskFileName, theArguments.folder, aConfiguration )
	copyFileToDsk( aPasFileName, theArguments.folder, aDskFileName, theArguments.folder, aConfiguration )
	#
	deleteFileInDsk( aPrjFileName, aDskFileName, theArguments.folder, aConfiguration )
	copyFileToDsk( aPrjFileName, theArguments.folder, aDskFileName, theArguments.folder, aConfiguration )
	#
	for aLibFileName in aDependencyList:
		deleteFileInDsk( aLibFileName, aDskFileName, theArguments.folder, aConfiguration )
		copyFileToDsk( aLibFileName, theArguments.folder, aDskFileName, theArguments.folder, aConfiguration )
	#end for
#end function



def retrieveCompilationLog( aConfiguration, theArguments ):
	# Retrieve the compilation .LST file from the .dsk and present it on the standard  output.
	presentScriptSection("RETRIEVING COMPILATION OUTPUT")
	
	print ("Deleting " + getLstFileNameFromArguments(theArguments) + " from project folder")

	oscommand = os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, getLstFileNameFromArguments(theArguments)) 
	try:
		os.remove(oscommand)
	except:
		print("")
		print("Warning. LST file does not seem to exist.")
		print("Check if '" + oscommand + "' is valid and available in your operating system.")
	#end try
	
	try:
		os.chdir(os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder) )
	except:
		print("")
		print("Aborting execution. Unable to switch to Project home folder.")
		print("Check if '" + os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder) + "' is valid and available folder in your operating system.")
		sys.exit()	
	#end try

	copyFileFromDsk( getLstFileNameFromArguments(theArguments), getDskFileNameFromArguments(theArguments), getDskFolderNameFromArguments(theArguments), aConfiguration )

	if theArguments.list == "TAIL":
		lstFileName = os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, getLstFileNameFromArguments(theArguments))
		try:
			lstFile = open(lstFileName)
		except FileNotFoundError:
			print("")
			print("Aborting execution. File not found.")
			print("The LST file '" + lstFileName + "' was not found.")
			sys.exit()
		#end try
		with lstFile as f:
			try:
				print( deque(f, 10) )
			except:
				print("")
				print("Warning. LST file is unreadable.")
				print("The LST file '" + lstFileName + "' is unreadable and appears to be corrupted.")
			#end try	
	elif theArguments.list == "ALL":
		if sys.platform.startswith('win'):
			typecommand = "type"
		else:
			typecommand = "cat"
		oscommand = typecommand + " " + safepath( os.path.join(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"], theArguments.folder, getLstFileNameFromArguments(theArguments)) ) 
		#print(oscommand)
		if subprocess.run(oscommand, shell=True).returncode == 1 :
			print("")
			print("Aborting execution. Unable to output .LST file to the standard output.")
			print("Check if '" + oscommand + "' is valid and viable in your operating system.")
			sys.exit()	
		#end if	
	#end if
#end function



def initialiseScriptArgumentsParser():
	# Initialise the arguments parser
	parser = argparse.ArgumentParser(description="Create a new Deft Pascal project structure and template source files.")
	parser.add_argument("file",help="Deft Pascal source file name to be compiled. File extension is required. Filepath is not needed as the location of the file is derived from the configuration (ini) file.")
	parser.add_argument("folder",help="Folder name where the source file is located. Folder is assumed to be under the PROJECTS_HOME folder defined in the configuration (ini) file.")
	parser.add_argument("-refresh", choices=['ALL','ABSENT','NEWER','NONE'],default='NONE',help="Refresh option for needed library files. {ALL} All needed library files will be copied from REPOSITORY_FOLDER to PROJECT_FOLDER during the compilation process. {ABSENT} Inexisting files in PROJECT_FOLDER will be copied from REPOSITORY_FOLDER. {NEWER} Files with a newer timestamp in REPOSITORY_FOLDER will be copied to PROJECT_FOLDER. {NONE} The default option, no files will be copied. Folder locations are defined in the configuration (ini) file.")
	parser.add_argument("-list", choices=['NO','TAIL','ALL'],default='TAIL',help="List the result of the compilation process. {NO} No listing is presented. {TAIL} The default option. Only the last part is presented showing the number of errors. {ALL} The full compilation result is presented.")
	return parser
#end function



def initialisedScriptConfigurationParser():
	# Initialise the configuration parser
	config = configparser.ConfigParser()
	config.read("deft_pascal_toolchain_configuration.ini")
	return config
#end function


def presentScriptSection( sectionName ):
	# present a section
	print("")
	print("------------------------")
	print(sectionName.upper())
	print("------------------------")
	print("")
#end function


def presentScriptTitle():
	# present the title
	print("------------------------")
	print("DEFT PASCAL II VERSION 4.1")
	print("CREATE NEW PROJECT - AUTOMATION SCRIPT VERSION 1.0")
	print("DEVELOPED BY ANDRE BALLISTA")
	print("FOR TANDY TRSCOLOR COMPUTERS")
#end function


def presentScriptSettings( aConfiguration, theArguments ):
	# present the settings
	presentScriptSection("SETTINGS")
	try:
		print("DEFT PASCAL DSK FOLDER:", safepath(aConfiguration["DEFT SETTINGS"]["DEFT_DSK_FOLDER"]))
		print("DEFT PASCAL DSK FILE:", aConfiguration["DEFT SETTINGS"]["DEFT_DSK_FILE"])
		print("PROJECTS HOME:", safepath(aConfiguration["PROJECT SETTINGS"]["PROJECTS_HOME"]))
		print("PROJECT FOLDER:", theArguments.folder)
		print("PROJECT SOURCE:", theArguments.file)
		print("LIBRARY REPOSITORY FOLDER:", safepath(aConfiguration["REPOSITORY SETTINGS"]["REPOSITORY_FOLDER"]))
		print("MAME FOLDER:", safepath(aConfiguration["MAME SETTINGS"]["MAME_FOLDER"]))
		print("AUTOIT FOLDER:", safepath(aConfiguration["AUTOIT SETTINGS"]["AUTOIT_FOLDER"]))
		print("REFRESH OPTION:",theArguments.refresh)
	except:
		print("")
		print("Aborting execution. Unable to find configuration file.")
		sys.exit()	
	#end try
#end function


def presentDependencies( directImport, indirectImport, theArguments ):
	# present the dependencies
	print("File '" + theArguments.file + "' directly uses following libraries:", directImport)
	print("File '" + theArguments.file + "' indirectly uses following libraries:", indirectImport)
	print("")
#end function




# SCRIPT BEGIN
presentScriptTitle()
inputArguments = initialiseScriptArgumentsParser().parse_args()

aConfiguration = initialisedScriptConfigurationParser()
presentScriptSettings(aConfiguration, inputArguments)
dependecyList = processSourceCodeDependencies( aConfiguration, inputArguments )
performRefreshParameter( dependecyList, aConfiguration, inputArguments )
listFilesPresentOnProjectFolder( aConfiguration, inputArguments )
refreshDskWithAllRelevantFiles( dependecyList, aConfiguration, inputArguments )
listFilesOnDsk( getDskFileNameFromArguments( inputArguments ), aConfiguration, inputArguments )
print( startMameAsynchronously( aConfiguration, inputArguments) )
startAndWaitCompilationViaAutoIT(aConfiguration, inputArguments)
retrieveCompilationLog( aConfiguration, inputArguments )
presentScriptSection("SCRIPT COMPLETED.")
# SCRIPT ENDS
