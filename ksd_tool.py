from pathlib import Path
import struct
import unicodedata
import argparse


def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256


opcodes_nijuuei = (
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
    (0x4200, '', "ed_play"),
    (0x4300, '', "force_save_menu"),
    (0x4400, 'I', "wait")
)


opcodes_moekan = (
    # -- Text --
    (0x0100, 'HH', "line_set"), # IHH for moeten. nvl/adv is baked directly into the command, crazy
    (0x0200, 'h', "voice_play"),
    (0x0300, 'h', "name_set"),
    (0x0400, '', "name_clear"),
    (0x0600, '', "nvl_line_clear"),
    (0x0700, 'h', "story_progress"),
    (0x0800, 'IH', "jump_choice"),
    (0x0900, 'I', "jump_auto"),
    (0x0A00, '', "nvl_on"),
    (0x0B00, '', "adv_on"),
    (0x0C00, 'h', "ksd_set"),
    (0x0D00, '', "ecchi_end"),
    (0x0E00, '', "route_end"),
    (0x0F00, '', "ksd_end"),
    (0x1000, 'i', "wait"),

    # -- Graphics --
    # Layer 1: Fullscreen backgrounds/CGs
    (0x1600, 'hh', "kgd_layer1_set"),
    (0x1700, '', "kgd_layer1_display"),
    (0x1900, 'h', "kgd_layer1_clear"),
    (0x1A00, '', "kgd_layer1_unk1"),

    # Layer 2: Date in the upper right of the screen
    # Gets two opcodes later on. Would be more sensible to swap layers 2 and 3 naming-wise
    # but I wanted to keep it consistent between games

    # Layer 3: Character sprites
    (0x1B00, 'hh', "kgd_layer3_set"),
    (0x1C00, 'HiiiiII', "kgd_layer3_param"),
    (0x1D00, 'h', "kgd_layer3_display"),
    (0x1E00, 'h', "kgd_layer3_fadeout"),
    (0x1F00, 'h', "kgd_layer3_clear"),
    (0x2000, 'Hh', "kgd_layer1_solidcolor"),
    (0x2100, 'hhhh', "kgd_layer3_crossfade"),

    # -- Progression flags --
    (0x2300, 'h', "unk2"),
    (0x2400, 'h', "unk3"),
    (0x2500, 'h', "gallery_unlock"),
    (0x2600, 'h', "nijuubako_opcode01"),
    (0x2700, 'ih', "jump_type1"),
    (0x2800, 'ih', "jump_type2"),
    (0x2900, 'h', "unk4"),
    (0x2A00, 'h', "unk5"),
    (0x2B00, 'hhhh', "unk6"),
    (0x2D00, 'ih', "jump_type3"),
    # 00 - rinia
    # haven't tested the ones below
    # 01 - kazusa?
    # 02 - fuyuha?
    # 03 - suzuki?
    # 04 - kirishima?

    (0x2F00, 'ihhhh', "jump_type4"),
    (0x3000, 'ihhhh', "jump_type5"),
    (0x3100, 'ihhhh', "jump_type6"),
    (0x3300, 'ihhhh', "jump_type7"),

    # -- Audio --
    (0x3800, 'h', "music_play_moekan"),
    (0x3900, '', "music_stop1"),
    (0x3A00, '', "music_stop2"),
    (0x3B00, 'hh', "sfx_set"),
    (0x3C00, 'hh', "sfx_play"), # 'h' for nijuubako
    (0x3D00, 'h', "sfx_loop"),
    (0x3E00, 'h', "sfx_stop"),
    (0x3F00, 'h', "sfx_unset"),

    # -- Graphical effects --
    (0x4100, 'hh', "kgd_layer1_crossfade"),
    (0x4200, 'h', "kgd_layer3_unk7"),
    (0x4300, 'h', "kgd_layer1_fx"),
    (0x4400, 'h', "kqd_display"),

    # -- Other --
    (0x4A00, '', "nijuubako_opcode02"),
    (0x4C00, '', "choice_dialog_end"),
    (0x4D00, 'h', "kgd_layer2_set_moekan"),
    (0x4E00, '', "kgd_layer2_clear"),
    (0x4F00, 'H', "movie_play"),
    (0x5000, '', "unk8"),
    (0x5200, 'ih', "jump_rinia_bad_end")
)


jump_opcodes_def = (
    "jump_choice",
    "jump_auto",
    "jump_branch1",
    "jump_branch2",
    "jump_route_038",
    "jump_route_036",
    "jump_route",
    "jump_fight_failure",

    "jump_type1",
    "jump_type2",
    "jump_type3",
    "jump_type4",
    "jump_type5",
    "jump_type6",
    "jump_type7",
    "jump_rinia_bad_end"
)


