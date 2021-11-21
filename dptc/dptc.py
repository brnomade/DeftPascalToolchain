# (2021) Andre Ballista

import sys
import os
import subprocess
import shutil
from string import Template


class LuaScript:

    @staticmethod
    def create_lua_script(template, substitutions, output_name, output_location):
        src = Template(template)
        result = src.substitute(substitutions)
        filename = "{0}.lua".format(output_name)
        f = open(os.path.join(output_location, filename), "w")
        f.write(result)
        f.close()
        return filename

    def create_compilation_script(self, source_name, project_folder):
        return self.create_lua_script(LuaTemplate.compile_script(),
                                      {"SOURCE": source_name, "OBJECT": source_name, "LIST": source_name},
                                      source_name,
                                      project_folder)

    def create_linking_script(self, source_name, project_folder):
        return self.create_lua_script(LuaTemplate.link_script(),
                                      {"SOURCE": source_name, "EXEC": source_name, "LIST": source_name},
                                      source_name,
                                      project_folder)


class LuaTemplate:

    @classmethod
    def link_script(cls):
        return """
        current_position = 1
        positions = {145, 177, 209, 241, 273, 305}
        inputs = {"{ENTER}", "$LIST/LST:1{ENTER}", "$EXEC/BIN:1{ENTER}", "Y{ENTER}", "N{ENTER}", "$SOURCE/PRJ:1{ENTER}"}
        
        function cursor_location()
            cpu = manager.machine.devices[":maincpu"]
            mem = cpu.spaces["program"]
            return 256 * mem:read_u8(136) + mem:read_u8(137) - 1024
        end
        
        function on_frame_event()
            if (current_position > 6) then
                emu.register_frame_done(nil, "frame")
                print("linkage completed")
                manager.machine:exit()
            end
            if (cursor_location() == positions[current_position]) then
                keyboard = manager.machine.natkeyboard
                coco:post_coded(inputs[current_position])
                current_position = current_position + 1
            end
        end
        
        emu.register_frame_done(on_frame_event, "frame")
        coco = manager.machine.natkeyboard
        coco:post_coded("LOADM{QUOTE}LINKER{QUOTE}:EXEC{ENTER}")
        """

    @classmethod
    def compile_script(cls):
        return """
        current_position = 1
        positions = {137, 169, 201, 233, 268, 352}
        inputs = {"$SOURCE/PAS:1{ENTER}", "$OBJECT/OBJ:1{ENTER}", "$LIST/LST:1{ENTER}", "N{ENTER}", "{ENTER}"}
        
        function cursor_location()
            cpu = manager.machine.devices[":maincpu"]
            mem = cpu.spaces["program"]
            return 256 * mem:read_u8(136) + mem:read_u8(137) - 1024
        end
        
        function on_frame_event()
            if (current_position > 6) then
                emu.register_frame_done(nil, "frame")
                print("compilation completed")
                manager.machine:exit()
            end
            if (cursor_location() == positions[current_position]) then
                keyboard = manager.machine.natkeyboard
                coco:post_coded(inputs[current_position])
                current_position = current_position + 1
            end
        end
        
        emu.register_frame_done(on_frame_event, "frame")
        coco = manager.machine.natkeyboard
        coco:post_coded("LOADM{QUOTE}PASCAL{QUOTE}:EXEC{ENTER}")
        """


