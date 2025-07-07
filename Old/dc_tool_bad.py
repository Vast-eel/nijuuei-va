#coding=shift-jis
from pathlib import Path
import struct
import unicodedata
import argparse
import re

# LOOKS AND IS AWFUL
# YOU HAVE TO MANUALLY FIX THE SCRIPTS IT EXPORTS TOO
# I DON'T THINK THIS IS EVEN THE VERSION I USED TO EXPORT THE SCRIPTS FOR THE MIKOTO PATCH
# I'LL REWRITE IT SOMEDAY

def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256


opcodes_dc = (
    # -- Text --
    (0x66, 'H', "command_block"),
    (0x86, 'H', "audio_params"),
    (0x8A, 'H', "sprite_params"),
    (0x8C, 'H', "line_params"),
)


command_blocks = (
    (0x00D5, 'H', "voice_play"),
    (0x00D6, 'H', "name_set"),
    (0x00D7, 'HH', ""), # layer2? probably not because its before the date fullscreen cgs
    #(0x0134, 'HH', ""),
    (0x015E, 'HH', "cg_set"), # cg_set
    (0x031D, '', "music_stop2"),
    (0x3585, '', "kgd_layer1_fx 4"), # fx4 - quick shake, fx5 - rumble (nijuuei)
    (0x35AD, '', "kgd_layer1_fx 9"),
    (0x037A, '', "wtf_princesssoft"), # this shows up several times with different behavior
    (0x037B, 'HI', ""), # asset_misc
    (0x03CA, '', "sfx_stop 0\nsfx_unset 0"),
    (0x077A, '', "wait 2000"),
    (0x0882, '', "kgd_layer3_display 0"),
    (0x08A1, '', "kgd_layer3_fadeout 0\nkgd_layer3_clear 0"),
    (0x08B1, '', "kgd_layer1_display"), # might be the other way around with display
    #(0x0B16, '', "kgd_layer2_clear"), # maybe 03A1 instead?
    (0x03A1, '', "kgd_layer2_clear"), # maybe 03A1 instead?
    (0x0B8B, '', "kgd_layer1_fx 0\nkgd_layer1_clear 0"),
    (0x0BA7, '', "kgd_layer1_fx 1"),
    (0x2804, 'BH', "line_set"),
    (0x30AD, '', "nvl_on"),
    (0x30DD, '', "adv_on"),
    (0x3101, '', "nvl_line_clear"),
    (0x36D4, 'HH', "comment"),

    #B - choice header (0xA6), H - offset of next choice, B - other choice shit (0x53)
    # if 0xB3 at offset - repeat
    (0x5A16, 'BHB', "jump_choice"),

    (0x5F23, '', "choice_dialog_end"),

    # 0x70 - new choice
    # 0x93 03 01 00 XX YYYY - XX = which choice, YYYY = offset to jump to
    (0x61B7, '', "choice_dialog_end"),

    (0x65DA, '', ""), # sfx_loop 0
)

