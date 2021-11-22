#!/usr/bin/env python3

# (2021) Andre Ballista

import configargparse
from dptc.dptc import DeftPascalToolChain
from dptc.dptc import LuaScript
import sys
import re


class DeftPascalCompiler(DeftPascalToolChain):

	@staticmethod
	def _default_tool_title():
		return "DPTCC - DEFT PASCAL TOOL CHAIN COMPILER - FOR DEFT PASCAL II VERSION 4.1"

	def run(self):
		self._present_script_title()
		if not self._check_source_file_requirements():
			sys.exit(1)
		dependency_list = self.process_source_code_dependencies()
		self.refresh_project_libraries(dependency_list)
		self.generate_project_file(dependency_list)
		self.list_files_present_in_project_folder()
		self._present_section_header("CREATE NEW DSK FILE")
		self._utils.create_dsk_file(self._get_dsk_file_name_from_arguments(), self._args.project_folder, self._args.emulator_folder)
		# self._present_section_header("DSK FILE CONTENTS")
		# self._utils.list_files_on_dsk(self._get_dsk_file_name_from_arguments(), self._args.project_folder, self._args.emulator_folder)
		self.refresh_dsk_with_relevant_files_for_compiling(dependency_list)
		self._present_section_header("DSK FILE CONTENTS")
		self._utils.list_files_on_dsk(self._get_dsk_file_name_from_arguments(), self._args.project_folder, self._args.emulator_folder)
		self._present_section_header("STARTING COMPILER VIA EMULATOR")
		log = self._start_emulator(LuaScript().create_compilation_script(self._args.source_file.strip().split(".")[0], self._args.project_folder, self._args.compiler_version))
		self.retrieve_object_file()
		error_count = self._retrieve_execution_log()
		if error_count > 0:
			print("\n\nCompilation failed. Errors found: {0}\n\n".format(error_count))
		else:
			print("\n\nCompilation completed. No errors found.\n\n")


if __name__ == '__main__':
	parser = configargparse.ArgParser(description="Compile the target Deft Pascal source and all modules from which it depends.",  default_config_files=["dptc.ini"])
	parser.add_argument("-source_file",  help="Source file to be compiled. File extension is required. Filepath is not needed.")
	parser.add_argument("-dsk_file", required=True, help="DSK file where the source file will be placed. File extension is not required and is assumed to be '.DSK'. Filepath is not needed.")
	parser.add_argument("--project_folder", required=True, help="Folder name where source and dsk files are located.")
	parser.add_argument("--lib_folder", required=True, help="Folder name where library files are located.")
	parser.add_argument("--compiler_disk", required=True, help="DSK file containing the DEFT PASCAL COMPILER. File extension is required. File path is not needed.")
	parser.add_argument("--compiler_folder", required=True, help="Folder name where the compiler file is located.")
	parser.add_argument("--compiler_version", required=False, choices=["3.3", "4.1"], default="3.3", type=str, help="Version of the compiler to use.")
	parser.add_argument("--emulator_folder", required=True, help="Folder name where mame emulator is installed.")
	parser.add_argument("--emulator_app", required=True, help="mame emulator executable.")
	parser.add_argument("--emulator_rom", required=True, help="rom to be used.")
	parser.add_argument("--emulator_speed", default=9, help="mame emulator speed.")
	parser.add_argument("--emulator_delay", default=3, help="mame emulator boot delay.")
	parser.add_argument("--emulator_extension", required=False, help="extension used on the emulator.")
	parser.add_argument("-type", choices=['MAIN', 'MODULE'], default='MAIN', help="Type of source file being compiled. {CODE} File is a '.PAS' code and therefore compiled as a stand-alone program. {MODULE} File is a '.MOD' code and therefore will be compiled as a library.")
	parser.add_argument("-refresh", choices=['ALL', 'ABSENT', 'NEWER', 'NONE'], default='ALL', help="Refresh option for needed library files. {ALL} All needed library files will be copied from lib_folder during the compilation process. {ABSENT} Not present files in PROJECT_FOLDER will be copied. {NEWER} Files with a newer timestamp will be copied. {NONE} The default option, no files will be copied.")
	parser.add_argument("-list", choices=['NO', 'TAIL', 'ALL'], default='TAIL', help="List the result of the compilation process. {NO} No listing is presented. {TAIL} The default option. Only the last part is presented showing the number of errors. {ALL} The full compilation result is presented.")

	dpc = DeftPascalCompiler(parser)
	dpc.run()
