from pathlib import Path
import struct
import argparse
import unicodedata
import ksd_opcodes

def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256

def script_export(game, in_name, out_name):
    with open(in_name, "rb") as file:
        if struct.unpack(">I", file.read(4))[0] != 0x4B534431: #check for "KSD1"
            raise Exception("Invalid KSD file.")

        file_size = Path(in_name).stat().st_size
        commands = {}
        labels = {}

        opcodes = ksd_opcodes.opcodes_moekan if game else ksd_opcodes.opcodes_nijuuei

        while file.tell() != file_size:
            buffer, = struct.unpack(">H", file.read(2))

            if buffer in opcodes:
                arg_fmt, command = opcodes[buffer]
                arg_size = struct.calcsize(arg_fmt)
                args = [*struct.unpack(arg_fmt, file.read(arg_size))]

                if command in ksd_opcodes.string_opcodes:
                    str_length = args[-1]
                    name_string = bytearray(file.read(str_length))
                    byte_invert(name_string)
                    args.append(name_string.decode("cp932"))

                if command in ksd_opcodes.jump_opcodes:
                    labels[args[0]] = f"@{len(labels)}"
                    args[0] = f"@{len(labels) - 1}"
            else:
                raise Exception("Opcode 0x%02x not found (offset: %08x)" % (buffer, file.tell()))

            commands[file.tell()] = command, args

    if not out_name:
        out_name = Path(Path.cwd(), "Exported/Ksd", (Path(in_name).stem + ".txt"))
        Path("Exported/Ksd").mkdir(parents = True, exist_ok = True)

    with open(out_name, "w", encoding = "cp932") as output:
        last_command = ""
        split_at = ("name_set", "nvl_on", "adv_on", "sfx_set",
                    "kgd_layer1_set", "kgd_layer2_set", "kgd_layer3_set", "kgd_layer3_fadeout")

        for offset in commands:
            command, args = commands[offset]

            # ugly way to make output more readable
            if last_command \
            and command in [*split_at, *ksd_opcodes.jump_opcodes] \
            and last_command not in [*split_at, *ksd_opcodes.jump_opcodes]:
                output.write("\n")

            output.write(f"    {command}")
            if args:
                if command in ksd_opcodes.string_opcodes:
                    if command in ("kgd_layer1_set", "kgd_layer2_set", "kgd_layer3_set",
                                    "jump_choice", "sfx_set"):
                        output.write(f" {str(args[0])}")
                    output.write(f" {str(args[-1])}")
                else:
                    for arg in args:
                        output.write(f" {str(arg)}")
            output.write("\n")

            last_command = command

            if offset in labels:
                output.write(f"\n{labels[offset]}\n")
                last_command = ""

def script_import(game, in_name, out_name):
    with open(in_name, "r", encoding = "cp932") as file:
        lines = file.read().split("\n")
        lines = [line.lstrip() for line in lines if line]

    opcodes = ksd_opcodes.opcodes_moekan if game else ksd_opcodes.opcodes_nijuuei
    opcodes_import = {v[1] : (k, v[0]) for k, v in opcodes.items()} # ugly
    commands = {}
    labels = {}
    ofs = 4

    for line in lines:
        args = []

        if line in ("line_set", "name_set"):
            plaintext = line.split(' ', 1)
        else:
            plaintext = line.split(' ')

        if '@' in plaintext[0]:
            labels[plaintext[0]] = ofs
            continue

        # this should probably be calculated on the fly while packing
        if plaintext[0] in opcodes_import:
            opcode, arg_fmt = opcodes_import[plaintext[0]]
            arg_size = struct.calcsize(arg_fmt)

            str_length = 0
            if plaintext[0] in ksd_opcodes.string_opcodes:
                # str_length = len(plaintext[-1]) * 2
                for c in plaintext[-1]:
                    status = unicodedata.east_asian_width(c)
                    if status in ('Na', 'N'):
                        str_length += 1
                    else:
                        str_length += 2

                if plaintext[0] == "line_set":
                    if '<' in plaintext[-1]:
                        plaintext.insert(1, str_length - 4)
                    else:
                        plaintext.insert(1, str_length)
                    plaintext.insert(2, str_length)
                elif plaintext[0] in ("name_set", "ksd_set", "anim_play",
                                    "kqd_display", "voice_play", "music_play_moekan",
                                    "kgd_layer2_set_moekan", "movie_play"):
                        plaintext.insert(1, str_length)
                else:
                        plaintext.insert(2, str_length)

        # moekan voice file names are null-terminated
        # comment out for nijuubako? should probably not cause issues though
        # todo: check if doing this for nijuuei fixes stuff like the shino death scene crashes
        # probably move this to the ugly length calc stuff above if I don't get rid of it
        if plaintext[0] == "voice_play":
            args[1].append(b"\x00\x00")
            str_length += 2

        args = plaintext[1:]
        args = [int(arg) if isinstance(arg, str) and arg.isnumeric()
                else arg for arg in args]
        commands[ofs] = [opcode, args]
        ofs += 2 + arg_size + str_length

    # replace jump tags with actual offsets
    for ofs in commands:
        args = commands[ofs][1]
        args = [labels[arg] if isinstance(arg, str) and arg.startswith("@")
                else arg for arg in args]
        commands[ofs][1] = args

    if not out_name:
        out_name = Path(Path.cwd(), "Imported/Ksd", (Path(in_name).stem + ".ksd"))
        Path("Imported/Ksd").mkdir(parents = True, exist_ok = True)

    with open(out_name, "wb") as output:
        output.write(b"KSD1")
        for ofs in commands:
            opcode = commands[ofs][0]
            args = commands[ofs][1]
            output.write(struct.pack('>H', opcode))
            arg_fmt = opcodes[opcode][0]
            arg_size = struct.calcsize(arg_fmt)

            try:
                output.write(struct.pack(arg_fmt, *args))
            except struct.error:
                output.write(struct.pack(arg_fmt, *args[:len(arg_fmt)]))
                str_to_write = bytearray(args[-1], "cp932")
                byte_invert(str_to_write)
                output.write(str_to_write)


parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("-e", "--export", const=0, dest="mode", action="store_const", help=".ksd -> .txt")
mode.add_argument("-i", "--import", const=1, dest="mode", action="store_const", help=".txt -> .ksd")
parser.add_argument("-g", "--game", metavar="game", dest="game", required=True, action="store",
                    type=int, choices=range(0, 2), help="0 = Nijuuei, 1 = Nijuubako/Moekan/Moeten")
parser.add_argument("in_name", action="store")
parser.add_argument("out_name", action="store", nargs='?', const=None,
                    help="outputs to a subfolder in the working directory if not given")

argv = parser.parse_args()

if (argv.mode == 0):
    script_export(argv.game, argv.in_name, argv.out_name)
else:
    script_import(argv.game, argv.in_name, argv.out_name)