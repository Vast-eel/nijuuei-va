import os
import sys
import struct
from PIL import Image
import zlib
from io import BytesIO

# CONTENDER FOR THIS PROJECT'S WORST SCRIPT ALONGSIDE THE DC SCRIPT CONVERTER
# I WAS SUPPOSED TO HAVE UPLOADED THIS OVER A YEAR AGO BUT FORGOT TO
# I BASICALLY REPLACE PARTS OF THE KGD FILE WITH PNG CHUNK DATA THEN READ IT WITH PILLOW
# THIS IS FUNNY TO LOOK BACK ON BUT I ALSO WANT TO KICK MY OWN ASS
# TO BE REWRITTEN LIKE JUST ABOUT EVERYTHING REALLY

def read_chunk(f):
    # Returns (chunk_type, chunk_data)
    chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
    chunk_data = f.read(chunk_length)
    checksum = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
    chunk_crc = struct.unpack('>I', f.read(4))[0]
    if chunk_crc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
            checksum))
    return chunk_type, chunk_data

class KageGraphicsData:
    file_name = ""
    file_size = 0
    Recon = []
    stride = 0

    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        if (mode == 0):
            self.file = open(self.file_name, mode="rb")
            self.output = self.file_name.rstrip(".kgd") + ".png"
        elif (mode == 1):
            self.file = Image.open(self.file_name, mode="r")
            #self.file = open(self.file_name, mode="rb")
            self.output = open(self.file_name.rstrip(".png") + ".kgd", mode="wb")


    def image_decompile(self):
        self.file.seek(9)
        # one of the strings left in moekan's executable mentions inflate
        # so the below is probably just a quirky IHDR chunk
        width = struct.unpack('<I', self.file.read(4))[0]
        height = struct.unpack('<I', self.file.read(4))[0]
        bit_depth = struct.unpack('<B', self.file.read(1))[0]
        color_type = struct.unpack('<B', self.file.read(1))[0]
        # I think the other parameters are always 0 so let's skip them
        self.file.seek(25)


        construct = BytesIO()
        construct.write(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A\x00\x00\x00\x0D")
        ihdr = bytearray(b"\x49\x48\x44\x52")
        ihdr.extend(struct.pack('>I', width))
        ihdr.extend(struct.pack('>I', height))
        ihdr.extend(struct.pack('>B', bit_depth))
        ihdr.extend(struct.pack('>B', color_type))
        ihdr.extend(b"\x00\x00\x00")
        construct.write(ihdr)
        construct.write(struct.pack('>I', zlib.crc32(ihdr)))
        while self.file.tell() != self.file_size:
            chunk_length = struct.unpack('<I', self.file.read(4))[0]
            self.file.seek(1, 1)
            chunk = self.file.read(chunk_length)
            construct.write(struct.pack('>I', chunk_length))
            construct.write(b"\x49\x44\x41\x54") # idat
            construct.write(chunk)
            construct.write(struct.pack('>I', zlib.crc32(chunk)))
        construct.write(b"\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82")

        im = Image.open(construct)
        if color_type == 6:
            b, g, r, a = im.split()
            im = Image.merge("RGBA", (r, g, b, a))
        else:
            b, g, r = im.split()
            im = Image.merge("RGB", (r, g, b))
        im.save(self.output, compress_level = 9)
        self.file.close()



    def image_compile(self):
        bio = BytesIO()
        if self.file.mode == "RGBA":
            b, g, r, a = self.file.split()
            im = Image.merge("RGBA", (r, g, b, a)).save(bio, format="png", compress_level = 9)
        else:
            b, g, r = self.file.split()
            Image.merge("RGB", (r, g, b)).save(bio, format="png", compress_level = 9)


        #image_data = np.array(self.file)
        self.output.write(b"\x89\x4B\x47\x44\x10\x00\x00\x00\x01")
        self.output.write(struct.pack('<I', self.file.width))
        self.output.write(struct.pack('<I', self.file.height))
        self.output.write(struct.pack('<B', 8))
        if self.file.mode == "RGBA":
            self.output.write(struct.pack('<B', 6))
            #image_data[..., :3] = image_data[..., 2::-1]
        elif self.file.mode == "RGB":
            self.output.write(struct.pack('<B', 2))
            #image_data[..., :2] = image_data[..., 1::-1]
        else:
            raise Exception("Unsupported image type")
        #image_data = zlib.compress(image_data, level = 9)
        self.output.write(b"\x00\x00\x00\x00\x00\x00")

        bio.seek(8)
        image_data = bytearray()
        while True:
            chunk_type, chunk_data = read_chunk(bio)
            if chunk_type == b"IDAT":
                image_data.extend(chunk_data)

                ###
                #self.output.write(struct.pack('<I', len(chunk_data)))
                #self.output.write(struct.pack('<B', 2))
                #self.output.write(chunk_data)
                ###
            if chunk_type == b'IEND':
                break


        chunks = [image_data[i:i+8192] for i in range(0, len(image_data), 8192)]
        #chunks = np.array_split(image_data, 8192)
        for i in range(len(chunks)):
            self.output.write(struct.pack('<I', len(chunks[i])))
            self.output.write(struct.pack('<B', 2))
            self.output.write(chunks[i])

        self.file.close()
        self.output.close()


mode = 1
#x = ("Kgd/FU002.png")
#x = ("Kgd/EXAMPLE_FU002.png")
x = sys.argv[1]
kgd = KageGraphicsData(x, mode)
if (mode == 0):
    kgd.image_decompile()
else:
    kgd.image_compile()

