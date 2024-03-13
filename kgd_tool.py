import os
import sys
import struct
from PIL import Image
from io import BytesIO

class KageGraphicsData:
    file_name = ""
    file_size = 0

    jumps = []
    jump_offsets = []

    jump_tags = []
    jump_tag_offsets = []

    offsets = []
    phrases = []

        


    def __init__(self, file_name, mode):
        self.file_name = file_name
        self.file_size = os.path.getsize(file_name)
        if (mode == 0):
            self.file = open(self.file_name, mode="rb")
            self.output = self.file_name.rstrip(".kgd") + ".png"
        elif (mode == 1):
            self.file = Image.open(self.file_name, mode="r")
            self.output = open(self.file_name.rstrip(".png") + ".kgd", mode="wb")
            

    def image_decompile(self):
        self.file.seek(6)
        depth = struct.unpack('<H', self.file.read(2))[0]
        width = struct.unpack('<I', self.file.read(4))[0]
        height = struct.unpack('<I', self.file.read(4))[0]
        img_size_1 = struct.unpack('<I', self.file.read(4))[0]
        img_size_2 = struct.unpack('<I', self.file.read(4))[0]
        data = self.file.read()
        if depth == 24:
            im = Image.frombytes('RGB', (width, height), data)
        #else:
        #    im = Image.frombytes('P', (width, height), data, "raw", 'P', 0)
             #palette=Image.ADAPTIVE)
        b, g, r = im.split()
        im = Image.merge("RGB", (r, g, b))
        im.show()
        im.save(self.output)
        
            
    def image_compile(self):
        # will rewrite later when I figure out the 8-bit images
        self.output.write(b"KGD1")
        self.output.write(struct.pack('<H', 24))
        self.output.write(struct.pack('<H', 24))
        self.output.write(struct.pack('<I', 800))
        self.output.write(struct.pack('<I', 600))
        self.output.write(struct.pack('<I', 0))
        try:
            r, g, b, a = self.file.split()
        except ValueError:
            r, g, b = self.file.split()
        img = Image.merge("RGB", (b, g, r))        
        img = img.tobytes()
        self.output.write(struct.pack('<I', len(img)))
        self.output.write(img)
        
                    

mode = 1
x = ("Compiled CGs/Dc_Irusui04.png")
kgd = KageGraphicsData(x, mode)
#x = sys.argv[1]
#kgd = KageGraphicsData(x, mode)
if (mode == 0):
    kgd.image_decompile()
else:
    kgd.image_compile()

