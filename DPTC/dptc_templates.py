# (2021) Andre Ballista

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