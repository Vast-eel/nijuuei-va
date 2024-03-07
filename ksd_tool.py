import os
import sys
import struct
import unicodedata

def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256

class KageScriptData:
    file_name = ""
    file_size = 0

    opcodes = (
                # -- Text --
                (0x0100, 'HH', "line_set"),
                (0x0200, 'H', "name_set"),
                (0x0300, '', "name_clear"),
                (0x0400, 'HH', "pis_set"),
                (0x0500, '', "nvl_line_clear"),
                (0x0600, 'IH', "jump_choice"),
                (0x0700, 'I', "jump_auto"),
                (0x0800, '', "nvl_on"),
                (0x0900, '', "adv_on"),
                (0x0A00, 'H', "ksd_set"),
                (0x0B00, '', "ecchi_end"),
                (0x0C00, '', "game_over"),
                (0x0D00, '', "ksd_end"),
                
                # -- Graphics --
                # Layer 1: Fullscreen backgrounds/CGs
                (0x0E00, 'hh', "kgd_layer1_set"),
                (0x0F00, '', "kgd_layer1_display"),
                (0x1000, '', "kgd_layer1_blackout"),
                (0x1100, 'h', "kgd_layer1_clear"),
                (0x1200, '', "kgd_layer1_fadein"),
                
                # Layer 2: Smaller elements (island backgrounds, textbox, etc)
                (0x1300, 'hh', "kgd_layer2_set"),
                (0x1400, '', "kgd_layer2_display"),
                (0x1500, '', "kgd_layer2_clear"),
                (0x1600, 'h', "kgd_layer2_fade_unk"),
                (0x1700, '', "kgd_layer2_fadein"),
                
                # Layer 3: Character sprites
                (0x1800, 'hh', "kgd_layer3_set"),
                (0x1900, 'HiiiiII', "kgd_layer3_param"),
                (0x1A00, 'h', "kgd_layer3_display"),
                (0x1B00, 'h', "kgd_layer3_fadeout"),
                (0x1C00, 'h', "kgd_layer3_clear"),
                
                # Blitting?
                # 002.ksd at 0x3330
                (0x1D00, 'hh', "kgd_layer1_blit"), #kgd_layer1_fade_solid
                (0x1E00, 'hh', "kgd_layer2_blit"),
                
                # -- Progression flags --
                # 0 = sae, 1 = fuurei, 4 = kikyou, 5 = mikoto
                (0x1F00, 'h', "section_jump_branch1"),
                (0x2000, 'h', "section_jump_branch2"),
                (0x2100, 'h', "gallery_unlock"),
                #(0x2200, '', "unused?"),
                (0x2300, 'IH', "jump_branch1"),
                (0x2400, 'IH', "jump_branch2"),
                (0x2500, 'h', "affection_plus"),
                (0x2600, 'h', "affection_minus"), 
                (0x2700, 'h', "affection_ecchi"), # used only in 036 for mikoto
                (0x2800, 'hh', "route_confirm"), # used only in 038
                (0x2900, 'IH', "jump_route_038"), # used only in 038
                #(0x2A00, '', "unused?"),
                (0x2B00, 'IHIH', "jump_route_036"), # another mikoto-only flag
                #(0x2C00, '', "unused?"),
                #(0x2D00, '', "unused?"),
                #(0x2E00, '', "unused?"),
                (0x2F00, 'IHIH', "jump_route"),
                
                # -- Audio --
                (0x3000, 'h', "music_play"),
                (0x3100, '', "music_stop"),
                #(0x3200, '', "unused?") - crash with a message about CD, music related?
                #(0x3300, '', "unused?"),
                (0x3400, 'hh', "sfx_set"),
                (0x3500, 'h', "sfx_play"),
                (0x3600, 'h', "sfx_loop1"),
                (0x3700, 'h', "sfx_loop2"),
                (0x3800, 'h', "sfx_stop"),
                
                # -- Graphical effects --
                (0x3900, 'h', "kgd_layer1_crossfade"),
                (0x3A00, 'h', "kgd_layer2_crossfade"),
                (0x3B00, 'h', "kgd_layer3_crossfade"),
                (0x3C00, 'h', "kgd_layer1_fx"), # 5 = screenshake?
                
                # -- Other --
                (0x3D00, '', "fight_end"), # enables saving
                (0x3E00, '', "fight_start"), # disables saving
                (0x3F00, 'I', "jump_fight_failure"),                
                (0x4000, '', "op_play"),
                (0x4100, 'h', "anim_play"),
                (0x4200, '', "game_clear"),
                (0x4300, '', "force_save_menu"),
                (0x4400, 'I', "wait"))

    commands = []
    args = []

    jump_opcodes = (
                0x0600,
                0x0700,
                0x2300,
                0x2400,
                0x2900,
                0x2B00,
                0x2F00,
                0x3F00)

    jumps = []
    labels = []    
    labels_set_1 = []
    labels_set_2 = []
    
                
   
    
    string_opcodes = (0x0100,
                     0x0200,
                     0x0600, 
                     0x0A00,
                     0x0E00,
                     0x1300, 
                     0x1800,
                     0x3400,
                     0x4100)



    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        # todo: don't do the paths like this
        if (mode == 0):
            self.file = open(self.file_name, mode="rb")
            self.output = open("Ksd/Decompiled/" + self.file_name.lstrip("Ksd/") + ".txt", mode="w", encoding="shift_jis")
        elif (mode == 1):
            self.file = open("Ksd/Decompiled/" + self.file_name.lstrip("Ksd/") + ".txt", mode="r", encoding="shift_jis")
            self.output = open("Ksd/Recompiled/" + self.file_name.lstrip("Ksd/"), mode="w+b")
        elif (mode == 2):
            self.file = open("Ksd/Voiced/" + self.file_name.lstrip("Ksd/") + ".txt", mode="r", encoding="shift_jis")
            self.output = open("Ksd/Recompiled/" + self.file_name.lstrip("Ksd/"), mode="w+b")


    def decrypt_string(self, name_length):
        last_pos = self.file.tell()
        name_string = bytearray(self.file.read(name_length))
        byte_invert(name_string)
        if len(name_string) % 2 != 0:
            last_pos -= 1
        self.file.seek(last_pos)
        return name_string.decode("shift_jis")


    def encrypt_string(self, s):
        name_string = bytearray(s, "shift_jis")
        byte_invert(name_string)
        return name_string
        
        
    def read_commands(self):
        self.file.seek(4, 0)
        index = 0
        while self.file.tell() != self.file_size:
            try:
                buffer = self.file.read(2)
                buffer = struct.unpack('>H', buffer)[0]  
            except struct.error:
                break                
            #print("0x%02x" % buffer)
            self.args.append([])
            args_struct = ''
            for i in range(len(self.opcodes)):
                if buffer == self.opcodes[i][0]:
                    args_struct = self.opcodes[i][1]
                    break
                 
            for i in args_struct:
                if ((i == 'i') or (i == 'I')):
                    byte_size = 4
                elif ((i == 'h') or (i == 'H')):
                    byte_size = 2
                self.args[index].append(struct.unpack(i, self.file.read(byte_size))[0])         

            self.commands.append(buffer)
            
            
            if self.commands[index] in self.string_opcodes:
                str_length = self.args[index][-1]
                self.args[index].append(self.decrypt_string(str_length))                     
            index += 1


            
    def script_decompile(self):
        self.file.seek(4, 0)
        
        label_index = 0
        preset_label1 = 0
        preset_label2 = 0
        for index in range(len(self.commands)):
            find_offset = 0
            for i in range(len(self.jump_opcodes)):
                if self.commands[index] == self.jump_opcodes[i]:
                    find_offset = 1
                    # the programmer got quirky with the jump opcodes and not only wrote
                    # to the same section tag a few times in one file, sometimes (e.g. 009.ksd)
                    # it's first set to a later offset than in its second occurence
                    # this solution to the problem is kind of garbage
                    if self.commands[index] == 0x2300:
                        self.labels_set_1.append([])
                        self.labels_set_1[preset_label1].append(self.args[index][1])
                        self.labels_set_1[preset_label1].append(self.args[index][0])
                        preset_label1 += 1
                    elif self.commands[index] == 0x2400:
                        self.labels_set_2.append([])
                        self.labels_set_2[preset_label2].append(self.args[index][1])
                        self.labels_set_2[preset_label2].append(self.args[index][0])
                        preset_label2 += 1
                    else:
                        self.labels.append([])
                        self.labels[label_index].append(label_index)
                        self.labels[label_index].append(self.args[index][0])
                        self.args[index][0] = label_index
                        label_index += 1           
                    break
            if find_offset == 0:
                continue
        
        self.file.close()
        
        offset = 4
        last_command = ''
        index = 0
        

        for index in range(len(self.commands)):
            for label in self.labels:
                if offset == label[1]:
                    self.output.write('@' + str(label[0]) + '\n')                   
            for idx, label in enumerate(self.labels_set_1):
                if offset == label[1]:
                    self.output.write('#' + str(label[0]) + '_' + str(idx) + '\n')
            for label in self.labels_set_2:
                if offset == label[1]:
                    self.output.write('!' + str(label[0]) + '\n')                    
            unknown_opcode = 0
            command_name = ''
            args_struct = ''
            unknown_opcode = 1
            for i in range(len(self.opcodes)):
                if self.commands[index] == self.opcodes[i][0]:
                    unknown_opcode = 0
                    args_struct = self.opcodes[i][1]
                    command_name = self.opcodes[i][2]     
                    break
            offset += 2
            
            
            if unknown_opcode == 0:            
                for i in args_struct:                         
                    if ((i == 'h') or (i == 'H')):
                        offset += 2
                    elif ((i == 'i') or (i == 'I')):                      
                        offset += 4        
                                       
                                            
                if (self.commands[index] in self.string_opcodes):
                    if self.args[index][-2] % 2 != 0:  
                        offset -= 1   
                    
                # separating commands with a newline for better readability, comment out if needed
                if command_name[:4] != last_command[:4]:
                    self.output.write('\n') 
                                    
                if self.args[index] != []:  
                    self.output.write(command_name)
                    if self.commands[index] in self.string_opcodes:
                        match self.commands[index]:
                            case 0x0600 | 0x0E00 | 0x1300 | 0x1800 | 0x3400:
                                self.output.write(' ' + str(self.args[index][0]))
                            case _:
                                pass
                        self.output.write(' ' + str(self.args[index][-1]))
                        self.output.write('\n')
                    else:
                        for arg in self.args[index]:
                            self.output.write(' ' + str(arg))
                        self.output.write('\n')
                else:
                    self.output.write(command_name + '\n')

                last_command = command_name
        self.output.close()         
                    

    def script_compile(self):
        lines = self.file.read().split('\n')
        lines = [line for line in lines if line]

        self.output.write(b"KSD1")        
        
        index = 0
        label_index = 0   
        preset_label1 = 0
        preset_label2 = 0
        
        while index < len(lines):
            if "line_set" in lines[index] or "name_set" in lines[index]:
                plaintext = lines[index].split(' ', 1)
            else:
                plaintext = lines[index].split(' ')
            if '@' in plaintext[0]:
                label_number = plaintext[0][1:]
                self.labels.append([])
                self.labels[label_index].append(int(label_number))
                self.labels[label_index].append(self.output.tell())
                label_index += 1
                index += 1
                continue
            elif '#' in plaintext[0]:
                counter = plaintext[0].index('_')
                label_number = plaintext[0][1:counter]
                self.labels_set_1.append([])
                self.labels_set_1[preset_label1].append(int(label_number))
                self.labels_set_1[preset_label1].append(self.output.tell())
                self.labels_set_1[preset_label1].append(int(plaintext[0][counter+1:]))
                preset_label1 += 1
                index += 1   
                continue
            elif '!' in plaintext[0]:
                label_number = plaintext[0][1:]
                self.labels_set_2.append([])
                self.labels_set_2[preset_label2].append(int(label_number))
                self.labels_set_2[preset_label2].append(self.output.tell())
                preset_label2 += 1
                index += 1        
                continue                      
                
            args_struct = ''        
            for i in range(len(self.opcodes)):
                if plaintext[0] == self.opcodes[i][2]:
                    plaintext[0] = self.opcodes[i][0]
                    args_struct = self.opcodes[i][1]
                    break                

            if (plaintext[0] in self.string_opcodes):
                #calc_length = len(plaintext[-1]) * 2
                calc_length = 0
                
                for c in plaintext[-1]:
                    status = unicodedata.east_asian_width(c)
                    if status in ('Na', 'N'):
                        calc_length += 1
                    else:
                        calc_length += 2
                
                match self.opcodes[i][0]:
                    case 0x0100:
                        if '<' in plaintext[-1]:
                            plaintext.insert(1, calc_length - 4)
                        else:
                            plaintext.insert(1, calc_length)
                        plaintext.insert(2, calc_length)
                    case 0x0200 | 0x0A00 | 0x4100:
                        plaintext.insert(1, calc_length)
                    case _:
                        plaintext.insert(2, calc_length)
                        
            self.output.write(struct.pack('>H', self.opcodes[i][0]))      
                                      
            for i in range(1, len(plaintext)):
                try:
                    bb = struct.pack('<' + args_struct[i-1], int(plaintext[i]))
                except:
                    bb = self.encrypt_string(plaintext[i])
                                        
                
                self.output.write(bb)
                                        
            index += 1
            
        self.file.close()
                
        self.output.seek(4, 0)
        offset = 0
        index = 0
        label_index = 0         
        out_size = os.path.getsize("Ksd/Recompiled/" + self.file_name.lstrip("Ksd/")) 

        self.labels_set_1 = sorted(self.labels_set_1, key=lambda x: x[2])           
        ignore = []       
        ignore2 = []
        while self.output.tell() != out_size:
            back = 0
            try:
                buffer = self.output.read(2)
                buffer = struct.unpack('>H', buffer)[0]               
            except struct.error:
                break
            #print("0x%02x" % buffer)
            self.args.append([])
            args_struct = ''
            for i in range(len(self.opcodes)):
                if buffer == self.opcodes[i][0]:
                    args_struct = self.opcodes[i][1]
                    break                        
                                     
            for i in args_struct:
                if ((i == 'i') or (i == 'I')):
                    byte_size = 4
                    back -= 4
                elif ((i == 'h') or (i == 'H')):
                    byte_size = 2
                    back -= 2
                self.args[index].append(struct.unpack(i, self.output.read(byte_size))[0])         

            self.commands.append(buffer)
            
            if (self.commands[index] in self.string_opcodes):
                if self.args[index][-1] % 2 != 0:  
                    self.output.seek(-1, 1)              
            
            # garbage!!
            # should probably just do this before the args_struct loop instead of this nonsense
            for x in range(len(self.jump_opcodes)):
                if buffer == self.jump_opcodes[x]:
                    lastpos = self.output.tell()
                    self.output.seek(back, 1) 
                    
                    if buffer == 0x2300:
                        for i in range(len(self.labels_set_1)):
                            if self.labels_set_1[i][0] == self.args[index][1]:
                                if i in ignore:
                                    continue
                                else:
                                    self.output.write(struct.pack('<I', self.labels_set_1[i][1]))  
                                    ignore.append(i)
                                break                        
                    elif buffer == 0x2400:
                        for i in range(len(self.labels_set_2)):
                            if self.labels_set_2[i][0] == self.args[index][1]:
                                if i in ignore2:
                                    continue
                                else:
                                    self.output.write(struct.pack('<I', self.labels_set_2[i][1]))  
                                    ignore2.append(i)
                                break     
                                             
                    else:
                        for i in range(len(self.labels)):
                            if self.labels[i][0] == self.args[index][0]:
                                self.output.write(struct.pack('<I', self.labels[i][1]))   
                                break
                    self.output.seek(lastpos)
            index += 1

        self.output.close()

infile = input("File: ")
mode = int(input("Mode (0 - export, 1 - import, 2 - add voices): "))

#infile = sys.argv[1]
#mode = 0

ksd = KageScriptData(infile, mode)
if (mode == 0):
    ksd.read_commands()
    ksd.script_decompile()
else:
    ksd.script_compile()