# every element of this tuple represents one IQ point lost by me in the making of this patch
assets = (
            (10002, "BG027.KGD"),
            (10003, "BG004.KGD"),
            (10004, "BG023.KGD"),
            (10005, "BG012.KGD"),
            (10006, "BG048.KGD"),
            (10007, "BG001.KGD"),
            (10008, "BG045.KGD"),
            (10009, "BG088.KGD"),
            (10012, "BG010.KGD"),
            (10014, "BG024.KGD"),
            (10019, "BG016.KGD"),
            (10022, "BG026.KGD"),
            (10024, "BG084.KGD"),
            (10025, "BG041.KGD"),
            (10026, "BG019.KGD"),
            (10027, "BG031.KGD"),
            (10028, "BG005.KGD"),
            (10029, "BG013.KGD"),
            (10031, "W1129.KGD"),
            (10032, "BG011.KGD"),
            (10042, "BG020.KGD"),
            (10052, "BG032.KGD"),
            (10063, "BG060.KGD"),
            (10064, "W1211.KGD"),
            (10065, "W1212.KGD"),
            (10066, "W1213.KGD"),
            (10068, "W1214.KGD"),
            (10069, "W1215.KGD"),
            (10070, "W1216.KGD"),
            (10071, "W1217.KGD"),
            (10072, "W1218.KGD"),
            (10073, "W1219.KGD"),
            (10074, "W1220.KGD"),
            (10076, "W1221.KGD"),
            (10077, "W1222.KGD"),
            (10078, "W1223.KGD"),
            (10082, "W1224.KGD"),
            (10113, "W1228.KGD"),
            (10149, "W1225.KGD"),
            (10152, "W1226.KGD"),
            (10153, "W1227.KGD"),
            (20028, "N152.KGD"),
            (30000, "RI001.KGD"),
            (30001, "RI002.KGD"),
            (30002, "RI021.KGD"),
            (30100, "RI003.KGD"),
            (30101, "RI017.KGD"),
            (30203, "RI015.KGD"),
            (30204, "RI018.KGD"),
            (30207, "RI031.KGD"),
            (30300, "RI022.KGD"),
            (30400, "RI011.KGD"),
            (30401, "RI020.KGD"),
            (30600, "KI001.KGD"),
            (30601, "KI002.KGD"),
            (30602, "KI008.KGD"),
            (30603, "KI009.KGD"),
            (30604, "KI018.KGD"),
            (30700, "KI006.KGD"),
            (30701, "KI011.KGD"),
            (30702, "KI012.KGD"),
            (30703, "KI013.KGD"),
            (30704, "KI020.KGD"),
            (30705, "KI021.KGD"),
            (30800, "KI003.KGD"),
            (30801, "KI010.KGD"),
            (30802, "KI019.KGD"),
            (31100, "FU001.KGD"),
            (31102, "FU008.KGD"),
            (31104, "FU011.KGD"),
            (31109, "FU025.KGD"),
            (31201, "FU010.KGD"),
            (31202, "FU003.KGD"),
            (31203, "FU021.KGD"),
            (31500, "KA001.KGD"),
            (31600, "KA002.KGD"),
            (31602, "KA007.KGD"),
            (31700, "KA008.KGD"),
            (31702, "KA021.KGD"),
            (31800, "KA004.KGD"),
            (31801, "KA005.KGD"),
            (31802, "KA010.KGD"),
            (31900, "KA009.KGD"),
            (31901, "KA010.KGD"),
            (32001, "KA013.KGD"),
            (32101, "KA023.KGD"),
            (32200, "SU001.KGD"),
            (32201, "SU002.KGD"),
            (32203, "SU004.KGD"),
            (32300, "SU005.KGD"),
            (32302, "SU006.KGD"),
            (32400, "SU010.KGD"),
            (32401, "SU025.KGD"),
            (33300, "SO018.KGD"),
            (33301, "SO026.KGD"),
            (33302, "SO027.KGD"),
            #(33302, "SO028.KGD"), - check which one is correct
            (33303, "SO028.KGD"),
            (33304, "SO029.KGD"),
            (33305, "SO030.KGD"),
            (33306, "SO031.KGD"),
            (33400, "SO021.KGD"),
            (33401, "SO032.KGD"),
            (33402, "SO033.KGD"),
            (33500, "FU005.KGD"),
            (33503, "KA011.KGD"),
            (33506, "KI005.KGD"),
            (33508, "KI023.KGD"),
            (33510, "RI005.KGD"),
            (33511, "RI007.KGD"),
            (33512, "RI010.KGD"),
            (33514, "SO008.KGD"),
            (33515, "SO009.KGD"),
            (33523, "SO022.KGD"),
            (33526, "SO037.KGD"),
            (33529, "SU011.KGD"),

            # new assets - mikoto sprites numbered based on the order they show up in-game
            (20362, "DC001.KGD"), # asagiri heliport
            (20363, "DC002.KGD"), # mikoto library day
            (20364, "DC003.KGD"), # mikoto library evening
            (20365, "DC004.KGD"), # mikoto wakeup
            (20366, "DC005.KGD"), # mikoto coffee
            (20367, "DC006.KGD"), # mikoto hill
            (20368, "DC007.KGD"), # mikoto tackle
            (20369, "DC008.KGD"), # mikoto garden 1
            (20370, "DC009.KGD"), # mikoto garden 2
            (20371, "DC010.KGD"), # first island whirlpool
            (20372, "DC011.KGD"), # strategy meeting 1
            (20373, "DC012.KGD"), # strategy meeting 2
            (20374, "DC013.KGD"), # strategy meeting 3
            (20375, "DC014.KGD"), # strategy meeting 4
            (20376, "DC015.KGD"), # mikoto ayatori 1
            (20377, "DC016.KGD"), # mikoto ayatori 2
            (20378, "DC017.KGD"), # mikoto captured
            (20379, "DC018.KGD"), # mikoto alice 1
            (20380, "DC019.KGD"), # mikoto alice 2
            (20381, "DC020.KGD"), # fuyuha heal
            (20382, "DC021.KGD"), # mikoto fight 1
            (20383, "DC022.KGD"), # mikoto fight 2
            (20384, "DC023.KGD"), # mikoto fight 3
            (20385, "DC024.KGD"), # mikoto fight 4
            (20386, "DC025.KGD"), # mikoto fight 4
            (20387, "DC026.KGD"), # mikoto end
            (10155, "DC027.KGD"), # mikoto omake kitchen bg
            (10156, "DC028.KGD"), # mikoto omake rinia room bg
            (20402, "DC029.KGD"), # mikoto omake end
            (32800, "MI007.KGD"),
            (32801, "MI005.KGD"),
            (32802, "MI006.KGD"),
            (32803, "MI012.KGD"),
            (32804, "MI010.KGD"),
            (32805, "MI004.KGD"),
            (32806, "MI008.KGD"),
            (32807, "MI011.KGD"),
            (32900, "MI002.KGD"),
            (32901, "MI003.KGD"),
            (32902, "MI009.KGD"),
            (32903, "MI001.KGD"),
     )

