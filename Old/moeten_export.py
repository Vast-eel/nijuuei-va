import struct

with open("Moeten/001.dat", mode='rb') as hdr:
    hdr.seek(12)
    hdr_size = struct.unpack("i", hdr.read(4))[0] + 12
    while hdr.tell() != hdr_size:
        file_name = hdr.read(16).decode("shift-jis").rstrip('\x00')
        file_size = struct.unpack("i", hdr.read(4))[0]
        file_offset = struct.unpack("i", hdr.read(4))[0]
        last = hdr.tell()
        with open("Bako/" + file_name, mode='wb') as output:
            hdr.seek(file_offset)
            output.write(hdr.read(file_size))
        hdr.seek(last)