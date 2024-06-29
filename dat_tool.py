from pathlib import Path
import struct
import argparse

class KeroDAT:
    file_amount = 0
    offsets = []

    def __init__(self, file_name, flag, mode, output_name):
        if mode == 1:
            print("Moeten support is currently unimplemented.")
            exit()

        if flag == 0:
            self.hdr = open(file_name, mode="rb")
            pac_name = '%03d' % (int(Path(file_name).stem) + 1) + ".dat"
            pac_name = Path((Path(file_name).parent), pac_name)
            self.pac = open(pac_name, mode="rb")
            if output_name == None:
                self.output_name = Path(Path.cwd(), "Exported/Dat", (Path(file_name).stem))
                Path(self.output_name).mkdir(parents = True, exist_ok = True)
            else:
                self.output_name = output_name
                Path(self.output_name).mkdir(parents = True, exist_ok = True)
        elif flag == 1:
            self.file_list = [f for f in Path(file_name).iterdir() if f.is_file()]
            if output_name == None:
                Path("Imported/Dat").mkdir(parents = True, exist_ok = True)
                hdr_name = Path(Path.cwd(), "Imported/Dat", (Path(file_name).stem + ".dat"))
                self.hdr = open(hdr_name, mode="wb")
                pac_name = '%03d' % (int(Path(file_name).stem) + 1) + ".dat"
                pac_name = Path(Path.cwd(), "Imported/Dat", pac_name)
                self.pac = open(pac_name, mode="wb")
            else:
               self.hdr = open(output_name, mode="wb")
               self.pac = open(Path(output_name).with_suffix(".pac"), mode="wb")

        # TODO: moeten has hdr and dat in one file, easy but I can't be bothered right now

    def file_export(self):
        self.hdr.seek(4)
        file_amount = struct.unpack("i", self.hdr.read(4))[0]
        self.pac.seek(4)
        if struct.unpack("i", self.pac.read(4))[0] == file_amount:
            for i in range(file_amount):
                file_name = self.hdr.read(16).decode("cp932").rstrip('\x00')
                file_size = struct.unpack("i", self.hdr.read(4))[0]
                file_offset = struct.unpack("i", self.hdr.read(4))[0]
                with open(Path(self.output_name)/file_name, mode='wb') as output:
                    self.pac.seek(file_offset)
                    output.write(self.pac.read(file_size))
        self.hdr.close()
        self.pac.close()

    def file_import(self):
        self.pac.write(b"\x89\x50\x41\x43")
        self.pac.write(struct.pack("<I", len(self.file_list)))

        self.file_list.sort()

        for file_name in self.file_list:
            with open(file_name, mode='rb') as file:
                self.offsets.append(self.pac.tell())
                self.pac.write(file.read())
        self.pac.close()

        self.hdr.write(b"\x89\x48\x44\x52")
        self.hdr.write(struct.pack("<I", len(self.file_list)))

        i = 0
        for file_name in self.file_list:
            padding = 16 - len(file_name.name)
            padded = bytearray(file_name.name, "cp932") + (b'\x00' * padding)
            self.hdr.write(padded)
            file_size = Path(file_name).stat().st_size
            self.hdr.write(struct.pack("<I", file_size))
            self.hdr.write(struct.pack("<I", self.offsets[i]))
            i += 1
        self.pac.close()


parser = argparse.ArgumentParser()
mode = parser.add_mutually_exclusive_group(required=True)
mode.add_argument("-e", "--export", const=0, dest="flag", action="store_const", help="unpack files")
mode.add_argument("-i", "--import", const=1, dest="flag", action="store_const", help="pack files")
parser.add_argument("-m", "--mode", metavar="mode", dest="mode", required=True, action="store",
                    type=int, choices=range(0, 2), help="0 = Nijuubako/Moekan, 1 = Moeten")
parser.add_argument("file_name", action="store")
parser.add_argument("output_name", action="store", nargs='?', const=None,
                    help="outputs to a subfolder in the working directory if not given")

args = parser.parse_args()

dat = KeroDAT(args.file_name, args.flag, args.mode, args.output_name)
if (args.flag == 0):
    dat.file_export()
else:
    dat.file_import()