string_opcodes_def = (
    "line_set",
    "name_set",
    "jump_choice",
    "ksd_set",
    "kgd_layer1_set",
    "kgd_layer2_set",
    "kgd_layer3_set",
    "sfx_set",
    "anim_play",

    "kqd_display",

    "voice_play",
    "music_play_moekan",
    "kgd_layer2_set_moekan",
    "movie_play"
)


class KageScriptData:
    file_size = 0
    mode = 0
    output_name = ""

    opcodes = ()

    commands = []
    args = []

    jumps = []
    labels = []


    def match_opcodes(self, opcode_subset):
        dict = {}
        for i in self.opcodes:
            for j in opcode_subset:
                if j == i[2]:
                    dict[j] = i[0]
        return dict


    def __init__(self, file_name, flag, mode, output_name):
        self.file_size = Path(file_name).stat().st_size
        self.mode = mode

        if self.mode == 0:
            self.opcodes = opcodes_nijuuei
            self.labels_set_1 = []
            self.labels_set_2 = []
        elif self.mode == 1:
            self.opcodes = opcodes_moekan
        self.jump_opcodes = self.match_opcodes(jump_opcodes_def)
        self.string_opcodes = self.match_opcodes(string_opcodes_def)

        if flag == 0:
            self.file = open(file_name, mode="rb")
            if output_name == None:
                self.output_name = Path(Path.cwd(), "Exported/KSD", (Path(file_name).stem + ".txt"))
                Path("Exported/KSD").mkdir(parents = True, exist_ok = True)
            else:
                self.output_name = output_name
            self.output = open(self.output_name, mode="w", encoding="cp932")
        elif flag == 1:
            self.file = open(file_name, mode="r", encoding="cp932")
            if output_name == None:
                self.output_name = Path(Path.cwd(), "Imported/KSD", (Path(file_name).stem + ".ksd"))
                Path("Imported/KSD").mkdir(parents = True, exist_ok = True)
            else:
                self.output_name = output_name
            self.output = open(self.output_name, mode="wb")


    def script_export(self):
        if struct.unpack('>I', self.file.read(4))[0] != 0x4B534431:
            raise Exception("Invalid KSD file.")

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
                if i == 'i' or i == 'I':
                    byte_size = 4
                elif i == 'h' or i == 'H':
                    byte_size = 2
                self.args[index].append(struct.unpack(i, self.file.read(byte_size))[0])

            self.commands.append(buffer)

            if self.commands[index] in self.string_opcodes.values():
                str_length = self.args[index][-1]
                last_pos = self.file.tell()
                name_string = bytearray(self.file.read(str_length))
                byte_invert(name_string)
                if len(name_string) % 2 != 0:
                    last_pos -= 1
                self.file.seek(last_pos)
                #print(self.file.tell(), "0x%02x" % self.commands[index], self.args[index])
                self.args[index].append(name_string.decode("cp932"))

            index += 1

        self.file.close()

        label_index = 0
        preset_label1 = 0
        preset_label2 = 0

        for index in range(len(self.commands)):
            find_offset = 0
            for i in self.jump_opcodes:
                if self.commands[index] == self.jump_opcodes[i]:
                    find_offset = 1
                    # the programmer got quirky with the jump opcodes and not only wrote to
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

        index = 0
        offset = 4
        last_command = ''

        for index in range(len(self.commands)):
            for label in self.labels:
                if offset == label[1]:
                    self.output.write('@' + str(label[0]) + '\n')
            if self.mode == 0:
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
                    if i == 'h' or i == 'H':
                        offset += 2
                    elif i == 'i' or i == 'I':
                        offset += 4

                if self.commands[index] in self.string_opcodes.values():
                    if self.args[index][-2] % 2 != 0:
                        offset -= 1

                # separating commands with a newline for better readability, comment out if needed
                if command_name[:4] != last_command[:4]:
                    self.output.write('\n')

                if self.args[index] != []:
                    self.output.write(command_name)
                    if self.commands[index] in self.string_opcodes.values():
                        if self.commands[index] in (
                            self.string_opcodes.get("jump_choice"),
                            self.string_opcodes.get("kgd_layer1_set"),
                            self.string_opcodes.get("kgd_layer2_set"),
                            self.string_opcodes.get("kgd_layer3_set"),
                            self.string_opcodes.get("sfx_set")
                        ):
                            self.output.write(' ' + str(self.args[index][0]))
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


    def script_import(self):
        lines = self.file.read().split('\n')
        lines = [line for line in lines if line]

        index = 0
        label_index = 0
        preset_label1 = 0
        preset_label2 = 0
        ofs = 4

        for line in range(len(lines)):
            if "line_set" in lines[line] or "name_set" in lines[line]:
                plaintext = lines[line].split(' ', 1)
            else:
                plaintext = lines[line].split(' ')
            if '@' in plaintext[0]:
                label_number = plaintext[0][1:]
                self.labels.append([])
                self.labels[label_index].append(int(label_number))
                self.labels[label_index].append(ofs)
                label_index += 1
                continue
            elif '#' in plaintext[0]:
                counter = plaintext[0].index('_')
                label_number = plaintext[0][1:counter]
                self.labels_set_1.append([])
                self.labels_set_1[preset_label1].append(int(label_number))
                self.labels_set_1[preset_label1].append(ofs)
                self.labels_set_1[preset_label1].append(int(plaintext[0][counter+1:]))
                preset_label1 += 1
                continue
            elif '!' in plaintext[0]:
                label_number = plaintext[0][1:]
                self.labels_set_2.append([])
                self.labels_set_2[preset_label2].append(int(label_number))
                self.labels_set_2[preset_label2].append(ofs)
                preset_label2 += 1
                continue

            args_struct = ''
            self.args.append([])
            for i in range(len(self.opcodes)):
                if plaintext[0] == self.opcodes[i][2]:
                    args_struct = self.opcodes[i][1]
                    break

            if plaintext[0] in self.string_opcodes:
                # calc_length = len(plaintext[-1]) * 2
                calc_length = 0

                for c in plaintext[-1]:
                    status = unicodedata.east_asian_width(c)
                    if status in ('Na', 'N'):
                        calc_length += 1
                    else:
                        calc_length += 2

                if plaintext[0] == "line_set":
                    if '<' in plaintext[-1]:
                        plaintext.insert(1, calc_length - 4)
                    else:
                        plaintext.insert(1, calc_length)
                    plaintext.insert(2, calc_length)
                elif plaintext[0] in (
                    "name_set",
                    "ksd_set",
                    "anim_play",

                    "kqd_display",

                    "voice_play",
                    "music_play_moekan",
                    "kgd_layer2_set_moekan",
                    "movie_play"
                ):
                        plaintext.insert(1, calc_length)
                else:
                        plaintext.insert(2, calc_length)

            self.commands.append(struct.pack('>H', self.opcodes[i][0]))
            ofs += 2

            #print(plaintext)
            for i in range(1, len(plaintext)):
                try:
                    packed = struct.pack('<' + args_struct[i-1], int(plaintext[i]))
                except:
                    packed = bytearray(plaintext[i], "cp932")
                    byte_invert(packed)
                self.args[index].append(packed)
                ofs += len(packed)

            # there are two extra bytes at the end of every voice file name in moekan.
            # probably not needed, but I wanted 1:1 imports/exports, so uncomment if you care
            '''
            if plaintext[0] == "voice_play":
                self.args[index][1] += (b"\x00\x00")
                ofs += 2
            '''
            index += 1

        self.file.close()

        if self.mode == 0:
            self.labels_set_1 = sorted(self.labels_set_1, key=lambda x: x[2])

        for i in range(len(self.commands)):
            buffer = struct.unpack('>H', self.commands[i])[0]
            if buffer in self.jump_opcodes.values():
                if buffer == 0x2300 and self.mode == 0:
                    for j in range(len(self.labels_set_1)):
                        if self.labels_set_1[j][0] == struct.unpack('<H', self.args[i][1])[0]:
                            self.args[i][0] = struct.pack('<I', self.labels_set_1[j][1])
                            del self.labels_set_1[j]
                            break
                elif buffer == 0x2400 and self.mode == 0:
                    for j in range(len(self.labels_set_2)):
                        if self.labels_set_2[j][0] == struct.unpack('<H', self.args[i][1])[0]:
                            self.args[i][0] = struct.pack('<I', self.labels_set_2[j][1])
                            del self.labels_set_2[j]
                            break
                else:
                    for j in range(len(self.labels)):
                        if self.labels[j][0] == struct.unpack('<I', self.args[i][0])[0]:
                            self.args[i][0] = struct.pack('<I', self.labels[j][1])
                            break

        self.output.write(b"KSD1")
        for i in range(len(self.commands)):
            self.output.write(self.commands[i])
            for j in self.args[i]:
                self.output.write(j)

        self.output.close()


parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("-e", "--export", const=0, dest="flag", action="store_const", help=".ksd -> .txt")
mode.add_argument("-i", "--import", const=1, dest="flag", action="store_const", help=".txt -> .ksd")
parser.add_argument("-m", "--mode", metavar="mode", dest="mode", required=True, action="store",
                    type=int, choices=range(0, 2), help="0 = Nijuuei, 1 = Nijuubako/Moekan/Moeten")
parser.add_argument("file_name", action="store")
parser.add_argument("output_name", action="store", nargs='?', const=None,
                    help="outputs to a subfolder in the working directory if not given")

args = parser.parse_args()

ksd = KageScriptData(args.file_name, args.flag, args.mode, args.output_name)
if (args.flag == 0):
    ksd.script_export()
else:
    ksd.script_import()