class ToolChainUtils:

    def create_dsk_file(self, dsk_file_name, dsk_folder_name, emulator_folder_name):
        # Create an empty dsk_file_name located in dsk_folder_name
        print("Creating '{0}' in '{1}'".format(dsk_file_name, dsk_folder_name))
        oscommand = "{0} {1} {2} {3}".format(self.safepath(os.path.join(emulator_folder_name, "imgtool.exe")),
                                             "create",
                                             "coco_jvc_rsdos",
                                             self.safepath(os.path.join(dsk_folder_name, dsk_file_name)))
        try:
            subprocess.run(oscommand, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as error:
            print("\nAborting execution. Unable to execute Mame imgtool.")
            print("Check if imgtool is located in '{0}'.".format(emulator_folder_name))
            sys.exit(1)

    def delete_file_in_dsk(self, file_name, dsk_file_name, dsk_folder_name, emulator_folder_name):
        # Delete a file_name from a dsk_file_name located in dsk_folder_name
        print("Deleting '{0}' in '{1}' from '{2}'".format(file_name, dsk_file_name, dsk_folder_name))
        oscommand = self.safepath(os.path.join(emulator_folder_name, "imgtool.exe"))
        oscommand = oscommand + " del coco_jvc_rsdos"
        oscommand = oscommand + " " + self.safepath(os.path.join(dsk_folder_name, dsk_file_name))
        oscommand = oscommand + " " + file_name
        try:
            subprocess.run(oscommand, shell=True, check=True, capture_output=True)
        except subprocess.CalledProcessError as error:
            if file_name in error.stderr.decode():
                print("\nWarning: file '{0}' not found in {1}".format(file_name, dsk_file_name))
            else:
                print("\nAborting execution. Unable to execute Mame imgtool.")
                print("Check if imgtool is located in '{0}'.".format(emulator_folder_name))
                sys.exit(1)

    def copy_file_to_dsk(self, file_name, file_folder_name, dsk_file_name, dsk_folder_name, emulator_folder_name):
        # Copy a file_name located in file_folder_name to a dsk_file_name located in dsk_folder_name
        print("Copying '{0}' to '{1}' in '{2}'".format(file_name, dsk_file_name, dsk_folder_name))
        if not os.path.isfile(os.path.join(file_folder_name, file_name)):
            print("\nAborting execution. File '{0}' not found in {1}".format(file_name, file_folder_name))
            sys.exit(1)
        else:
            oscommand = self.safepath(os.path.join(emulator_folder_name, "imgtool.exe"))
            oscommand = oscommand + " put coco_jvc_rsdos"
            oscommand = oscommand + " " + self.safepath(os.path.join(dsk_folder_name, dsk_file_name))
            oscommand = oscommand + " " + self.safepath(os.path.join(file_folder_name, file_name))
            oscommand = oscommand + " " + file_name
            oscommand = oscommand + " --ftype=binary --filter=ascii"
            try:
                subprocess.run(oscommand, shell=True, check=True)
            except subprocess.CalledProcessError as error:
                if file_name in error.stderr.decode():
                    print("\nWarning: file '{0}' not found".format(file_name))
                else:
                    print("\nAborting execution. Unable to execute Mame imgtool.")
                    print("Check if imgtool is located in '{0}'.".format(emulator_folder_name))
                    sys.exit(1)

    def list_files_on_dsk(self, dsk_file_name, dsk_folder_name, emulator_folder_name):
        # List the files existing in the dsk_file_name located in dsk_folder_name
        oscommand = self.safepath(os.path.join(emulator_folder_name, "imgtool.exe"))
        oscommand = oscommand + " dir coco_jvc_rsdos"
        oscommand = oscommand + " " + self.safepath(os.path.join(dsk_folder_name, dsk_file_name))
        try:
            subprocess.run(oscommand, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("\nAborting execution. Unable to execute Mame imgtool.")
            print("Check if imgtool is located in '{0}'.".format(emulator_folder_name))
            sys.exit(1)

    def copy_file_from_dsk(self, file_name, dsk_file_name, dsk_folder_name, emulator_folder_name):
        # Copy a file_name from dsk_file_name to dsk_folder_name to file_folder_name
        # Assumption is that aDskFolderName is located inside ["PROJECT SETTINGS"]["PROJECTS_HOME"]
        print("Retrieving '{0}' from '{1}' in '{2}'".format(file_name, dsk_file_name, dsk_folder_name))
        oscommand = self.safepath(os.path.join(emulator_folder_name, "imgtool.exe"))
        oscommand = oscommand + " get coco_jvc_rsdos"
        oscommand = oscommand + " " + self.safepath(os.path.join(dsk_folder_name, dsk_file_name))
        oscommand = oscommand + " " + file_name.capitalize()
        oscommand = oscommand + " --filter=ascii"
        # print(oscommand)
        try:
            subprocess.run(oscommand, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("\nAborting execution. Unable to execute Mame imgtool.")
            print("Check if imgtool is located in '{0}'".format(emulator_folder_name))
            sys.exit(1)

    @staticmethod
    def safepath(str_path):
        # function to handle windows path names with empty spaces
        # in linux or ios this function is neutral
        if sys.platform.startswith('win'):
            return '"{0}"'.format(str_path)
        else:
            return str_path


class DeftPascalToolChain:

    _glb_default_separator = "------------------------"
    _glb_default_copyright = "DEVELOPED BY ANDRE BALLISTA"

    def __init__(self, input_parser):
        self._parser = input_parser
        self._args = input_parser.parse_args()
        self._utils = ToolChainUtils()
        self._lua_pascal_script = "_pascal.lua".format(self._args.source_file.strip().split(".")[0])

    @staticmethod
    def _default_tool_title():
        raise NotImplementedError("Must be implemented by subclass")

    @staticmethod
    def _present_section_header(a_section_title):
        print("\n{0}\n{1}\n{0}".format(DeftPascalToolChain._glb_default_separator, a_section_title.upper()))

    def _present_script_title(self):
        print("\n{0}\n{1}\n{2}\n{0}\n".format(DeftPascalToolChain._glb_default_separator,
                                              self._default_tool_title(),
                                              DeftPascalToolChain._glb_default_copyright))
        print(self._parser.format_values())

    def _check_source_file_requirements(self):

        if self._args.source_file.count(".") != 1:
            # extension is present
            print("\nAborting execution. {0}.".format("Source filename must have an extension"))
            return False
        elif len(self._args.source_file.split(".")[1]) > 3:
            # extension is max 3 length
            print("\nAborting execution. {0}.".format("Maximum extension length exceeded"))
            return False
        elif len(self._args.source_file.split(".")[0]) > 8:
            # filename is max 8 length
            print("\nAborting execution. {0}.".format("Maximum filename length exceeded"))
            return False
        else:
            return True

    def _check_object_file_requirements(self):
        if not os.path.isfile(os.path.join(self._args.project_folder, self._get_obj_file_name_from_arguments())):
            # object file must exist
            print(os.path.join(self._args.project_folder, self._get_obj_file_name_from_arguments()))
            print("\nAborting execution. {0}.".format("Object filename not found"))
            return False
        else:
            return True

    def _navigate_dependency_list(self, a_file_name):
        # recursive function to navigate all library files referenced by the main source file
        sourcefile = os.path.join(self._args.lib_folder, a_file_name)
        try:
            lines = open(sourcefile).read().splitlines()
        except FileNotFoundError:
            # file was not found on the library repository, will try to find it on the project folder instead
            sourcefile = os.path.join(self._args.project_folder, a_file_name)
            try:
                lines = open(sourcefile).read().splitlines()
            except FileNotFoundError:
                print("\nAborting execution. Library file not found.\n")
                print("'{0}' not located in '{1}' or '{2}'".format(a_file_name, self._args.lib_folder, self._args.project_folder))
                sys.exit(1)
        import_list = ""
        index = 0
        while lines[index].startswith("%"):
            if "%C" in lines[index]:
                library = lines[index].split("%C")[1].split("/")[0]
                extension = lines[index].split("%C")[1].split("/")[1].split(":")[0]
                import_list = import_list + " " + library + "." + extension
                import_list = import_list + self._navigate_dependency_list(library + "." + extension)
            index = index + 1
        return import_list

    def _get_direct_dependency_list(self):
        # Identify all libraries used by the source code file.
        try:
            lines = open(os.path.join(self._args.project_folder, self._args.source_file)).read().splitlines()
        except FileNotFoundError:
            print("\nAborting execution. Source file '{0}' not found.".format(os.path.join(self._args.project_folder.strip(), self._args.source_file.strip())))
            sys.exit(1)
        import_list = list()
        index = 0
        while lines[index].startswith("%"):
            if "%C" in lines[index]:
                library = lines[index].split("%C")[1].split("/")[0]
                extension = lines[index].split("%C")[1].split("/")[1].split(":")[0]
                import_list.append(library + "." + extension)
            index = index + 1
        return import_list

    def _get_indirect_dependency_list(self, a_list):
        # Identify all libraries used by the libraries used by the source code file
        import_list = list()
        for libFile in a_list:
            for tempFile in self._navigate_dependency_list(libFile).strip().split():
                import_list.append(tempFile)
        return import_list

    def _present_dependencies(self, direct_import, indirect_import):
        print("File '{0}' directly imports: {1}".format(self._args.source_file, direct_import))
        print("File '{0}' indirectly imports: {1}".format(self._args.source_file, indirect_import))

    def process_source_code_dependencies(self):
        self._present_section_header("PROCESSING DEPENDENCIES")
        direct_import_list = self._get_direct_dependency_list()
        indirect_import_list = self._get_indirect_dependency_list(direct_import_list)
        self._present_dependencies(direct_import_list, indirect_import_list)
        return direct_import_list + indirect_import_list

    def _copy_all_files_from_library_to_project_folder(self, library_list):
        # force the refresh of the file from repository folder into project folder
        for lib_file in library_list:
            print("... refreshing '{0}' from '{1}'".format(lib_file, self._args.lib_folder))
            source_file = os.path.join(self._args.lib_folder, lib_file)
            target_file = os.path.join(self._args.project_folder, lib_file)
            try:
                shutil.copy(source_file, target_file)
            except FileNotFoundError:
                print("\nAborting execution. Couldn't refresh from repository. Library file not found.")
                print("'{0}' not found in '{1}'".format(lib_file, self._args.lib_folder))
                sys.exit()

    def _copy_absent_files_from_library_to_project_folder(self, library_list):
        # refresh only the files not present in the project folder
        for lib_file in library_list:
            target_file = os.path.join(self._args.project_folder, lib_file)
            if os.path.isfile(target_file):
                print("Copying '{0}' ... file already exists in '{1}'".format(lib_file, self._args.project_folder))
            else:
                print("Copying '{0}' ... from '{1}'".format(lib_file, self._args.lib_folder))
                source_file = os.path.join(self._args.lib_folder, lib_file)
                try:
                    shutil.copy(source_file, target_file)
                except FileNotFoundError:
                    print("\nAborting execution. Couldn't refresh from repository. Library file not found.")
                    print("'{0}' not found in '{1}'".format(lib_file, self._args.lib_folder))
                    sys.exit(1)

    def _copy_newer_files_from_library_to_project_folder(self, library_list):
        # refresh only the files that are newer in the repository
        for lib_file in library_list:
            source_file = os.path.join(self._args.lib_folder, lib_file)
            target_file = os.path.join(self._args.project_folder, lib_file)
            try:
                older = (os.stat(target_file).st_mtime > os.stat(source_file).st_mtime)
            except FileNotFoundError:
                print("\nAborting execution. Couldn't validate files. Library file not found.")
                print("'{0}' not found in '{1}'.".format(lib_file, self._args.lib_folder))
                print("'{0}' not found in '{1}'.".format(lib_file, self._args.project_folder))
                sys.exit(1)
            if older:
                print("'{0}' already matches the repository file on '{0}'.".format(lib_file, self._args.lib_folder))
            else:
                print("Copying '{0}' from '{1}'.".format(lib_file, self._args.lib_folder))
                try:
                    shutil.copy(source_file, target_file)
                except FileNotFoundError:
                    print("\nAborting execution. Couldn't refresh from repository. Library file not found.")
                    print("'{0}' not found in '{1}'.".format(lib_file, self._args.lib_folder))
                    sys.exit(1)

    def refresh_project_libraries(self, library_list):
        # process the refresh parameter for the provided list of libraries
        if self._args.refresh == "ALL":
            self._copy_all_files_from_library_to_project_folder(library_list)
        elif self._args.refresh == "ABSENT":
            self._copy_absent_files_from_library_to_project_folder(library_list)
        elif self._args.refresh == "NEWER":
            self._copy_newer_files_from_library_to_project_folder(library_list)
        else:
            print("No libraries refreshed.")

    def generate_project_file(self, dependency_list):
        self._present_section_header("GENERATE PROJECT FILE")
        particle = "{0}/OBJ:1"
        with open(os.path.join(self._args.project_folder, self._get_prj_file_name_from_arguments()), 'w') as f:
            temp_name = particle.format(self._get_source_file_name_from_arguments().replace(".pas", ""))
            f.write(temp_name)
            print("including '{0}' as '{1}'".format(self._get_source_file_name_from_arguments(), temp_name))
            for filename in dependency_list:
                temp_name = particle.format(filename)
                f.write(temp_name)
                print("including '{0}' as '{1}'".format(filename, temp_name))

    def list_files_present_in_project_folder(self):
        # Execute a call to the operating system to get the list of files on the project folder
        self._present_section_header("PROJECT FOLDER CONTENTS")
        if sys.platform.startswith('win'):
            dir_command = "dir"
        else:
            dir_command = "ls -la"
        os_command = dir_command + " " + self._utils.safepath(os.path.join(self._args.project_folder))
        try:
            subprocess.run(os_command, shell=True, check=True)
        except subprocess.CalledProcessError:
            print("\nAborting execution. Unable to get folder contents.")
            print("Check if '{0}' is valid and available on your operating system.".format(dir_command))
            sys.exit(1)

    def _get_source_file_name_from_arguments(self):
        # Return a source file name derived from the script arguments
        if self._args.type.strip() == "MAIN":
            extension = ".pas"
        elif self._args.type.strip() == "MODULE":
            extension = ".mod"
        else:
            extension = ".pas"
        return self._args.source_file.strip().split(".")[0] + extension

    def _get_obj_file_name_from_arguments(self):
        # Return an object file name derived from the script arguments
        if self._args.type.strip() == "MAIN":
            extension = "OBJ"
        elif self._args.type.strip() == "MODULE":
            extension = "LIB"
        else:
            extension = "OBJ"
        return "{0}.{1}".format(self._args.source_file.strip().split(".")[0], extension)

    def _get_prj_file_name_from_arguments(self):
        # Return a PRJ file name derived from the script arguments
        return "{0}.PRJ".format(self._args.source_file.strip().split(".")[0])

    def _get_bin_file_name_from_arguments(self):
        # Return a BIN file name derived from the script arguments
        return "{0}.BIN".format(self._args.source_file.strip().split(".")[0])

    def _get_dsk_file_name_from_arguments(self):
        # Return a DSK file name derived from the script arguments
        return "{0}.dsk".format(self._args.dsk_file.strip().split(".")[0])

    def _get_lst_file_name_from_arguments(self):
        # Return a PRJ file name derived from the script arguments
        return "{0}.LST".format(self._args.source_file.strip().split(".")[0])

    def _get_dsk_folder_name_from_arguments(self):
        # Return the folder name where the DSK file is located - derived from the script arguments
        return self._args.project_folder.strip()

    def refresh_dsk_with_relevant_files_for_compiling(self, a_dependency_list):
        self._present_section_header("REFRESHING DSK FILE")

        source_file_name = self._get_source_file_name_from_arguments()
        # prj_file_name = self._get_prj_file_name_from_arguments()
        a_dsk_file_name = self._get_dsk_file_name_from_arguments()
        # lst_file_name = self._get_lst_file_name_from_arguments()
        # obj_file_name = self._get_obj_file_name_from_arguments()

        # refresh the source file
        self._utils.delete_file_in_dsk(source_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
        self._utils.copy_file_to_dsk(source_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # refresh the prj file
        # self._utils.delete_file_in_dsk(prj_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
        # if a_dependency_list:
        #    self._utils.copy_file_to_dsk(prj_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # refresh all libraries
        for a_lib_file_name in a_dependency_list:
            self._utils.delete_file_in_dsk(a_lib_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
            self._utils.copy_file_to_dsk(a_lib_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # delete the lst file
        # self._utils.delete_file_in_dsk(lst_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # delete the obj file
        # self._utils.delete_file_in_dsk(obj_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

    def refresh_dsk_with_relevant_files_for_linking(self, a_dependency_list):
        self._present_section_header("REFRESHING DSK FILE")
        # source_file_name = self._get_source_file_name_from_arguments()
        prj_file_name = self._get_prj_file_name_from_arguments()
        a_dsk_file_name = self._get_dsk_file_name_from_arguments()
        lst_file_name = self._get_lst_file_name_from_arguments()
        obj_file_name = self._get_obj_file_name_from_arguments()

        # refresh the source file
        # self._utils.delete_file_in_dsk(source_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
        # self._utils.copy_file_to_dsk(source_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # refresh the prj file
        self._utils.delete_file_in_dsk(prj_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
        self._utils.copy_file_to_dsk(prj_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # refresh the OBJ file
        self._utils.delete_file_in_dsk(obj_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
        self._utils.copy_file_to_dsk(obj_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # refresh all libraries
        # TODO: Here it needs to refresh the OBJ files
        for a_lib_file_name in a_dependency_list:
            self._utils.delete_file_in_dsk(a_lib_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)
            self._utils.copy_file_to_dsk(a_lib_file_name, self._args.project_folder, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

        # delete the lst file
        self._utils.delete_file_in_dsk(lst_file_name, a_dsk_file_name, self._args.project_folder, self._args.emulator_folder)

    def _start_emulator(self, boot_script_file):
        # Start mame as a parallel process and running independently from the script
        # The execution of Mame will not block the main script.
        try:
            os.chdir(self._args.emulator_folder)
        except:
            print("\nAborting execution. Unable to switch to emulator home folder.")
            print("Check if '{0}' is valid and available folder in your operating system.".format(self._args.emulator_folder))
            sys.exit(1)
        oscommand = self._utils.safepath(os.path.join(self._args.emulator_folder, self._args.emulator_app))
        oscommand = oscommand + " " + self._args.emulator_rom
        oscommand = oscommand + ' -window -keepaspect -natural -console -skip_gameinfo'
        oscommand = oscommand + " -flop1 " + self._utils.safepath(os.path.join(self._args.compiler_folder, self._args.compiler_disk))
        oscommand = oscommand + " -flop2 " + self._utils.safepath(os.path.join(self._args.project_folder, self._get_dsk_file_name_from_arguments()))
        oscommand = oscommand + " -speed {0}".format(self._args.emulator_speed)
        if self._args.emulator_extension:
            oscommand = oscommand + " -ext {0}".format(self._args.emulator_extension)
        oscommand = oscommand + " -autoboot_delay {0}".format(self._args.emulator_delay)
        oscommand = oscommand + " -autoboot_script " + os.path.join(self._args.project_folder, boot_script_file)
        try:
            subprocess.run(oscommand)
        except:
            print("\nAborting execution. Unable to start emulator.")
            print("Check if '{0}' is located in '{1}'.".format(self._args.emulator_app, self._args.compiler_folder))
            sys.exit(1)
        return oscommand

    def retrieve_object_file(self):
        # retrieve the object .OBJ file resulting from the compilation process
        self._present_section_header("RETRIEVING OBJECT FILE")
        print("Deleting '{0}' from '{1}'".format(self._get_obj_file_name_from_arguments(), self._args.project_folder))
        oscommand = os.path.join(self._args.project_folder, self._get_obj_file_name_from_arguments())
        try:
            os.remove(oscommand)
        except:
            print("Warning. '{0}' not found in '{1}'.".format(self._get_obj_file_name_from_arguments(),
                                                              self._args.project_folder))

        try:
            os.chdir(os.path.join(self._args.project_folder))
        except:
            print("\nAborting execution. Unable to switch to Project folder '{0}'.".format(self._args.project_folder))
            print("Check if '{0}' is valid and present in your operating system.".format(self._args.project_folder))
            sys.exit(1)

        self._utils.copy_file_from_dsk(self._get_obj_file_name_from_arguments(), self._get_dsk_file_name_from_arguments(), self._get_dsk_folder_name_from_arguments(), self._args.emulator_folder)

    def retrieve_executable_file(self):
        # retrieve the executable .BIN file resulting from the linking process
        self._present_section_header("RETRIEVING EXECUTABLE FILE")
        print("Deleting '{0}' from '{1}'".format(self._get_bin_file_name_from_arguments(), self._args.project_folder))
        oscommand = os.path.join(self._args.project_folder, self._get_bin_file_name_from_arguments())
        try:
            os.remove(oscommand)
        except:
            print("Warning. '{0}' not found in '{1}'.".format(self._get_bin_file_name_from_arguments(),
                                                              self._args.project_folder))

        try:
            os.chdir(os.path.join(self._args.project_folder))
        except:
            print("\nAborting execution. Unable to switch to Project folder '{0}'.".format(self._args.project_folder))
            print("Check if '{0}' is valid and present in your operating system.".format(self._args.project_folder))
            sys.exit(1)

        self._utils.copy_file_from_dsk(self._get_bin_file_name_from_arguments(), self._get_dsk_file_name_from_arguments(), self._get_dsk_folder_name_from_arguments(), self._args.emulator_folder)

    def _retrieve_execution_log(self):
        # Retrieve the execution .LST file from the .dsk and present it on the standard output.
        self._present_section_header("RETRIEVING EXECUTION OUTPUT LOG")
        print("Deleting '{0}' from '{1}'".format(self._get_lst_file_name_from_arguments(), self._args.project_folder))
        oscommand = os.path.join(self._args.project_folder, self._get_lst_file_name_from_arguments())
        try:
            os.remove(oscommand)
        except:
            print("Warning. '{0}' not found in '{1}'.".format(self._get_lst_file_name_from_arguments(),
                                                              self._args.project_folder))

        try:
            os.chdir(os.path.join(self._args.project_folder))
        except:
            print("\nAborting execution. Unable to switch to Project folder '{0}'.".format(self._args.project_folder))
            print("Check if '{0}' is valid and present in your operating system.".format(self._args.project_folder))
            sys.exit(1)

        self._utils.copy_file_from_dsk(self._get_lst_file_name_from_arguments(), self._get_dsk_file_name_from_arguments(), self._get_dsk_folder_name_from_arguments(), self._args.emulator_folder)

        lst_filename = os.path.join(self._args.project_folder, self._get_lst_file_name_from_arguments())
        try:
            with open(lst_filename) as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("\nAborting execution. File not found.")
            print("LST file '{0}' was not found.".format(lst_filename))
            sys.exit(1)

        if self._args.list == "TAIL":
            print(lines[-3:])
        elif self._args.list == "ALL":
            if sys.platform.startswith('win'):
                typecommand = "type"
            else:
                typecommand = "cat"
            oscommand = typecommand + " " + os.path.join(self._args.project_folder, self._get_lst_file_name_from_arguments())
            # print(oscommand)
            if subprocess.run(oscommand, shell=True).returncode == 1:
                print("\nAborting execution. Unable to output .LST file to the standard output.")
                print("Check if '{0}' is valid and viable in your operating system.".format(oscommand))
                sys.exit(1)
