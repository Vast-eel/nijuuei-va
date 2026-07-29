import struct
from pathlib import Path, PureWindowsPath
import sys

def aim_decompress(aim):
    ofs, = struct.unpack("<I", aim[0x1A:0x1E])
    ofs += 0x10 # +0x10 to skip the filename field
    width, = struct.unpack("<I", aim[0x22:0x26])
    height, = struct.unpack("<I", aim[0x26:0x2A])
    bit_count, = struct.unpack("<H", aim[0x2C:0x2E])
    byte_count = bit_count >> 3

    dec = bytearray()
    for i in range(ofs, len(aim) - byte_count, byte_count + 1):
        if bit_count == 24:
            bgr = struct.unpack("<3B", aim[i:i+3])
            mul, = struct.unpack("<B", aim[i+3:i+4])
        elif bit_count == 8:
            bgr = struct.unpack("<B", aim[i:i+1])
            mul, = struct.unpack("<B", aim[i+1:i+2])
        dec.extend(bgr * mul)

    # bmps are evil and stored upside down
    # there's probably a way to do this in-place with numpy or smth
    row_size = width * byte_count
    final = bytearray(aim[0x10:ofs])
    for y in range(height - 1, -1, -1):
        start = y * row_size
        end = start + row_size
        final.extend(dec[start:end])

    return final

def aod_extract(packfile):
    with open(packfile, "rb") as aod:
        out_path = Path(packfile.stem)
        defs = []
        stop_def = False
        while not stop_def:
            fname = aod.read(40)
            if fname == b'' or fname[0] == 0x00:
                stop_def = True
                break
            ofs, = struct.unpack("<I", aod.read(4))
            fsize, = struct.unpack("<I", aod.read(4))
            aod.read(16)
            if fname[0] == 0xFF:
                aod.seek(ofs, 1)
            else:
                fname = fname.decode("cp932").rstrip('\x00')
                fname = PureWindowsPath(fname)
                defs.append([fname, ofs+aod.tell(), fsize])
                p = Path(packfile.stem, fname).parent
                p.mkdir(parents=True, exist_ok=True)

        for file in defs:
            aod.seek(file[1])
            if file[2]:
                data = bytearray(aod.read(file[2]))
                if file[0].suffix == ".wcm":
                    file[0] = file[0].with_suffix(".txt")
                    for i in range(0, len(data)):
                        data[i] = ~data[i] + 256
                elif file[0].suffix == ".aim":
                    file[0] = file[0].with_suffix(".bmp")
                    data = aim_decompress(data)

                with open(Path(out_path, file[0]), "wb") as out:
                    print(Path(out_path, file[0]))
                    out.write(data)

if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        packfile = Path(arg)
        if packfile.suffix == ".aod":
            aod_extract(packfile)
else:
    for packfile in Path.cwd().glob('*.aod'):
        aod_extract(packfile)