class KageScriptData:
    file_size = 0
    mode = 0
    output_name = ""

    opcodes = ()
    command_blocks = ()

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


    def __init__(self, file_name, output_name):
        self.file_size = Path(file_name).stat().st_size
        self.command_blocks = command_blocks
        self.opcodes = opcodes_dc

        self.file = open(file_name, mode="rb")
        if output_name == None:
            self.output_name = Path(Path.cwd(), "Exported/DC", (Path(file_name).stem + ".txt"))
            Path("Exported/DC").mkdir(parents = True, exist_ok = True)
        self.output = open(self.output_name, mode="w", encoding="cp932")


    def script_export(self):
        index = 0
        names = []

        self.file.seek(10480)

        while self.file.tell() != 12352:
            try:
                buffer = self.file.read(1)
                buffer = struct.unpack('<B', buffer)[0]
            except struct.error:
                break
            #print("0x%02x" % buffer)

            if buffer == 0x30:
                has_ofs_next = struct.unpack('<B', self.file.read(1))[0]
                if has_ofs_next == 0xA6:
                    ofs = struct.unpack('<H', self.file.read(2))[0]
                    #print(self.file.read(ofs - self.file.tell()).decode("shift-jis"))
                    names.append(self.file.read(ofs - self.file.tell()).decode("cp932"))

        self.file.seek(27272)

        jump_count = 1

        while self.file.tell() != self.file_size:
            try:
                buffer = self.file.read(1)
                buffer = struct.unpack('<B', buffer)[0]
            except struct.error:
                break
            #print("0x%02x" % buffer)

            for i in range(len(self.opcodes)):
                if buffer == self.opcodes[i][0]:
                    command_block = struct.unpack('<H', self.file.read(2))[0]

                    self.args.append([])
                    args_struct = ''

                    for i in range(len(self.command_blocks)):
                        if command_block == self.command_blocks[i][0]:
                            args_struct = self.command_blocks[i][1]
                            break

                    if command_block == 0x037A:
                        if buffer == 0x8A:
                            args_struct = 'HH'
                        elif buffer == 0x86:
                            args_struct = 'HI'
                        elif buffer == 0x8C:
                            self.file.read(2)
                            break
                    #print(self.file.tell())
                    for i in args_struct:
                        if i == 'i' or i == 'I':
                            byte_size = 4
                        elif i == 'h' or i == 'H':
                            byte_size = 2
                        elif i == 'b' or i == 'B':
                            byte_size = 1
                        self.args[index].append(struct.unpack(i, self.file.read(byte_size))[0])

                    self.commands.append(command_block)

                    if self.commands[index] in (0x2804, 0x36D4):
                        try:
                            ofs = self.args[index][-1]
                            line = re.sub(r"@{1}　?", '',
                                self.file.read(ofs - self.file.tell()).decode("cp932"))
                            self.args[index].append(line)
                        except ValueError:
                            self.args[index].append("")

                    elif self.commands[index] == 0x5A16:
                        fuckyou = 1
                        ofs = self.args[index][1]
                        self.args[index] = [[]]
                        self.args[index][0] = jump_count
                        line = re.sub(r"@{1}　?", '',
                            self.file.read(ofs - self.file.tell()).decode("cp932"))
                        self.args[index].append(line)
                        while fuckyou == 1:
                            if struct.unpack('B', self.file.read(1))[0] == 0xB3:
                                if struct.unpack('B', self.file.read(1))[0] == 0xA6:
                                    jump_count += 1
                                    ofs = struct.unpack('H', self.file.read(2))[0]
                                    #print(ofs)
                                    self.file.seek(1, 1)
                                    line = re.sub(r"@{1}　?", '',
                                        self.file.read(ofs - self.file.tell()).decode("cp932"))
                                    self.args[index].append('\n' + "jump_choice " + str(jump_count) + " " + line)
                            else:
                                fuckyou = 0
                                break

                    elif self.commands[index] == 0x61B7:
                        fuckyou = 1
                        while fuckyou == 1:
                            if struct.unpack('B', self.file.read(1))[0] == 0x70:


                                self.file.seek(4, 1)
                                choice = struct.unpack('H', self.file.read(2))[0]
                                '''
                                self.file.seek(2, 1)
                                ofs = struct.unpack('H', self.file.read(2))[0]
                                self.args[index].append(choice)
                                self.args[index].append(ofs)
                                '''
                                self.labels.append([])
                                self.labels[choice].append(choice)
                                self.file.seek(2, 1)
                                ofs = struct.unpack('H', self.file.read(2))[0]
                                self.labels[choice].append(ofs)
                            else:
                                fuckyou = 0
                                break



                    elif self.commands[index] == 0x00D6:
                        if self.args[index][0] != 0:
                            self.args[index][0] = names[self.args[index][0]]
                    elif self.commands[index] == 0x00D5:
                        vo = self.args[index][0]
                        self.args[index][0] = "v" + str(vo).zfill(5) + ".wav"

                    index += 1

        self.file.close()

        label_index = 0
        preset_label1 = 0
        preset_label2 = 0

        index = 0
        last_command = ''

        sprite_loaded = 0
        bg_loaded = 0
        sfx_stopper = 0

        for index in range(len(self.commands)):
            unknown_opcode = 0
            command_name = ''
            unknown_opcode = 1
            for i in range(len(self.command_blocks)):
                if self.commands[index] == self.command_blocks[i][0]:
                    unknown_opcode = 0
                    args_struct = self.command_blocks[i][1]
                    command_name = self.command_blocks[i][2]
                    break

            if unknown_opcode == 0:
                if command_name == "wtf_princesssoft":
                    if self.commands[index + 1] == 0x08C9:
                        command_name = "kgd_layer3_set"
                        for i in assets:
                            if self.args[index][1] == i[0]:
                                #self.args[index] = [[]]
                                self.args[index][0] = sprite_loaded
                                self.args[index][1] = i[1]
                                if sprite_loaded == 0:
                                    #self.args[index].append("kgd_layer3_param 0 0 0 0 0 800 600\nkgd_layer3_display 0")
                                    self.args[index].append("\nkgd_layer3_param 0 0 0 0 0 800 600")
                                break
                        try:
                            print("test sprite num", int(self.args[index][1]))
                        except:
                            pass
                    elif self.commands[index + 1] == 0x037B:
                        command_name = "music_play_moekan"
                        bgm_name = str(self.args[index][1] + 1).zfill(3) + ".WAV"
                        self.args[index] = [[]]
                        self.args[index][0] = bgm_name
                    elif self.commands[index + 1] == 0x08A1:
                        command_name = "sfx_set"
                        sfx_name = "SE" + str(self.args[index][1] + 1).zfill(3) + ".WAV"
                        self.args[index] = [[]]
                        self.args[index][0] = sfx_name
                    elif self.commands[index + 1] == 0x08B1:
                        command_name = "kgd_layer1_set"
                        for i in assets:
                            if self.args[index][1] == i[0]:
                                self.args[index][0] = bg_loaded
                                self.args[index][1] = i[1]
                                #self.args[index] = [[]]
                                #self.args[index][0] = kgd_name
                                break
                        try:
                            print("test bg num", int(self.args[index][1]))
                        except:
                            pass
                    else:
                        #print("0x%02x" % self.commands[index + 1])
                        command_name = "sfx_set"
                        self.args[index][0] = 0
                        if self.args[index][1] <= 82:
                            sfx_name = str(self.args[index][1] + 1).zfill(3)
                        else:
                            sfx_name = str(self.args[index][1]).zfill(3)
                        self.args[index][1] = "SE" + sfx_name + ".WAV"
                        if self.commands[index - 1] == 0x65DA:
                            self.args[index].append("\nsfx_loop 0")
                        else:
                            self.args[index].append("\nsfx_play 0 0")
                            sfx_stopper = 1
                elif command_name == "cg_set":
                    command_name = "kgd_layer1_set"
                    for i in assets:
                        if self.args[index][1] == i[0]:
                            self.args[index][0] = bg_loaded
                            self.args[index][1] = i[1]
                            self.args[index].append("\nkgd_layer2_clear")
                            #self.args[index] = [[]]
                            #self.args[index][0] = kgd_name
                            break
                    print("test cg num", self.args[index][1])
                elif command_name == "kgd_layer3_fadeout 0\nkgd_layer3_clear 0":
                    sprite_loaded = 0
                elif command_name == "kgd_layer1_fx 0\nkgd_layer1_clear 0":
                    bg_loaded = 0
                elif command_name == "sfx_stop 0\nsfx_unset 0":
                    sfx_stopper = 0
                elif command_name == "name_set" and self.args[index][0] == 0:
                    command_name = "name_clear"
                    self.args[index] = []
                elif command_name == "kgd_layer3_display 0":
                    if sprite_loaded == 3:
                        command_name = "kgd_layer3_param 3 0 0 0 0 800 600\nkgd_layer3_unk7 0\nkgd_layer3_crossfade 0 3 31 3"
                    else:
                        sprite_loaded = 3
                elif command_name == "kgd_layer1_display":
                    if bg_loaded == 1:
                        command_name = "kgd_layer1_crossfade 0 26\nkgd_layer1_clear 1"
                    else:
                        bg_loaded = 1
                elif command_name == "kgd_layer1_fx 1":
                    if last_command == "kgd_layer1_crossfade 0 26\nkgd_layer1_clear 1":
                        command_name = ""
                    elif last_command == "kgd_layer1_set":
                        command_name = "kgd_layer1_crossfade 0 26\nkgd_layer1_clear 1"

                # separating commands with a newline for better readability, comment out if needed
                if command_name[:4] != last_command[:4]:
                    self.output.write('\n')

                if command_name in ("line_set", "voice_play", "name_set", "comment"):
                    if self.args[index] != []:
                        self.output.write(command_name)
                        if command_name in ("line_set", "comment"):
                            self.output.write(' ' + str(self.args[index][-1]))
                            if sfx_stopper == 1:
                                self.output.write("\nsfx_stop 0\nsfx_unset 0")
                                sfx_stopper = 0

                        else:
                            for arg in self.args[index]:
                                try:
                                    self.output.write(' ' + str(arg))
                                except:
                                    self.output.write(' ' + arg)
                        self.output.write('\n')
                    else:
                        self.output.write(command_name + '\n')

                last_command = command_name


        '''
        for x in range(len(names)):
            self.output.write("(" + str(x) + ", " + "\"" + names[x] + "\")," + '\n')
        '''
        self.output.close()


parser = argparse.ArgumentParser()
parser.add_argument("file_name", action="store")
parser.add_argument("output_name", action="store", nargs='?', const=None,
                    help="outputs to a subfolder in the working directory if not given")

args = parser.parse_args()

ksd = KageScriptData(args.file_name, args.output_name)
ksd.script_export()