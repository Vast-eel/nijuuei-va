from pathlib import Path
import struct
import unicodedata
import argparse


def byte_invert(array):
    for i in range(0, len(array)):
        array[i] = ~array[i] + 256


class KagePhraseData:
    file_size = 0
    output_name = ""

    phrases = []
    offsets = []


    def __init__(self, file_name, flag, output_name):
        self.file_name = file_name
        self.file_size = Path(file_name).stat().st_size

        if flag == 0:
            self.file = open(file_name, mode="rb")
            if output_name == None:
                self.output_name = Path(Path.cwd(), "Exported/", (Path(file_name).stem + ".txt"))
                Path("Exported/").mkdir(parents = True, exist_ok = True)
            else:
                self.output_name = output_name
            self.output = open(self.output_name, mode="w", encoding="cp932")
        elif flag == 1:
            self.file = open(file_name, mode="r", encoding="cp932")
            if output_name == None:
                self.output_name = Path(Path.cwd(), "Imported/", (Path(file_name).stem + ".kpd"))
                Path("Imported/").mkdir(parents = True, exist_ok = True)
            else:
                self.output_name = output_name
            self.output = open(self.output_name, mode="wb")


    def script_export(self):
        if struct.unpack('>I', self.file.read(4))[0] != 0x4B504431:
            raise Exception("Invalid KPD file.")

        index = 0
        phrase_count = struct.unpack('<I', self.file.read(4))[0]
        while index < phrase_count:
            self.offsets.append(struct.unpack('<I', self.file.read(4))[0])
            index += 1

        index = 0
        while self.file.tell() != self.file_size:
            for i in self.offsets:
                if self.file.tell() == i:
                    self.phrases.append([])
                    for i in range(0, 2):
                        length = struct.unpack('<H', self.file.read(2))[0]
                        last_pos = self.file.tell()
                        name_string = bytearray(self.file.read(length))
                        byte_invert(name_string)
                        if len(name_string) % 2 != 0:
                            last_pos -= 1
                        self.file.seek(last_pos)
                        self.phrases[index].append(name_string.decode("cp932"))
                        if i == 1:
                            break
                        self.file.seek(length, 1)
                    index += 1
            self.file.seek(2, 1)

        self.file.close()

        for i in range(len(self.phrases)):
            self.output.write('#' + str(i) + '\n')
            self.output.write(self.phrases[i][0] + '\n' + self.phrases[i][1] + '\n\n')

        self.output.close()


    def script_import(self):
        lines = self.file.read().split('\n\n')
        lines = [line for line in lines if line]

        header = bytearray(b"KPD1")
        content = bytearray()

        counter = 0
        for line in lines:
            plaintext = line.split('\n', 2)
            if '#' in plaintext[0]:
                self.phrases.append([])
                counter = int(plaintext[0][1:])
                self.phrases[counter].append(plaintext[1])
                self.phrases[counter].append(plaintext[2])

        self.file.close()

        header.extend(struct.pack('<I', counter + 1))
        header_length = counter * 4 + 12

        ofs = header_length
        for i in self.phrases:
            for x in range(len(i)):
                if x == 0:
                    self.offsets.append(ofs)

                calc_length = 0
                normal_width_characters = 0

                for c in i[x]:
                    status = unicodedata.east_asian_width(c)
                    if status == 'Na':
                        calc_length += 1
                        normal_width_characters += 1
                    elif status == 'N':
                        calc_length += 1
                    else:
                        calc_length += 2

                content.extend(struct.pack('<H', calc_length))
                ofs += calc_length + 2

                name_string = bytearray(i[x], "cp932")
                byte_invert(name_string)
                content.extend(name_string)

        for i in self.offsets:
            header.extend(struct.pack('<I', i))

        self.output.write(header)
        self.output.write(content)

        self.output.close()


parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("-e", "--export", const=0, dest="flag", action="store_const", help=".kpd -> .txt")
mode.add_argument("-i", "--import", const=1, dest="flag", action="store_const", help=".txt -> .kpd")
parser.add_argument("file_name", action="store")
parser.add_argument("output_name", action="store", nargs='?', const=None,
                    help="outputs to a subfolder in the working directory if not given")
args = parser.parse_args()


kpd = KagePhraseData(args.file_name, args.flag, args.output_name)
if args.flag == 0:
    kpd.script_export()
else:
    kpd.script_import()